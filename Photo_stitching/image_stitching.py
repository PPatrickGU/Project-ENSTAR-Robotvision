#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import cv2
from matplotlib import pyplot as plt
from numba import jit  #acclerate

@jit(nopython=True)
def superposition(cols, img_1, warpImg):
    for col in range(0, cols):
        if img_1[:, col].any() and warpImg[:, col].any():  #left side of the suoverlap
            left = col
            break
    for col in range(cols - 1, 0, -1):
        if img_1[:, col].any() and warpImg[:, col].any():  #right side of the suoverlap
            right = col
            break
    return left, right

def majorization(cols, rows, img_1, warpImg):
    res = np.zeros([rows, cols, 3], np.uint8)
    for row in range(0, rows):
        #print(row)
        for col in range(0, cols):
            if not img_1[row, col].any():  # 如果没有原图，用旋转的填充
                res[row, col] = warpImg[row, col]
            elif not warpImg[row, col].any():
                res[row, col] = img_1[row, col]
            else:
                srcImgLen = float(abs(col - left))
                testImgLen = float(abs(col - right))
                alpha = srcImgLen / (srcImgLen + testImgLen)
                res[row, col] = np.clip(img1[row, col] * (1 - alpha) + warpImg[row, col] * alpha, 0, 255)
    return res


t1 = cv2.getTickCount()
MIN_MATCH_COUNT = 20

img1 = cv2.imread('1.png',0)
img2 = cv2.imread('2.png',0)
img_1 = cv2.imread('1.png')
img_2 = cv2.imread('2.png')

# Resize the pictures to accelerate, cv2.INTER_LINEAR is faster than cv2.INTER_CUBIC)
height1, width1 = img1.shape
img1 = cv2.resize(img1, (int(width1), int(height1)), interpolation=cv2.INTER_LINEAR)#cv2.INTER_CUBIC)
height2, width2 = img2.shape
img2 = cv2.resize(img2, (int(width2), int(height2)), interpolation=cv2.INTER_LINEAR)#cv2.INTER_CUBIC)

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2,k=2)
matchesMask = [[0,0] for i in range(len(matches))]

good = []
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
    if m.distance < 0.7*n.distance:
        good.append(m)

# Core !!!
if len(good) > MIN_MATCH_COUNT:
    # findHomography
    # perspectiveTransform
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    # Matrix of trasnsformation
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h, w = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    warpImg = cv2.warpPerspective(img_2, np.linalg.inv(M), (img_1.shape[1] + img_2.shape[1], img_2.shape[0]))
    direct = warpImg.copy()

    direct[0:img_1.shape[0], 0:img_1.shape[1]] = img_1

    rows, cols = img_1.shape[:2]
    left, right = superposition(cols, img_1, warpImg)


    #res = majorization(cols, rows, img_1, warpImg)

    #warpImg[0:img1.shape[0], 0:img1.shape[1]] = res[:, :, 0]
    #warpImg[0:img1.shape[0], 0:img1.shape[1]] = res
    direct = cv2.cvtColor(direct, cv2.COLOR_RGB2BGR)
    #warpImg = cv2.cvtColor(warpImg, cv2.COLOR_RGB2BGR)

    t2 = cv2.getTickCount()
    time = (t2 - t1) / cv2.getTickFrequency()
    print("Detection time :", time, "s")

    plt.imshow(direct, ), plt.show()
    #plt.imshow(warpImg, ), plt.show()
    direct = cv2.cvtColor(direct, cv2.COLOR_BGR2RGB)
    #warpImg = cv2.cvtColor(warpImg, cv2.COLOR_BGR2RGB)
    cv2.imwrite("simplepanorma1.png",direct)
    #cv2.imwrite("bestpanorma1.png",warpImg)

else:
    print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                   singlePointColor=None,
                   matchesMask=matchesMask,  # draw only inliers
                   flags=2)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

plt.imshow(img3), plt.show()




