import numpy as np
from sympy import *



def findHomography(srcPoints, dstPoints):

    b = np.zeros(8, np.float)
    A = np.zeros((8, 8), np.float)
    for j in range(4):
        A[j * 2] = [srcPoints[j][0], srcPoints[j][1], 1, 0, 0, 0, -srcPoints[j][0] * dstPoints[j][0],
                       -dstPoints[j][0] * srcPoints[j][1]]
        b[j * 2] = dstPoints[j][0]
        A[j * 2 + 1] = [ 0, 0, 0, srcPoints[j][0], srcPoints[j][1], 1, -srcPoints[j][0] * dstPoints[j][1]
                           , -dstPoints[j][1] * srcPoints[j][1]]
        b[j * 2 + 1] = dstPoints[j][1]
    b = b.T

    try:
        H = np.linalg.solve(A, b)  # 求解Homography係數
    except np.linalg.LinAlgError:
        return None
    H = np.concatenate([H,[1]]).reshape((3,3))
    return H


def findHomographyRANSAC(srcPoints, dstPoints):

    ITER_NUM = 500
    bestH = None
    bestErr = np.inf

    for x in range(ITER_NUM):
        maybe_idxs, test_idxs = random_partition(4, len(srcPoints))
        H = findHomography(srcPoints[maybe_idxs], dstPoints[maybe_idxs])
        if H is None:
            continue
        testErr = np.mean(computeError(H, srcPoints[test_idxs], dstPoints[test_idxs]))
        if testErr < bestErr:
            bestH = H
            bestErr = testErr

    return bestH


def computeError(H, pt1, pt2):
    match_pt2 = pt2.T
    transformed_pt1 = H.dot(np.concatenate([pt1.T, np.ones([1, pt1.shape[0]])], axis=0))
    transformed_pt1 = (transformed_pt1 / transformed_pt1[2])[:2,]
    dists = np.linalg.norm((transformed_pt1 - match_pt2), axis=0).T
    return dists


def random_partition(k, pts_size):
    all_idxs = np.arange(pts_size)
    np.random.shuffle(all_idxs)
    idxs1 = all_idxs[:k]
    idxs2 = all_idxs[k:]
    return idxs1, idxs2


if __name__ == '__main__':
    srcPoints = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1]
    ])

    dstPints = np.array([
        [2, 1],
        [4, 1],
        [3, 2],
        [2, 2]
    ])

    print(findHomography(srcPoints, dstPints))
