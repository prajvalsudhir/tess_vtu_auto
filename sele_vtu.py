from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PIL import Image
from PIL import ImageFilter
import pytesseract
import cv2
import csv
import time



cdriver = "C:\\Users\\prajv\\Downloads\\chromedriver_win32\\chromedriver"
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
print(cdriver)

#
driver = webdriver.Chrome(cdriver)


driver.get("https://results.vtu.ac.in/_CBCS/index.php")


final_csv = []
field_names = ["Student Name", "Student USN"]



# find = driver.find_elements_by_xpath('//*[(@id = "raj")]//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-12", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "form-control", " " ))]')
# for i in range(len(find)):
#      find[i].send_keys("1rn18is001")


def captcha():
    # driver.get("https://results.vtu.ac.in/_CBCS/index.php")
    driver.save_screenshot("screen_vtu.png")

    with Image.open("screen_vtu.png") as shot:
        w, h = shot.size
        # box = (670,500,880,530)
        # box = (350,400,1000,600)  #(left,upper,right,lower) specifies the pixels to be cut(increase left and upper values and decrease right and lower values  to get an idea)
        box = (670, 460, 855, 570)
        cshot = shot.crop(box)
        cshot.convert('L').filter(ImageFilter.DETAIL).save("crop_vtu.jpg")
        shot.convert('L').filter(ImageFilter.DETAIL).save("screen_vtu.png")

    # img = Image.open("crop_vtu.png")
    #
    #### CAPTCHA IMAGE CLEANING ####

    cropped_image = Image.open("crop_vtu.jpg")
    newsize = (525, 250)
    cropped_image = cropped_image.resize(newsize, resample=Image.ANTIALIAS)
    pixel_matrix = cropped_image.load()
    for col in range(0, cropped_image.height):
        for row in range(0, cropped_image.width):
            # print(pixel_matrix[row, col])
            if pixel_matrix[row, col] > 136:
                pixel_matrix[row, col] = 255  # where 255 = white pixel and 0 = pure black pixel
            else:
                pixel_matrix[row, col] = 0

    for column in range(1, cropped_image.height - 1):
        for row in range(1, cropped_image.width - 1):
            if pixel_matrix[row, column] == 0 \
                    and pixel_matrix[row, column - 2.7] == 255 and pixel_matrix[row, column + 2.7] == 255:
                pixel_matrix[row, column] = 255
            if pixel_matrix[row, column] == 0 \
                    and pixel_matrix[row - 2.3, column] == 255 and pixel_matrix[row + 2.3, column] == 255:
                pixel_matrix[row, column] = 255

    cropped_image.save('thresholded_image.png')
    img3 = cv2.imread('thresholded_image.png', 0)
    img3 = cv2.medianBlur(img3, 5)
    # img3 = cv2.medianBlur(img3,5)
    # img3 = cv2.GaussianBlur(img3,(5,5),0)
    # img3 = cv2.adaptiveThreshold(img3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                              cv2.THRESH_BINARY,11,2)
    cv2.imwrite('out_img3.jpg', img3)
    cv2.waitKey(0)

    tess = pytesseract.image_to_string(cv2.imread('out_img3.jpg'))
    res = ''

    for i in range(len(tess)):
        if tess[i].isalnum():
            res += tess[i]

    # print(tess)
    print(res)
    return res


# #

with open('pp.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader)
    for row in reader:
      minor_field_name = ["Student Name", "Student USN", "Subject Code", "Subject Name", "Internal Marks",
                            "External Marks", "Total", "Result"]

      result = {}
      minor_final_result = []
      flag = 0
      while flag!=1:
          try:
              usn = row['usn']
              find = driver.find_elements_by_xpath('//*[@id="raj"]/div[1]/div/input')
              for i in range(len(find)):
                  find[i].send_keys(usn)

              time.sleep(1)

              find1 = driver.find_elements_by_xpath('//*[@id="raj"]/div[2]/div[1]/input')
              for i in range(len(find1)):
                  find1[i].send_keys(captcha())

              find2 = driver.find_elements_by_xpath('//*[@id="submit"]')
              for i in range(len(find2)):
                  find2[i].click()

              if(driver.find_elements_by_xpath('//*[@id="dataPrint"]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div')):
                  flag =1
                  # excel_auto.auto_map()
                  # print(excel_auto.minor_final_result)
                  # excel_auto.auto_write()

                  student_deatils_table = driver.find_element_by_xpath("//table[1]")
                  result["Student Name"] = student_deatils_table.find_elements_by_tag_name("td")[3].text[2:]
                  result["Student USN"] = usn

                  final_result_table = driver.find_elements_by_tag_name("table")[1]
                  # result["Total Marks"] = final_result_table.find_elements_by_tag_name("td")[1].text[2:]
                  # result["Result"] = final_result_table.find_elements_by_tag_name("td")[3].text[2:]

                  marks_table = driver.find_elements_by_class_name("divTable")[0]
                  for cell in marks_table.find_elements_by_class_name("divTableRow")[1:]:
                      minor_result = {}
                      minor_result["Student Name"] = student_deatils_table.find_elements_by_tag_name("td")[3].text[2:]
                      minor_result["Student USN"] = usn
                      # minor_result["Overall Marks"] = final_result_table.find_elements_by_tag_name("td")[1].text[2:]
                      # minor_result["Overall Result"] = final_result_table.find_elements_by_tag_name("td")[3].text[2:]

                      minor_result["Subject Code"] = cell.find_elements_by_class_name("divTableCell")[0].text
                      minor_result["Subject Name"] = cell.find_elements_by_class_name("divTableCell")[1].text
                      # print ("minor result = " + str(minor_result))
                      if cell.find_elements_by_class_name("divTableCell")[0].text not in field_names:
                          if cell.find_elements_by_class_name("divTableCell")[
                              0].text + " Internal Marks" not in field_names:
                              field_names.append(
                                  cell.find_elements_by_class_name("divTableCell")[0].text + " Internal Marks")
                          if cell.find_elements_by_class_name("divTableCell")[
                              0].text + " External Marks" not in field_names:
                              field_names.append(
                                  cell.find_elements_by_class_name("divTableCell")[0].text + " External Marks")
                          if cell.find_elements_by_class_name("divTableCell")[0].text + " Total" not in field_names:
                              field_names.append(cell.find_elements_by_class_name("divTableCell")[0].text + " Total")
                          if cell.find_elements_by_class_name("divTableCell")[0].text + " Result" not in field_names:
                              field_names.append(cell.find_elements_by_class_name("divTableCell")[0].text + " Result")

                      result[cell.find_elements_by_class_name("divTableCell")[0].text + " Internal Marks"] = \
                      cell.find_elements_by_class_name("divTableCell")[2].text
                      minor_result["Internal Marks"] = cell.find_elements_by_class_name("divTableCell")[2].text
                      result[cell.find_elements_by_class_name("divTableCell")[0].text + " External Marks"] = \
                      cell.find_elements_by_class_name("divTableCell")[3].text
                      minor_result["External Marks"] = cell.find_elements_by_class_name("divTableCell")[3].text
                      result[cell.find_elements_by_class_name("divTableCell")[0].text + " Total"] = \
                      cell.find_elements_by_class_name("divTableCell")[4].text
                      minor_result["Total Marks"] = cell.find_elements_by_class_name("divTableCell")[4].text
                      result[cell.find_elements_by_class_name("divTableCell")[0].text + " Result"] = \
                      cell.find_elements_by_class_name("divTableCell")[5].text
                      minor_result["Result"] = cell.find_elements_by_class_name("divTableCell")[5].text

                      minor_final_result.append(minor_result)
                  driver.get("https://results.vtu.ac.in/_CBCS/index.php")
          except:
              continue

      final_csv.append(result)
    print(final_csv)


with open('vtu_excel.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for row in final_csv:
            writer.writerow(row)






#
#
# driver.get("https://results.vtu.ac.in/_CBCS/index.php")
# find1 = driver.find_elements_by_xpath('//*[@id="raj"]/div[2]/div[1]/input')
# for i in range(len(find1)):
#     find1[i].send_keys(res)
#
# find2 = driver.find_elements_by_xpath('//*[@id="submit"]')
# for i in range(len(find2)):
#     find2[i].click()
#
# driver.switch_to.alert.accept()




# driver.close()

