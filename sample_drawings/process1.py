#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 00:27:11 2020

@author: yywong
"""

#FOR DRAWING INFO WITH NO INTERNAL TABLE LINES
#DRAWING: 08.png

import cv2
import numpy as np
from matplotlib import pyplot as pt
import pytesseract
from pytesseract import Output
import re
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

#Read image
img = cv2.imread("08.png", 0)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#Binarise image with the pre-defined threshold 
thresh = 128
img_bin = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

#Rotate image so that table line is horizontal
rotated = cv2.rotate(img_bin, cv2.ROTATE_90_CLOCKWISE)

#Plot histogram to find table
counts = np.sum(rotated==0, axis=1)
#pt.plot(counts)
#pt.figure()
#pt.imshow(img_bin, cmap="gray")

#Extract drawing and save as new image 

drawing = img_bin[0:2409,800:3163]
cv2.imwrite("drawing_08.png", drawing)

#Extract table for processing
table = img_bin[0:2409,0:800]
#pt.imshow(table, cmap="gray")

#Extract table data to dataframe 
data = pytesseract.image_to_data(table, output_type=Output.DICT)
data_df = pytesseract.image_to_data(table, output_type=Output.DATAFRAME)
keys = list(data.keys())

#Find location of NUMBER text using pattern matching
#x: distance of upper left corner of bounding box to left border of image
#y: distance of upper left corner of bounding box to top border of image
#w: width of bounding box
#h: height of bounding box
dnumber = 'NUMBER:'
n_boxes = len(data['text'])
for i in range(n_boxes):
    if int(data['conf'][i]) > 60:
    	if re.match(dnumber, data['text'][i]):
	        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
	        dnumber_loc = cv2.rectangle(table, (x, y), (x + w, y + h), (0, 255, 0), 2)          
#pt.imshow(dnumber_loc, cmap="gray")

''' DOESN'T WORK
#Find value of drawing number using pattern matching
dn_value = '^([a-zA-Z0-9]|[a-zA-Z0-9])-([a-zA-Z0-9]|[a-zA-Z0-9]|[a-zA-Z0-9])-([a-zA-Z0-9])-([a-zA-Z0-9]|[a-zA-Z0-9])-([a-zA-Z0-9]|[a-zA-Z0-9])-([a-zA-Z0-9]|[a-zA-Z0-9])-([a-zA-Z0-9]|[a-zA-Z0-9])-([a-zA-Z0-9])$'
n_boxes = len(data['text'])
for i in range(n_boxes):
    if int(data['conf'][i]) > 60:
    	if re.match(dn_value, data['text'][i]):
	        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
	        dn_value_loc = cv2.rectangle(table, (x, y), (x + w, y + h), (0, 255, 0), 2)
'''

n_boxes1 = len(data['text'])
for i in range(n_boxes1):
    if int(data['conf'][i]) > 60:
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        table = cv2.rectangle(table, (x, y), (x + w, y + h), (0, 255, 0), 2)

#Find location of drawing number value (???)
n_boxes1 = len(data['text'])
for i in range(n_boxes1):
    if int(data['conf'][i]) > 60:
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        
''' DOESN'T WORK
#dilation
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
dilation = cv2.dilate(table, kernel, iterations = 1)
#pt.imshow(dilation,cmap = 'gray')
'''

df_dnumber = data_df['text']=="NUMBER:"
dnum_row = data_df[df_dnumber]
(x, y, w, h) = (dnum_row['left'], dnum_row['top'], dnum_row['width'], dnum_row['height'])
topLeft = (x,y)
#bottomLeft = 
