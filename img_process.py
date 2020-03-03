from PIL import Image
from PIL import ImageFilter
import pytesseract
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd =  os.path.abspath(os.path.join(os.path.dirname(__file__),"Tesseract-OCR\\tesseract.exe"))

cropped_image = Image.open("crop_vtu.jpg")
newsize = (525, 250)
cropped_image = cropped_image.resize(newsize, resample=Image.ANTIALIAS)
pixel_matrix = cropped_image.load()
for col in range(0, cropped_image.height):
    for row in range(0, cropped_image.width):
        # print(pixel_matrix[row, col])
        if pixel_matrix[row, col] > 150:
            pixel_matrix[row, col] = 255  # where 255 = white pixel and 0 = pure black pixel
        else:
            pixel_matrix[row, col] = 0

for column in range(0, cropped_image.height - 1):
    for row in range(0, cropped_image.width - 1):
        if pixel_matrix[row, column] == 0 \
                and pixel_matrix[row, column - 1.9] == 255 and pixel_matrix[row, column + 1.9] == 255:
            pixel_matrix[row, column] = 255
        if pixel_matrix[row, column] == 0 \
                and pixel_matrix[row - 3.2, column] == 255 and pixel_matrix[row + 3.2, column] == 255:
            pixel_matrix[row, column] = 255

cropped_image.save('thresholded_image2.png')
img3 = cv2.imread('thresholded_image2.png', 0)
img3 = cv2.medianBlur(img3, 5)
img3 = cv2.medianBlur(img3, 5)
img3 = cv2.threshold(img3,0,255,cv2.THRESH_OTSU)
# img3 = cv2.GaussianBlur(img3,(5,5),0)
# img3 = cv2.adaptiveThreshold(img3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                              cv2.THRESH_BINARY,11,2)
cv2.imwrite('out_img4.jpg', img3[1])
cv2.waitKey(0)



# img4 = cv2.imread('crop_vtu.jpg', 0)
# img4 = cv2.resize(img4,(700,250))
# img4 = cv2.threshold(img4, 0, 255, cv2.THRESH_OTSU)
# # cv2.imshow('output',img4[1])
# cv2.imwrite('out_img4.jpg',img4[1])
# cv2.waitKey(0)




tess = pytesseract.image_to_string(cv2.imread('out_img4.jpg'))
print(tess)
# print(os.path.abspath(os.path.join('tess_vtu_auto\\chromedriver_win32\\chromedriver')))