from selenium import webdriver
from pathlib import Path

cdriver = "C:\\Users\\prajv\\Downloads\\chromedriver_win32\\chromedriver"
print(cdriver)

driver = webdriver.Chrome(cdriver)


def search(n):
    save = open('sem_res.txt', 'w')
    for i in range(70,n+1,1):

            driver.get("http:www.vtu4u.com/result/1rn18is0{}/sem-2/rs-22?cbse=1".format(i))
            path = '//*[contains(concat( " ", @class, " " ), concat( " ", "student_details", " " ))]'
            stud_info = driver.find_elements_by_xpath(path)
            for i in range(len(stud_info)):
                print(stud_info[i].text)
                save.write(stud_info[i].text)
            save.write("\n")

            res_info = driver.find_elements_by_xpath("//*[@id='wrap']/div[2]/div[1]/div[2]/div[1]/div[3]/div[3]/div[2]")
            print(res_info)
            for i in range(len(res_info)):
                print(res_info[i].text)
                save.write(res_info[i].text)
            save.write("\n")

            marks_info = driver.find_elements_by_xpath(
                "//*[@id='wrap']/div[2]/div[1]/div[2]/div[1]/div[3]/div[3]/table")
            for j in range(len(marks_info)):
                print(marks_info[j].text)
                save.write(marks_info[j].text)
            save.write("\n")
    save.close()






if __name__ == '__main__':

    search(80)
