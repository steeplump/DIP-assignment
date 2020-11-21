#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:05:11 2020

@author: yywong
"""


import cv2
from matplotlib import pyplot as pt
import pytesseract
from openpyxl import load_workbook
import csv

pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
wb = load_workbook('01_info.xlsx')
sheet = wb.active

image = cv2.imread("01.png", 0)
image_c = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img_data = image_c[1900:2409,0:3153]
img_drawing = image_c[0:1900,0:3153]
cv2.imwrite('drawing_01.png', img_drawing)

"""
pt.figure()
pt.subplot(3,1,1)
pt.imshow(image_c, cmap = "gray")
pt.title("Original Image")

pt.subplot(3,1,2)
pt.imshow(img_data, cmap="gray")
pt.title("Drawing Info")

pt.subplot(3,1,3)
pt.imshow(img_drawing, cmap="gray")
pt.title("Drawing")
"""

data_str = pytesseract.image_to_string(img_data)
data = pytesseract.image_to_data(img_data, output_type=pytesseract.Output.DATAFRAME)
data = data.filter(like='text')
data.to_excel('01_info.xlsx')


"""
#DOESNT WORK
data = pytesseract.image_to_data(img_data, output_type=pytesseract.Output.DICT)
#data = data.filter(like='text')
with open("test.csv", "w", newline="") as csv_file:
    cols = ["amendments","unit","drawing number","drawing title","issue date","changes"]
    writer = csv.DictWriter(csv_file, fieldnames=cols)
    writer.writeheader()
    writer.writerows(data)
"""