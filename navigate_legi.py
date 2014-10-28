#!/usr/bin/python
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0")
driver=webdriver.Firefox(profile)

driver.get('http://legistar.council.nyc.gov/Legislation.aspx')
inputElement = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtSearch")
inputElement.send_keys('street')

inputButton = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnSearch")
inputButton.click()

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html)

#print soup

driver.implicitly_wait(10)

for
driver.find_element_by_link_text('2').click()
