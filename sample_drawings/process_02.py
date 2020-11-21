#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 23:54:47 2020

@author: yywong
"""

import cv2
from matplotlib import pyplot as pt
import pytesseract 
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

img = cv2.imread("02.png",0)
img_c = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_data = img_c[1950:2400,0:3153]
img_drawing = img_c[0:1950,0:3153]

pt.figure()
pt.subplot(3,1,1)
pt.imshow(img_data, cmap="gray")

pt.subplot(3,1,2)
pt.imshow(img_drawing, cmap="gray")

pt.subplot(3,1,3)
pt.imshow(img_c, cmap="gray")



d = pytesseract.image_to_data(img_data, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(img_data, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    