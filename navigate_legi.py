#!/usr/bin/python
import re
import time
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import requests

def to_excel():
    book = xlwt.Workbook(encoding='utf-8', style_compression = 0)
    sheet = book.add_sheet('Legi', cell_overwrite_ok = True)  
    row=-1

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0")
driver=webdriver.Firefox(profile)

driver.get('http://legistar.council.nyc.gov/Legislation.aspx')
driver.find_element_by_link_text('Advanced search >>>').click()

dropdown = driver.find_element_by_name('ctl00$ContentPlaceHolder1$lstMax')
dropdown.click()

driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstMax_DropDown').click()
for val in driver.find_elements_by_class_name('rcbItem'):
    if val.text == 'All':
        val.click()

dropdown = driver.find_element_by_name('ctl00$ContentPlaceHolder1$lstYearsAdvanced')
dropdown.click()

driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstYearsAdvanced_DropDown').click()
for val in driver.find_elements_by_class_name('rcbItem'):
    if val.text == 'All Years':
        val.click()

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
                request2 = requests.get(url2)
                soup2 = BeautifulSoup(request2.content)
                type = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblType2"})
                status = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblStatus2"})
                print url2

                if ((type[0].text == "Resolution" or 
                    type[0].text == "Introduction") and 
                    (status[0].text == "Adopted")):

                    legislation_title = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblName2"})
                    legislation_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblOnAgenda2"})
                    legislation_committee = soup2.find_all("a",{"id":"ctl00_ContentPlaceHolder1_hypInControlOf2"})
                    legislation_text = soup2.find_all("span",{"class":"st1"})                                

                    legi_url, title, date, committee, text = ([] for i in range(5))
                    row = row + 1 

                    legi_url = url2                
                    for item in legislation_title:
                        title.append(item.text)
                    for item in legislation_date:
                        date.append(item.text)
                    for item in legislation_committee:
                        committee.append(item.text)
                    for item in legislation_text:
                        text.append(' '+item.text)

                    legi = [legi_url,title,date,committee,text]
                    for column, var_observ in enumerate(legi):
                        sheet.write (row, column, var_observ)
                    time.sleep(1)
        except:
            pass

    next_page = "%d" % (i)
    driver.find_element_by_link_text(next_page).click()
    driver.implicitly_wait(10)

book.save("legislation_data.xls")
