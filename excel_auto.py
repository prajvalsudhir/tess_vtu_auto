from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
import csv
import os


# cdriver = "C:\\Users\\prajv\\Downloads\\chromedriver_win32\\chromedriver"
cdriver = os.path.abspath(os.path.join(os.path.dirname(__file__),"chromedriver_win32\\chromedriver"))
print(cdriver)
driver = webdriver.Chrome(cdriver)


field_names = ['SUB-CODE']
final_res = []



with open('pp.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader)
    for row in reader:
        usn = row['usn']
        driver.get("http:www.google.com")
        search = driver.find_elements_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        for i in range(len(search)):
            search[i].send_keys(usn, Keys.ENTER)



with open('pp_res.csv','w') as resfile:
    writer = csv.DictWriter(resfile,fieldnames=field_names)
    writer.writeheader()
    driver.get("https://www.vtu4u.com/result/1rn18is076/sem-2/rs-22?cbse=1")
    find = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "table-hover", '
                                         '" " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "ng-binding", '
                                         '" " )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]')

    # writer.writeheader()
    for j in range(len(find)):
            # writer.writerow({'SUB-CODE':find[j].text})
            # print(find[j].text)
            final_res.append({'SUB-CODE':find[j].text})

    for row in final_res:
        writer.writerow(row)
