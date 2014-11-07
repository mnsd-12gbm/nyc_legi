#!/usr/bin/python
import re
import time
import xlwt
import requests
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

print sys.getdefaultencoding()
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

driver.find_element_by_link_text('8').click()
for i in range(9,11):
    hrefs = driver.find_elements_by_xpath("//*[@href]")
    lg_list = []

    for j in hrefs:
        legislation = j.get_attribute("href")
        lg_list.append(legislation)

    for lg in lg_list:    
        try:
            if 'LegislationDetail' in lg:
                url2 = "%s" % (lg)
                print url2

                driver.get(url2)
                driver.find_element_by_link_text('Text').click()
                url2_html = driver.page_source
                soup2 = BeautifulSoup(url2_html,'html.parser')

                agenda_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblOnAgenda2"})
                a_date = []
                for item in agenda_date:
                    item = item(text=True)
                    a_date.append(''.join(item) if item else 'NA')

                bloomberg_years = list(range(2002,2013))
                if a_date[-4:] in bloomberg_years:    
                    passed_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblPassed2"})
                    legislation_number = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblFile2"})
                    legislation_status = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblStatus2"})
                    legislation_name = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblName2"})
                    legislation_title = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblTitle2"})
                    legislation_committee = soup2.find_all("a",{"id":"ctl00_ContentPlaceHolder1_hypInControlOf2"})
                    legislation_text = soup2.find_all("span",{"class":"st1"})                                
                    passed_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblPassed2"})  

                    title, name, legi_num, status,  p_date, committee, l_text = ([] for i in range(7))
                    row = row + 1 

                    for item in legislation_title:
                        item = item(text=True)
                        title.append(''.join(item) if item else 'NA')
                    for item in legislation_name:
                        item = item(text=True)
                        name.append(''.join(item) if item else 'NA')
                    for item in legislation_number:
                        item = item(text=True)
                        legi_num.append(''.join(item) if item else 'NA')
                    for item in legislation_status:
                        item = item(text=True)
                        status.append(''.join(item) if item else 'NA')
                    for item in passed_date:
                        item = item(text=True)
                        p_date.append(''.join(item) if item else 'NA')
                    for item in legislation_committee:
                        item = item(text=True)
                        committee.append(''.join(item) if item else 'NA')
                    for item in legislation_text:
                        item = item(text=True)
                        l_text.append(' '.join(item) if item else ' ')
                    lg_text = re.split('Be it enacted by the Council as follows:' , l_text)

                    legi = [url2,title,name,legi_num,status,a_date,p_date,committee,lg_text[1]]
                    for column, var_observ in enumerate(legi):
                        sheet.write (row, column, var_observ)
                    book.save("legis_data.xls")
        except:
            pass

    next_page = "%d" % (i)
    driver.find_element_by_link_text(next_page).click()
    driver.implicitly_wait(1)

book.save("legis_data.xls")
