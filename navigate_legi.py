#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import xlwt
import requests
import sys
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

writer = csv.writer(open("legi_data.csv", "wb"))
"""
with open('legi_data.csv', 'w') as file:
    writer = csv.writer(file, delimiter = ',', lineterminator = '\n',)

print sys.getdefaultencoding()
book = xlwt.Workbook(encoding='utf-8', style_compression = 0)
sheet = book.add_sheet('Legi', cell_overwrite_ok = False)  
"""

row=-1
for i in range(1,21):

    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0")
    driver=webdriver.Firefox(profile)

    driver.get('http://legistar.council.nyc.gov/Legislation.aspx')
    driver.find_element_by_link_text('Advanced search >>>').click()
    
    #'05/31/2010'
    #'6/15/2006'
    #'2/15/2004'
    #'1/1/2002'
    inputElement1 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtOnAgenda1_dateInput")
    inputElement1.clear()
    inputElement1.send_keys('1/1/2002')
    inputElement2 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtOnAgenda2_dateInput")
    inputElement2.clear()
    
    #'12/31/2013'
    #'5/30/2010'
    #'6/14/2006'
    #'2/14/2004'
    inputElement2.send_keys('2/14/2004')
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_radOnAgenda_3").click()

    # Select "Introduction" as document type in drop-down menu
    dropdown = driver.find_element_by_name('ctl00$ContentPlaceHolder1$lstType')
    dropdown.click()

    driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstType_DropDown').click()
    for val in driver.find_elements_by_class_name('rcbItem'):
        if val.text == 'Introduction':
            val.click()

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

    # Submit the search
    SearchButton = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnSearch2")
    SearchButton.click()

    next_page = "%d" % (i)
    if i in range(2,11): 

        driver.find_element_by_link_text(next_page).click()
        print next_page
    else:
        pass
    if i in range(11,21):

        driver.find_element_by_link_text('...').click()
        driver.implicitly_wait(10)

        inputElement1 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtOnAgenda1_dateInput")
        inputElement2 = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtOnAgenda2_dateInput")
        if inputElement1 == '':
            inputElement1.send_keys('01/01/2002')
        if inputElement2 == '':
            inputElement2.send_keys('12/31/2013')
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_radOnAgenda_3").click()

        driver.find_element_by_id("ctl00_ContentPlaceHolder1_radOnAgenda_3").click()
        driver.find_element_by_link_text(next_page).click()
        print next_page
    else:
        pass

    driver.implicitly_wait(1)
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
                passed_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblPassed2"})
                legislation_number = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblFile2"})
                legislation_status = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblStatus2"})
                legislation_name = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblName2"})
                legislation_title = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblTitle2"})
                legislation_committee = soup2.find_all("a",{"id":"ctl00_ContentPlaceHolder1_hypInControlOf2"})
                legislation_text = soup2.find_all("span",{"class":"st1"})                                
                passed_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblPassed2"})  

                title, l_name, legi_num, status,  a_date, p_date, committee, l_text, = ([] for i in range(8))
                row = row + 1 

                for item in legislation_title:
                    item = item(text=True)
                    title.append(''.join(item) if item else 'NA')
                for item in legislation_name:
                    item = item(text=True)
                    l_name.append(''.join(item) if item else 'NA')
                for item in legislation_number:
                    item = item(text=True)
                    legi_num.append(''.join(item) if item else 'NA')
                for item in legislation_status:
                    item = item(text=True)
                    status.append(''.join(item) if item else 'NA')
                for item in agenda_date:
                    item = item(text=True)
                    a_date.append(''.join(item) if item else 'NA')
                for item in passed_date:
                    item = item(text=True)
                    p_date.append(''.join(item) if item else 'NA')
                for item in legislation_committee:
                    item = item(text=True)
                    committee.append(''.join(item) if item else 'NA')
                for item in legislation_text:
                    item = item(text=True)
                    l_text.append(' '.join(item) if item else ' ')
                #lg_text.append(''.join([i if ord(i) < 128 else ' ' for i in l_text]))
                #lg_text = re.split('Be it enacted by the Council as follows:' , l_text)
                #lg_text = removeNonAscii(l_text)

                legi = [i, url2,title,l_name,legi_num,status,a_date,p_date,committee,l_text]
                print a_date
                print p_date
                print row

                writer.writerow([i,url2,title,l_name,legi_num,status,a_date,p_date,committee,l_text])
                """
                for column, var_observ in enumerate(legi):
                    sheet.write (row, column, var_observ)
                book.save("legis_data.xls")
                """
        except:
            pass

