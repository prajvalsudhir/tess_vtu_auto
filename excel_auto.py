from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
import csv



cdriver = "C:\\Users\\prajv\\Desktop\\PycharmProjects\\PS-PY\\venv\\tess_vtu_auto\\chromedriver_win32\\chromedriver"
print(cdriver)
driver = webdriver.Chrome(cdriver)


with open('pp.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader)
    for row in reader:
        usn = row['usn']
        driver.get("http:www.google.com")
        search = driver.find_elements_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        for i in range(len(search)):
            search[i].send_keys(usn, Keys.ENTER)


