import cv2
import numpy as np

MIN_MATCH_COUNT = 10

def show_match_image(img1, img2):
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:

          good.append(m)
    # cv2.drawMatchesKnn expects list of lists as matches.
    good_2 = np.expand_dims(good, 1)
    matching = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good_2[:20],None, flags=2)

    if len(good)>MIN_MATCH_COUNT:
        # 獲取關鍵點的坐標
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,5.0)
        wrap = cv2.warpPerspective(img2, H, (img2.shape[1]+img2.shape[1] , img2.shape[0]+img2.shape[0]))
        # result = cv2.addWeighted(img1, 0.5, wrap, 0.5, 0)
        wrap[0:img2.shape[0], 0:img2.shape[1]] = img1

        # rows, cols = np.where(wrap[:,:,0] !=0)
        # min_row, max_row = min(rows), max(rows) +1
        # min_col, max_col = min(cols), max(cols) +1
        # result = wrap[min_row:max_row,min_col:max_col,:]#去除黑色無用部分
        result = wrap

        cv2.imshow('Match Result', matching)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return matching, result

if __name__ == '__main__':
    img1 = cv2.imread('data/Rainier1.png')  # queryImage
    img2 = cv2.imread('data/Rainier3.png')  # trainImage
    matching, result = show_match_image(img1, img2)