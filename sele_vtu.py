from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
from PIL import ImageFilter
import pytesseract
import cv2




cdriver = "C:\\Users\\prajv\\Desktop\\PycharmProjects\\PS-PY\\venv\\tess_vtu_auto\\chromedriver_win32\\chromedriver"
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\prajv\\Desktop\\PycharmProjects\\PS-PY\\venv\\tess_vtu_auto\\Tesseract-OCR\\tesseract.exe'
print(cdriver)

#
# driver = webdriver.Chrome(cdriver)


# driver.get("http:www.amazon.in")
# find = driver.find_elements_by_xpath('//*[@id="twotabsearchtextbox"]')
# for i in range(len(find)):
#     find[i].send_keys("laptops",Keys.ENTER)



# driver.get("https://results.vtu.ac.in/vitavicbcsjj19/index.php")
# find = driver.find_elements_by_xpath('//*[(@id = "raj")]//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-12", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "form-control", " " ))]')
# for i in range(len(find)):
#      find[i].send_keys("1rn18is001")

# driver.save_screenshot("screen_vtu.png")

with Image.open("screen_vtu.png") as shot:
    w,h = shot.size
    # box = (670,500,880,530)
    # box = (350,400,1000,600)  #(left,upper,right,lower) specifies the pixels to be cut(increase left and upper values and decrease right and lower values  to get an idea)
    box = (670,500,880,530)
    cshot = shot.crop(box)
    cshot.convert('L').filter(ImageFilter.DETAIL).save("crop_vtu.jpg")
    shot.convert('L').filter(ImageFilter.DETAIL).save("screen_vtu.png")

# img = Image.open("crop_vtu.png")
#

img = cv2.imread('screen_vtu.png')




# img3 = cv2.imread('crop_vtu2.jpg',0)
# img3 = cv2.resize(img3,(640,300),interpolation=cv2.INTER_LINEAR)
# # img3 = cv2.medianBlur(img3,5)
# img3 = cv2.GaussianBlur(img3,(5,5),0)
# img3 = cv2.adaptiveThreshold(img3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                              cv2.THRESH_BINARY,11,2)
# # img3 = cv2.threshold(img3,127,255,cv2.THRESH_BINARY,11)
# cv2.imwrite('out_img3.jpg',img3)
# cv2.waitKey(0)

# img3 = Image.open('crop_vtu2.jpg')
# newsize = (300,100)
# img3 = img3.resize(newsize,resample=Image.LANCZOS)
# img3.show()


#### CAPTCHA IMAGE CLEANING ####

cropped_image = Image.open("out_img.jpg")
newsize = (500,100)
cropped_image = cropped_image.resize(newsize,resample=Image.ANTIALIAS)
pixel_matrix = cropped_image.load()
for col in range(0, cropped_image.height):
    for row in range(0, cropped_image.width):
        # print(pixel_matrix[row, col])
        if pixel_matrix[row, col] > 132:
            pixel_matrix[row, col] = 255   # where 255 = white pixel and 0 = pure black pixel
        else:
            pixel_matrix[row,col] = 0

for column in range(1, cropped_image.height - 1):
    for row in range(1, cropped_image.width - 1):
        if pixel_matrix[row, column] == 0 \
            and pixel_matrix[row, column - 2] == 255 and pixel_matrix[row, column + 2] == 255 :
            pixel_matrix[row, column] = 255
        if pixel_matrix[row, column] == 0 \
            and pixel_matrix[row - 2, column] == 255 and pixel_matrix[row + 2, column] == 255:
            pixel_matrix[row, column] = 255

cropped_image.save('thresholded_image.png')


img3 = cv2.imread('thresholded_image.png',0)
img3 = cv2.medianBlur(img3,5)
# img3 = cv2.GaussianBlur(img3,(5,5),0)
img3 = cv2.adaptiveThreshold(img3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY,11,2)
cv2.imwrite('out_img3.jpg',img3)
cv2.waitKey(0)






tess = pytesseract.image_to_string(cv2.imread('out_img3.jpg'))

print(tess)
# #
# driver.get("https://results.vtu.ac.in/vitavicbcsjj19/index.php")
# find1 = driver.find_elements_by_xpath('//*[@id="raj"]/div[1]/div[2]/input')
# for i in range(len(find1)):
#      find1[i].send_keys(tess)


# driver.get("https://results.vtu.ac.in/vitavicbcsjj19/index.php")
# find = driver.find_elements_by_xpath('//*[(@id = "raj")]//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-12", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "form-control", " " ))]')
# for i in range(len(find)):
#      find[i].send_keys("1rn18is001")



# find2 = driver.find_elements_by_xpath('//*[@id="submit"]')
# for i in range(len(find2)):
#     find2[i].click()
#
#
# driver.get("https://results.vtu.ac.in/vitavicbcsjj19/index.php")
# find1 = driver.find_elements_by_xpath('//*[@id="raj"]/div[1]/div[2]/input')
# find1 = driver.find_elements_by_xpath('//*[@id="raj"]/div[1]/div[2]/input')
# for i in range(len(find1)):
#      find1[i].send_keys(tess)





# driver.close()

