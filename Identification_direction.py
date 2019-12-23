#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Step 0: transform
# Step 1: find the red triangle
# Step 2: find the correct circle nearest of the red triangle (through the ratio between the triangle and the circle)
# Step 3: analyse the direction (By gray value, the larger the gray value, the lighter the color) (modes or means)
# Problem: the sign in the picture may be an ellipse instead of a circle, so it's better to detect an ellipse.


import cv2
import numpy as np
import matplotlib.pyplot as plt

# Step 0: transform
image = cv2.imread('2.png')
image2 = cv2.imread('2.png')

hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# transform RGB into HSV which is easier to identify the color

# find intersection point of two lines
def FindIntersectionPoint(slope1, intercept1, judge1, slope2, intercept2, judge2):
    if judge1 == 0 and judge2 == 1:   #the first line is vertical
        x = slope1
        y = slope2 * x + intercept2
    elif judge1 == 1 and judge2 == 0:   #the second line is vertical
        x = slope2
        y = slope1 * x + intercept1
    elif judge1 == 0 and judge2 == 0:  # both lines are vertical
        x = 0
        y = 0
    else:   #the slops of both lines exist
        x = int((intercept2 - intercept1) / (slope1 - slope2))
        y = int(slope1 * x + intercept1)
    return x,y

def Distance(point1, point2):
    distance = ((point1[1] - point2[1]) ** 2 + (point1[0] - point2[0]) ** 2) ** 0.5
    return distance

# Step 1: find the red triangle
# 1) red region
low_range = np.array([0, 123, 100])
high_range = np.array([5, 255, 255])
th = cv2.inRange(hue_image, low_range, high_range)
# range of red color in HSV
# All the points in the image whose color is out of the range is converted to black, and the others white.
# So we get a grayscale picture.

# 2) find the triangle in the grayscale picture
# get the edge of triangle

edges = cv2.Canny(th, 50, 250)
lines = cv2.HoughLines(edges, 1, np.pi/180, 50)
#Here 50 is the threshold that we need change (it depends on the size of the red triangle)
lines1 = lines[:,0,:]

slope = []
intercept = []
judge = []

for rho, theta in lines1:
    #print('tho theta',rho,theta)
    a = np.cos(theta)
    b = np.sin(theta)
    # we konw that x0 = rho x cos(theta)
    #              y0 = rho x sin(theta)
    x0 = a*rho
    y0 = b*rho
    # Transformation from parameter space to actual coordinate points
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*a)
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*a)
    #print(x1,x2,y1,y2)

    #print (theta)
    if theta == np.pi or theta == 0:
        judge.append(0)
        slope.append(x0)
        intercept.append(y0)
    else:
        judge.append(1)
        slope.append(-a/b)
        intercept.append(y0 + a/b * x0)
    #   slope.append((y2-y1)/(x2-x1))
    #   intercept.append(y1-(y2-y1)/(x2-x1)*x1)
    cv2.line(th, (x1, y1), (x2, y2), (255, 255, 255), 1)

last1 = FindIntersectionPoint(slope[0], intercept[0], judge[0], slope[1], intercept[1], judge[1])
last2 = FindIntersectionPoint(slope[1], intercept[1], judge[1], slope[2], intercept[2], judge[2])
last3 = FindIntersectionPoint(slope[0], intercept[0], judge[0], slope[2], intercept[2], judge[2])
# the triangular vertex
d1 = Distance(last1, last2)
d2 = Distance(last2, last3)
d3 = Distance(last1, last3)
length = 1/3*(d1 + d2 + d3)
#length of triangle
center = [1/3*(last1[0] + last2[0] + last3[0]), 1/3*(last1[1] + last2[1] + last3[1])]
#center of the triangle

#print (last1, last2, last3)

cv2.circle(th, last1, 10, (255, 0, 0))
cv2.circle(th, last2, 10, (255, 0, 0))
cv2.circle(th, last3, 10, (255, 0, 0))

# Step 2: find the correct circle of the red trinangle (through the ratio between the triangle and the circle)

gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=220, param2=30, minRadius=int(3*length), maxRadius=int(10*length))
if circles is not None:
    #print(circles)
    mindistance = 2000 # minimum distance between the centre of the triangle and the circle center
    n = -1
    for i in circles[0,:]:
        #print(i[0], i[1], i[2])
        #(i[0],i[1]) the circle center, i[2] teh radius
        if Distance([i[0],i[1]], center) < mindistance:
            mindistance = Distance([i[0],i[1]], center)
            n = n + 1
    #print(n, mindistance, circles[0,:][n][1])
    circle_center = (circles[0,:][n][0], circles[0,:][n][1])
    circle_radius = circles[0,:][n][2]
    cv2.circle(image2, circle_center, circle_radius, (0, 255, 0), 2)
    #cv2.circle(image2, (500, 0), circle_radius, (0, 255, 0), 2)
    cv2.circle(image2, circle_center, 2, (0, 0, 255), 3)



# Step 3: analyse the direction (By gray value, the larger the gray value, the lighter the color)
colone, line = gray.shape
# gray_value_up = 0
# gray_value_down = 0
# counter_up = 0
# counter_down = 0


gray_value_up = []
gray_value_down = []
counter_up = 0
counter_down = 0

for n in range(int(circle_center[1] - circle_radius-1), int(circle_center[1] + circle_radius )):
    for m in range(int(circle_center[0] - circle_radius-1), int(circle_center[0]+circle_radius )):
        if Distance([m,n], circle_center) < circle_radius and n < circle_center[1] and gray[m,:][n-1] != 255:
            gray_value_up.append(gray[m,:][n-1])
            #counter_up = counter_up + 1
        elif Distance([m,n], circle_center) < circle_radius and n > circle_center[1] and gray[m,:][n-1] != 255:
            gray_value_down.append( gray[m,:][n-1])
            # counter_down = counter_down + 1
average_gray_value_up = np.mean(gray_value_up)
average_gray_value_down = np.mean(gray_value_down)
print(average_gray_value_up, average_gray_value_down)

if average_gray_value_up < average_gray_value_down:
    print('Direction : N')
else:
    print('Direction : S')
#
#
# # the method of compare the average gray values is not correct, so we turn to comparing the modes
# gray_value_up = []
# gray_value_down = []
# counter_up = 0
# counter_down = 0
# for n in range(int(circle_center[1] - circle_radius-1), int(circle_center[1] + circle_radius )):
#     for m in range(int(circle_center[0] - circle_radius-1), int(circle_center[0]+circle_radius )):
#         if Distance([m,n], circle_center) < circle_radius and n < circle_center[1] and gray[m,:][n-1] != 255:
#             gray_value_up.append(gray[m,:][n-1])
#             counter_up = counter_up + 1
#         elif Distance([m,n], circle_center) < circle_radius and n > circle_center[1] and gray[m,:][n-1] != 255:
#             gray_value_down.append( gray[m,:][n-1])
#             counter_down = counter_down + 1
# counts1 = np.bincount(gray_value_up)
# counts2 = np.bincount(gray_value_down)
#
# mode_gray_value_up = np.argmax(counts1)
# mode_gray_value_down = np.argmax(counts2)
#
#
# print(mode_gray_value_up, mode_gray_value_down, counter_up, counter_down)
#
# if mode_gray_value_up < mode_gray_value_down:
#     print('N')
# else:
#     print('S')


cv2.imshow("Processing procedure 1", th)
cv2.imshow("Processing procedure 2", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()