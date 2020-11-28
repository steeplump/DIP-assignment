#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 11:46:05 2020

@author: yywong
"""

import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import pytesseract
import openpyxl

pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

img_path = '01.png'

img = cv2.imread(img_path, 0)
img.shape

plt.imshow(img, cmap="gray")


# plot histogram to find number of black pixels in each column
v_counts = np.sum(img==0, axis=1)
# plot the histogram to check the location of the table's vertical lines
#plt.plot(v_counts)

# histogram to find number of black pixels in each row
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
h_counts = np.sum(rotated==0, axis=1)
# plot the histogram to check the location of the table's horizontal lines
#plt.plot(h_counts)

# extract the drawing from the image and save in new .png file
# different methods defined for different layout of image

# horizontal table at the bottom of image
# image no. 1, 2, 3
option = img_path
if option == '01.png' or option == '02.png' or option == '03.png':
    img_drawing = img[0:1900,0:3153]
    cv2.imwrite('drawing_only.png', img_drawing)
# vertical table at right side of image
# image no. 4,5,6,7
elif option == '04.png' or option == '05.png' or option == '06.png' or option == '07.png':
    img_drawing = img[0:2400,0:2400]
    cv2.imwrite('drawing_only.png', img_drawing)
#vertical table at left side of image
# image no. 8,9,10,11
elif option == '08.png' or option == '09.png' or option == '10.png' or option == '11.png':
    img_drawing = img[0:3153,810:3158]
    cv2.imwrite('drawing_only.png', img_drawing)
# L shape table at bottom right
# image no. 12,13,14,15,16,17,18
elif option == '12.png' or option == '13.png' or option == '14.png' or option == '15.png' or option == '16.png' or option == '17.png' or option == '18.png':
    img_drawing = img[0:1727,0:2360]
    cv2.imwrite('drawing_only.png', img_drawing)
# separated table at bottom of image
# image no. 19,20
elif option == '19.png' or option == '20.png':
    img_drawing = img[0:1500,0:3153]
    cv2.imwrite('drawing_only.png', img_drawing)
    

# convert image to binary/binarise using predefined threshold value of 128
thresh, img_bin = cv2.threshold(
    img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# invert the binarised image
img_bin = 255-img_bin
# plot image
plotting = plt.imshow(img_bin, cmap='gray')
plt.show()

# countcol(width) of kernel as 100th of total width
kernel_len = np.array(img).shape[1]//100
# create vertical kernel to detect vertical lines
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
# create horizontal kernel to detect horizontal lines
hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
# kernel with size 2x2
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# use the vertical kernel to save the vertical lines in a jpg
image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
# Plot the generated image
plotting = plt.imshow(image_1, cmap='gray')
plt.show()

# use the horizontal kernel to save the horizontal lines in a jpg
image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
# plot the image
plotting = plt.imshow(image_2, cmap='gray')
plt.show()

# merge horizontal and vertical lines in a new image
img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
# eroding and thesholding 
img_vh = cv2.erode(~img_vh, kernel, iterations=2)
thresh, img_vh = cv2.threshold(
    img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
bitxor = cv2.bitwise_xor(img, img_vh)
bitnot = cv2.bitwise_not(bitxor)
# plot the image
plotting = plt.imshow(bitnot, cmap='gray')
plt.show()

# find contours for box detection
contours, hierarchy = cv2.findContours(
    img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)

# sort the countours
contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")
# make list of height of all the boxes
heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
# calculate mean
mean = np.mean(heights)

# list box to store the boxes
box = []
# get position (x,y), width and height for every contour and show on the image
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if (w < 1000 and h < 500):
        image = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        box.append([x, y, w, h])

plotting = plt.imshow(image, cmap='gray')
plt.show()

# make two lists to define row and column where cell is located
row = []
column = []
j = 0

# sort the boxes to their respective row and column
for i in range(len(box)):

    if(i == 0):
        column.append(box[i])
        previous = box[i]

    else:
        if(box[i][1] <= previous[1]+mean/2):
            column.append(box[i])
            previous = box[i]

            if(i == len(box)-1):
                row.append(column)

        else:
            row.append(column)
            column = []
            previous = box[i]
            column.append(box[i])

print(column)
print(row)

# count max number of cells
countcol = 0
for i in range(len(row)):
    countcol = len(row[i])
    if countcol > countcol:
        countcol = countcol

# find center of each column
center = [int(row[i][j][0]+row[i][j][2]/2)
          for j in range(len(row[i])) if row[0]]

center = np.array(center)
center.sort()
print(center)


# arrange boxes by distance to the center of the column
finalboxes = []
for i in range(len(row)):
    lis = []
    for k in range(countcol):
        lis.append([])
    for j in range(len(row[i])):
        diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
        minimum = min(diff)
        indexing = list(diff).index(minimum)
        lis[indexing].append(row[i][j])
    finalboxes.append(lis)


# extract via pytesseract and put in a list
outer = []
for i in range(len(finalboxes)):
    for j in range(len(finalboxes[i])):
        inner = ''
        if(len(finalboxes[i][j]) == 0):
            outer.append(' ')
        else:
            for k in range(len(finalboxes[i][j])):
                y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], finalboxes[i][j][k][3]
                finalimg = bitnot[x:x+h, y:y+w]
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                border = cv2.copyMakeBorder(
                    finalimg, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255])
                resizing = cv2.resize(border, None, fx=2,
                                      fy=2, interpolation=cv2.INTER_CUBIC)
                dilation = cv2.dilate(resizing, kernel, iterations=1)
                erosion = cv2.erode(dilation, kernel, iterations=2)

                out = pytesseract.image_to_string(erosion)
                if(len(out) == 0):
                    out = pytesseract.image_to_string(
                        erosion, config='--psm 3')
                inner = inner + " " + out
            outer.append(inner)

# make a dataframe of the list
arr = np.array(outer)
dataframe = pd.DataFrame(arr.reshape(len(row), countcol))
print(dataframe)
data = dataframe.style.set_properties(align="left")

# save in excel
data.to_excel("result.xlsx")