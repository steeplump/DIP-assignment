# DIP-assignment

## About

Python script file: `test.py`

Includes methods to extract drawing from image with different layout designs:

* Horizontal drawing info table at the bottom of the image: 01, 02, 03
* Vertical drawing info table on right side of image: 04, 05, 06, 07
* Vertical drawing info table on left side of image: 08, 09, 10, 11
* L-shaped drawing info table at bottom right side of image: 12, 13, 14, 15, 16, 17, 18
* Separated table at bottom right and bottom left side of image: 19, 20

Does not include methods to extract images with different layout designs:

* Drawing info table with no table lines to separate the words (successful): 08
* Drawing info table with table lines (successful): 01, 02, 03, 04, 10, 11, 14, 15, 16, 17, 18, 20
* Drawing info table with table lines and fine inner table lines (not successful): 05, 06, 07, 09, 12, 13, 19

## Output files

* `result.xlsx` - table data is extracted here.
* `drawing_only.png` - drawing is extracted here.

## Notes

* Remember to specify the location of PyTesseract in your machine before running the script file.
* Set the image you want to process via `img_path`.

