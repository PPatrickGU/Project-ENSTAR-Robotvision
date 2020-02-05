#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Step 1: En utilisant la bibliothèque d'ArUco, on obtient la position de la centre de la signe.
# Step 2: Trouver la cercle dont la rayon est correste
# Step 3: Comparer la valeur de gris de la deux semi-cercle (on compare seulent une partie mais pas toute la semi-cercle pour économiser du temps )

import numpy as np
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
from numba import jit

@jit(nopython=True)
def value_up_down(circle_center,circle_radius):
    gray_value_up = []
    gray_value_down = []
    for n in range(int(circle_center[1] - 9*circle_radius/16-1), int(circle_center[1] - 7*circle_radius/16-1 )):
        for m in range(int(circle_center[0] - 9*circle_radius/16-1), int(circle_center[0] - 7*circle_radius/16-1 )):
            gray_value_up.append(gray[n,:][m])
            gray_value_down.append(gray[int(n + circle_radius),:][m])
    return gray_value_up, gray_value_down

t1 = cv2.getTickCount()
img = cv2.imread("1.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()


# Step 1: En utilisant la bibliothèque d'ArUco, on obtient la position de la centre de la signe.
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
parameters = aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
img_markers = aruco.drawDetectedMarkers(img.copy(), corners, ids)


# Step 2: Trouver la cercle dont la rayon est correste (en utilisant le ratio entre le logo ArUco et la rayon de la cercle)
x1 = abs(corners[0][0][0][0]-corners[0][0][1][0])
x2 = abs(corners[0][0][3][0]-corners[0][0][2][0])
y1 = abs(corners[0][0][0][1]-corners[0][0][2][1])
y2 = abs(corners[0][0][1][1]-corners[0][0][3][1])
length = (x1 + x2 + y1 + y2)/4 #la longueur du logo ArUco dans la photo

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=220, param2=30, minRadius=int(2*length), maxRadius=int(6*length))
c = corners[0][0]
#circle_center1 = (circles[0, :][0][0], circles[0, :][0][1])
circle_center = (c[:, 0].mean(), c[:, 1].mean())
circle_radius = circles[0, :][0][2]

cv2.circle(img_markers, circle_center, circle_radius, (0, 255, 0), 2)
#cv2.imshow("ddd", img_markers)

# Step 3: Comparer la valeur de gris de la deux semi-cercle (on compare seulent une partie mais pas toute la semi-cercle pour économiser du temps )
(gray_value_up, gray_value_down) = value_up_down(circle_center,circle_radius)

average_gray_value_up = np.mean(gray_value_up)
average_gray_value_down = np.mean(gray_value_down)

print(average_gray_value_up, average_gray_value_down)

if average_gray_value_up < average_gray_value_down:
    print('Direction : N')
else:
    print('Direction : S')

t2 = cv2.getTickCount()
time = (t2 - t1)/ cv2.getTickFrequency()
print("Detection time :",time,"s")







