import cv2
import numpy as np
import func
import match
import blending
from SIFTMatcher import SIFTMatcher
from glob import glob

# Configs
THRESHOLD = 0.7

def main():
    name = 'View'
    imgList = glob('./data/{}*.JPG'.format(name))
    panoFileName = './result/pano_{}.jpg'.format(name)

    # Read Images
    Images = {}
    for idx, imgPath in enumerate(sorted(imgList)):
        img = cv2.imread(imgPath)
        Images.update({idx: img})
        print(idx, imgPath)
    print('Images loaded. Beginning feature detection...')

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # Extract SIFT features
    Descriptor = {}
    PointInImg = {}
    for idx, (key, img) in enumerate(sorted(Images.items())):
        I = np.asarray(img)
        f, d = sift.detectAndCompute(I, None)
        PointInImg.update({idx: f})
        Descriptor.update({idx: d})

    # Show match result
    if len(Images) > 1:
        match.show_match_image(Images[0], Images[1])

    # Compute homography
    Transform = {0: np.identity(3)}
    PointInPano = [PointInImg[0][i].pt for i in range(len(PointInImg[0]))]
    DescriptorInPano = Descriptor[0]
    for idx in range(1, len(imgList)):
        print('fitting transformation from ' + str(idx) + ' to pano\t')
        M = SIFTMatcher(DescriptorInPano, Descriptor[idx], THRESHOLD)
        print('matching points:', len(M, ), '\n')

        dst_pts = np.float32([PointInPano[m[0]] for m in M]).reshape(-1, 1, 2)
        src_pts = np.float32([PointInImg[idx][m[1]].pt for m in M]).reshape(-1, 1, 2)

        # H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        H = func.findHomographyRANSAC(src_pts.reshape(-1,2), dst_pts.reshape(-1,2))

        # Remove matched keypoints before appending
        indices = [m[1] for m in M]
        pts = np.delete(PointInImg[idx], indices, axis=0)
        des = np.delete(Descriptor[idx], indices, axis=0)

        # Transform coord. of descriptors to pano space
        pts = np.asarray([pts[i].pt for i in range(len(pts))])
        pts = H.dot(np.concatenate([pts.T, np.ones([1, pts.shape[0]])], axis=0))
        pts = (pts / pts[2])[:2,].T

        # Append points and descriptors
        PointInPano = np.concatenate([PointInPano, pts], axis=0)
        DescriptorInPano = np.concatenate([DescriptorInPano, des], axis=0)

        Transform.update({idx: H})

    # Compute translation
    pano_corners = np.array([[], []])
    for idx in range(len(imgList)):
        # Find new corners
        curImg = Images[idx]
        corners = np.array([
            [0, curImg.shape[1], curImg.shape[1], 0],
            [0, 0, curImg.shape[0], curImg.shape[0]],
            [1, 1, 1, 1]
        ])
        new_corners = Transform[idx].dot(corners)
        pano_corners = np.concatenate([pano_corners, (new_corners/new_corners[2])[:2,]], axis=1)

    # Calculate translation matrix
    T = np.identity(3, np.float)
    T[0, 2] = -pano_corners[0].min()
    T[1, 2] = -pano_corners[1].min()

    # Calculate new image size
    new_size = (int(pano_corners[0].max()-pano_corners[0].min()), int(pano_corners[1].max()-pano_corners[1].min()))

    # Stitch images
    pano = cv2.warpPerspective(Images[0], T, new_size)
    print('Pano size:', pano.shape)
    for idx in range(1, len(imgList)):

        H = Transform[idx]

        # Warp images
        warped_mask = cv2.warpPerspective(Images[idx], T.dot(H), new_size)
        warped = cv2.warpPerspective(Images[idx], T.dot(H), new_size, borderMode=cv2.BORDER_REFLECT)

        # Find mask
        mask = np.sum(warped_mask, axis=2) != 0
        mask = mask.astype(np.float) # bool to 0 1

        # Do multiband blending
        pano = blending.MultibandBlending(pano, warped, mask)

        cv2.imshow('result{}_{}_pano'.format(idx, idx+1), pano)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imwrite(panoFileName, pano)


if __name__ == '__main__':
    main()