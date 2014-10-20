import mechanize
import re
from bs4 import BeautifulSoup
import urllib2
import requests

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
                print url2
                
                request2 = requests.get(url2)
                soup2 = BeautifulSoup(request2.content)
                
                legi_date = soup2.find_all("span",{"id":"ctl00_ContentPlaceHolder1_lblName2"})
                print legi_date[0].text

                legi_text = soup2.find_all("span",{"class":"st1"})
                for item in legi_text:
                    print item.text
        except:
            pass