#!/usr/bin/python
import re
import time
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import requests

book = xlwt.Workbook(encoding='utf-8', style_compression = 0)
sheet = book.add_sheet('Legi', cell_overwrite_ok = True)  
row=-1

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0")
driver=webdriver.Firefox(profile)

driver.get('http://legistar.council.nyc.gov/Legislation.aspx')
driver.find_element_by_link_text('Advanced search >>>').click()

# Select to remove limit on searched legislative items in drop-down menu
dropdown = driver.find_element_by_name('ctl00$ContentPlaceHolder1$lstMax')
dropdown.click()

driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstMax_DropDown').click()
for val in driver.find_elements_by_class_name('rcbItem'):
    if val.text == 'All':
        val.click()

# Select "All Years" in drop-down menu
dropdown = driver.find_element_by_name('ctl00$ContentPlaceHolder1$lstYearsAdvanced')
dropdown.click()

driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstYearsAdvanced_DropDown').click()
for val in driver.find_elements_by_class_name('rcbItem'):
    if val.text == 'All Years':
        val.click()

# Select "Introduction" as document type in drop-down menu
dropdown = driver.find_element_by_name('ctl00$ContentPlaceHolder1$lstType')
dropdown.click()

driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstType_DropDown').click()
for val in driver.find_elements_by_class_name('rcbItem'):
    if val.text == 'Introduction':
        val.click()

# Submit the search
SearchButton = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnSearch2")
SearchButton.click()

for i in range(2,4):
    driver.implicitly_wait(10)
    hrefs = driver.find_elements_by_xpath("//*[@href]")
    for j in hrefs:
        legislation = j.get_attribute("href")
        try:
            if 'LegislationDetail' in legislation:
                url2 = "%s" % (legislation)

                tail_null = "Advanced&Search="
                tail1 = "ID|Text|&Search="
                tail2 = "ID%7cText%7c&Search=" 
                url2 = url2.replace(tail_null,tail1)
                url2a = url2.replace(tail1,tail2)
                print url2
                print url2a

                request2 = requests.get(url2)
                soup2 = BeautifulSoup(request2.content)

                #leg_type = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblType2"})
                agenda_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblOnAgenda2"})
                passed_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblPassed2"})

                if ((agenda_date[-4:]>=2002) or (passed_date[-4:]>=2002)):
                    legislation_number = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblFile2"})
                    legislation_status = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblStatus2"})
                    legislation_name = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblName2"})
                    legislation_title = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblTitle2"})
                    legislation_committee = soup2.find_all("a",{"id":"ctl00_ContentPlaceHolder1_hypInControlOf2"})
                    legislation_text = soup2.find_all("span",{"class":"st1"})                                

                    request2a = requests.get(url2a)
                    soup2a = BeautifulSoup(request2a.content)
                    legislation_text2 = soup2a.find_all("span",{"class":"st1"}) 

                    title, name, legi_num, status, a_date, p_date, committee, l_text = ([] for i in range(8))
                    row = row + 1 

                    for item in legislation_title:
                        title.append(item.text)              
                    for item in legislation_name:
                        name.append(item.text)
                    for item in legislation_number:
                        legi_num.append(item.text)
                    for item in legislation_status:
                        status.append(item.text)
                    for item in agenda_date:
                        a_date.append(item.text)
                    for item in passed_date:
                        p_date.append(item.text)
                    for item in legislation_committee:
                        committee.append(item.text)
                    for item in legislation_text:
                        l_text.append(' '+item.text)
                    for item in legislation_text2:
                        l_text.append(' '+item.text)

                    legi = [url2,title,name,legi_num,status,a_date,p_date,committee,l_text]
                    for column, var_observ in enumerate(legi):
                        sheet.write (row, column, var_observ)
                    time.sleep(.25)
        except:
            pass

    next_page = "%d" % (i)
    driver.find_element_by_link_text(next_page).click()
    driver.implicitly_wait(10)

book.save("legislation_data.xls")
