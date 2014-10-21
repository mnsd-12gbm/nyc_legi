"""
Get data regarding NYC City Council Legislation
"""
import mechanize
import re
from bs4 import BeautifulSoup
import urllib2
import requests
import collections
import xlwt

book = xlwt.Workbook(encoding='utf-8', style_compression = 0)
sheet = book.add_sheet('Legi', cell_overwrite_ok = True)  
row=-1

for items in ['obesity']:
    url = r'http://legistar.council.nyc.gov/Legislation.aspx'
    request = mechanize.Request(url)
    response = mechanize.urlopen(request)
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    form = forms[0]
    response.close()

    form['ctl00$ContentPlaceHolder1$txtSearch'] = items
    submit_page = mechanize.urlopen(form.click())
    soup = BeautifulSoup(submit_page.read())

    for link in soup.find_all("a"):
    	legislation = link.get("href")
        try:
            if 'LegislationDetail' in legislation:
            	url_stem = 'http://legistar.council.nyc.gov/'
                url2 = "%s%s" % (url_stem, legislation)

                request2 = requests.get(url2)
                soup2 = BeautifulSoup(request2.content)
                
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

                sheet.write (row, 0, legi_url)
                sheet.write (row, 1, title)
                sheet.write (row, 2, date)
                sheet.write (row, 3, committee)
                sheet.write (row, 4, text)
        except:
            pass

book.save("legislation_results.xls")
