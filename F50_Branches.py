#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import re
from time import time
import json
import argparse

def get_store(store):
    store_name = store['Name']
    store_timings = store['OperatingHours']['Hours']
    street = store['Address']['AddressLine1']
    city = store['Address']['City']
    county = store['Address'].get('County')
    zipcode = store['Address']['PostalCode']
    state = store['Address']['Subdivision']
    country = store['Address'].get('CountryName')

    try:
        contact = store['TelephoneNumber'][0]['PhoneNumber']
    except:
        contact = store['TelephoneNumber'].get('PhoneNumber')

    open_timing = []
    stores_open = []
    for store_timing in store_timings:
        timing = store_timing['TimePeriod']['Summary']
        weekDay = store_timing['FullName']
        stores_open.append(weekDay)
        open_timing.append({"Week Day":weekDay,"Open Hours":timing})

    data = {
    'Store_Name' : store_name,
    'Street' : street,
    'City' : city,
    'County' : county,
    'Zipcode' : zipcode,
    'State' : state,
    'Contact' : contact,
    'Timings' : open_timing,
    'Stores_Open' : stores_open,
    'Country' : country
    }
    return data

def parse(zipcode):
    #sending requests to get the accesskey for the store listing page url
    stores_url = 'https://www.target.com/store-locator/find-stores?address={0}&capabilities=&concept='.format(zipcode)
    front_page_response = requests.get(stores_url)
    raw_access_key = re.findall("accesskey\s+?\:\"(.*)\"",front_page_response.text)

    if raw_access_key:
        accesskey = raw_access_key[0]
    else:
        print("Access key not found")

    access_time = int(time()) 
    stores_listing_url = 'https://api.target.com/v2/store?nearby={0}&range=100&locale=en-US&key={1}&callback=jQuery2140816666152355445_1500385885308&_={2}'.format(zipcode,accesskey,access_time)
    storeing_response = requests.get(stores_listing_url)
    content =re.findall("\((.*)\)",storeing_response.text)
    Locations = []
    try:
        json_data = json.loads(content[0])
        total_stores = json_data['Locations']['@count']

        if not total_stores == 0:
            stores = json_data["Locations"]["Location"]
            # Handling multiple Locations 
            if total_stores > 1:
                for store in stores:
                    Locations.append(get_store(store))
            # Single Location
        else:
            Locations.append(get_store(stores))
        return Locations
    except ValueError:
        print("No json content found in response")
  
    if __name__=="__main__":
        argparser = argparse.ArgumentParser()
        argparser.add_argument('zipcode', help='Zip code')

    args = argparser.parse_args()
    zipcode = args.zipcode

    print("Fetching Location details")
    scraped_data = parse(zipcode)
    print("Writing data to output file")
    with open('%s-locations.json'%(zipcode),'w') as fp:
        json.dump(scraped_data,fp,indent = 4)


# In[108]:


# Allianz SE
import requests
from bs4 import BeautifulSoup
r=requests.get(r'https://www.allianz.com/en/about-us/who-we-are/regions-countries.html')
c=r.content
soup=BeautifulSoup(c)
s1=soup.findAll('div',{'class':'c-link-list '})

link=[]
for i in range(len(s1)):
    for j in range(len(s1[i].findAll('a'))):
        link.append(r'https://www.allianz.com'+s1[i].findAll('a')[j]['href'])
        r=requests.get(r'https://www.allianz.com/en/about-us/who-we-are/regions-countries/argentina.html')

name=[]
address=[]
contact1=[]
contact2=[]
website=[]
for i in range(len(link)):
    r=requests.get(link[i])
    c=r.content
    soup=BeautifulSoup(c)
    s3=soup.find_all('ul',{'class':'c-tabs__nav l-grid__column-small-12 offset-large-1 offset-medium-1 l-grid__column-large-3 l-grid__column-medium-3'})
    s4=s3[0].find_all('li',{'class':'c-tabs__nav-item'})
    for j in range(len(s4)):
        try:
            name.append(s4[j].find('h5').text)
            address.append(s4[j].find_all('div',{'class':'c-copy'})[0].text)
            contact1.append(s4[j].find_all('div',{'class':'link'})[0].text)
            contact2.append(s4[j].find_all('div',{'class':'link'})[1].text)
            website.append(s4[j].find_all('div',{'class':'link'})[3].text)
        except:
            continue


# In[65]:


# UniCredit SpA
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
browser=webdriver.Chrome(path, chrome_options=chrome_options)
browser.get(r'https://www.unicreditgroup.eu/en/worldwide/our-worldwide-presence.html')
soup=BeautifulSoup(browser.page_source)
s1=soup.find_all('div',{'class':'mainCountry'})
s2=soup.find_all('div',{'class':'country'})
link=[]
for i in range(len(s1)):
    link.append(r'https://www.unicreditgroup.eu'+s1[i].find_all('a')[0]['href'])
for i in range(len(s2)):
    link.append(r'https://www.unicreditgroup.eu'+s2[i].find_all('a')[0]['href'])

s1=soup.find_all('div',{'class':'tabPanel commercialBanking selected'})
s2=s1[0].find_all('div',{'class':'bankName'})
name=[]
address=[]
contact=[]
website=[]
for i in range(len(link)):
    try:
        browser.get(link[i])
        c=browser.page_source
        soup=BeautifulSoup(c)
        s10=soup.findAll('div',{'class':'tabHeader'})
        for k in range(1,len(s10)-1):
            source=browser.page_source
            soup=BeautifulSoup(source)
            s2=soup.find_all('div',{'class':'bankName'})
            s3=soup.find_all('div',{'class':'moreInfo'})
            sub_link=[]
            for j in range(len(s3)):
                r=requests.get(r'https://www.unicreditgroup.eu'+s3[j].find_all('a')[0]['href'])
                c=r.content
                soup1=BeautifulSoup(c)
                s4=soup1.find_all('div',{'class':'base companyHeadquarters headquarters'})
                s5=soup1.find_all('div',{'class':'companyContacts base contacts'})
    #             s6=s5[0].find_all('div',{'class':'infos'})
                s7=soup1.find_all('div',{'class':'externalLink icon'})
                address.append(s4[0].text)
                contact.append(s5[0].text)
                website.append(s7[0].find('a')['href'])
            browser.find_element_by_xpath(r'//*[@id="worldwide"]/div[4]/div/div[1]/div/div[%d]/div/a'%k).click()
    except:
        pass


# In[2]:


# Lowe's
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
r=requests.get(r'https://www.lowes.com/Lowes-Stores')
c=r.content
soup=BeautifulSoup(c)

s1=soup.find_all('ul',{'class':'list unstyled'})
url=[]
for i in range(len(s1)):
    s2=s1[i].find_all('li')
    for j in range(len(s2)):
        url.append(r'https://www.lowes.com'+s2[j].find_all('a')[0]['href'])

details=[]
for j in range(len(url)):
    r=requests.get(url[j])
    c=r.content
    soup=BeautifulSoup(c)
    s3=soup.find_all('div',{'class':'storedirectory'})
    s4=s3[0].find_all('div',{'class':'v-spacing-small'})
    for k in range(len(s4)):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-gpu')
        path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
        browser=webdriver.Chrome(path, chrome_options=chrome_options)
        link=r'https://www.lowes.com'+s4[k].find_all('a')[0]['href']
        browser.get(link)
        soup=BeautifulSoup(browser.page_source)
        s5=soup.find_all('div',{'class':'view-store-info'})
        s6=s5[0].find_all('address',{'class':'v-spacing-small'})
#         s7=soup.find_all('ul',{'id':'storeList'})
#         s8=s7[0].find_all('li')
        details.append(s6[0].text)
        browser.close()
pd.DataFrame(details).to_excel(r'C:\Users\Menda Jawahar\Desktop\Fortune50\Lowe.xlsx')
#         for l in range(len(s8)):
#             details.append(s8[l].text)


# In[3]:


# Prudential Financial
import requests
from bs4 import BeautifulSoup
r=requests.get(r'https://www.prudential.com/links/about/worldwide-locations/')
c=r.content
soup=BeautifulSoup(c)
s1=soup.find_all('div',{'class':'pru-module-rich-text-editor'})

url=[]
for i in range(len(s1)):
    if len(s1[i].find_all('ul',{'dir':'ltr'}))>0:
#         li.append(s1[i].find_all('ul',{'dir':'ltr'})[0].find_all('li'))
        for j in range(len(s1[i].find_all('ul',{'dir':'ltr'})[0].find_all('li'))):
            url.append(r'https://www.prudential.com/links/about/worldwide-locations/'+s1[i].find_all('ul',{'dir':'ltr'})[0].find_all('li')[j].find_all('a')[0]['href'])
    else: 
        None


r=requests.get(url[19])
c=r.content
soup=BeautifulSoup(c)
s2=soup.find_all('div',{'class':'pru-module-rich-text-editor'})

details=[]
for l in range(len(url)):
    r=requests.get(url[l])
    c=r.content
    soup=BeautifulSoup(c)
    s2=soup.find_all('div',{'class':'pru-module-rich-text-editor'})
    for m in range(len(s2)):
        if len(s2)==1:
            details.append(s2[m].find_all('p')[2].text)
        else:
            s3=s2[0].find_all('div',{'class':'panel-body'})
            try:
                details.append(s3[0].find_all('p')[2].text)
            except:
                pass


# In[118]:


# AXA SA
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
r=requests.get(r'https://us.axa.com/contact-us.html#contactus_ResponsiveTab4')
c=r.content
soup=BeautifulSoup(c)

s1=soup.find_all('select',{'id':'select-branchName'})
values = [o.get("value") for o in s1[0].find_all('option')]
s2=s1[0].text
s3=s2.replace('\n','!')
s3=s3.replace('!Select state!','')
l1=s3.split('!')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
details=[]
for j in range(len(l1)-1):
    try:
        browser=webdriver.Chrome(path, chrome_options=chrome_options)
        browser.get(r'https://us.axa.com/find-fp-results.html?branchName={}'.format(l1[j]))
        soup=BeautifulSoup(browser.page_source)
        s4=soup.find_all('div',{'class':'fp-name'})
        for k in range(len(s4)):
            details.append(s4[k].text)
        browser.close()
    except:
        pass


# In[79]:


# Target Corp
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time
df1=pd.read_excel(r'C:\Users\Menda Jawahar\Desktop\Zipcodes.xlsx')

name=[]
add=[]
for i in range(len(df1)):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    #         chrome_options.add_argument('--headless')
    #         chrome_options.add_argument('--disable-gpu')
    path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
    browser=webdriver.Chrome(path, chrome_options=chrome_options)
    browser.get(r'https://www.target.com/store-locator/find-stores/{}'.format(df1['ZipCode'][i]))
    source=browser.page_source
    soup=BeautifulSoup(source)
    s1=soup.find_all('div',{'class':'Card-rwevr7-0 kUucXy'})
    if len(s1)!=0:
        for i in range(len(s1)):
            name.append(s1[i].find_all('h2',{'class':'styles__StoreCardTitle-n4vg0b-0-Heading bFTvJp sc-bdVaJa ixexCJ'})[0].text)
            add.append(s1[i].find_all('div',{'class':'styles__CardMessage-nego8d-3 kNosOL'})[0].find_all('a')[0].text)  

pd.DataFrame(add).to_excel(r'C:\Users\Menda Jawahar\Desktop\add.xlsx')


# In[127]:


# TJX
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time
df1=pd.read_excel(r'C:\Users\Menda Jawahar\Desktop\Zipcodes.xlsx')

add=[]
for i in range(len(df1)):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    #         chrome_options.add_argument('--headless')
    #         chrome_options.add_argument('--disable-gpu')
    path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
    browser=webdriver.Chrome(path, chrome_options=chrome_options)
    browser.get(r'http://www.tjx.com/stores')
    browser.find_element_by_xpath('//*[@id="address"]').click()
    browser.find_element_by_xpath('//*[@id="address"]').send_keys(int(df1['ZipCode'][i]))
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="address"]').send_keys(Keys.DOWN)
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="address"]').send_keys(Keys.ENTER)
    time.sleep(4)
    source=browser.page_source
    soup=BeautifulSoup(source)
    s1=soup.find_all('div',{'class':'locator__results-scroll'})
    s2=s1[0].find_all('div',{'class':'locator__result gutter-pad'})
    for i in range(len(s2)):
        add.append(s2[i].text)
    browser.close()
pd.DataFrame(add).to_excel(r'C:\Users\Menda Jawahar\Desktop\TJX.xlsx')


# Banco Santandar
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time
r=requests.get(r'https://locations.santanderbank.com/index.html')
c=r.content
soup=BeautifulSoup(c)
s1=soup.find_all('ul',{'class':'c-directory-list-content'})
s2=s1[0].find_all('a')

name=[]
address=[]
for i in range(len(s2)):
    url=r'https://locations.santanderbank.com/'+s2[i]['href']
    r1=requests.get(url)
    c1=r1.content
    soup1=BeautifulSoup(c1)
    try:
        s3=soup1.find_all('div',{'class':'row c-directory-list-content-wrapper'})
        if len(s3)!=0:
            s4=s3[0].findAll('ul',{'class':'c-directory-list-content'})
            for j in range(len(s4)):
                for k in range(len(s4[j])):
                    sub_url=r'https://locations.santanderbank.com/'+s4[j].findAll('a')[k]['href']
                    r2=requests.get(sub_url)
                    c2=r2.content
                    soup2=BeautifulSoup(c2)
                    s5=soup2.find_all('div',{'class':'Nap container container-border-bottom'})
                    for l in range(len(s5)):
                        name.append(s5[l].find_all('h1'))
                        address.append(s5[l].find_all('div',{'class':'Nap-address'})[0].text)
        else:
            s3=soup1.find_all('div',{'class':'Nap container container-border-bottom'})
            address.append(s3[0].text)
    except:
        pass


# In[368]:


# UBS
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-gpu')
path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
browser=webdriver.Chrome(path, chrome_options=chrome_options)
browser.get(r'https://www.ubs.com/locations.html#usa/en/ns/all/')

soup=BeautifulSoup(browser.page_source)
s1=soup.find_all('div',{'tabindex':'-1'})
s2=s1[0].find_all('ul',{'aria-expanded':'true'})
s3=s2[0].find_all('li')
address=[]
for i in range(len(s3)):
    address.append(s3[i].text)
r=requests.get(r'https://www.ubs.com/locations/_jcr_content.lofisearch.all.en.data').json()
x=r['hits']['hits']
l=[]
for i in x:
    for k,v in i.items():
        l.append(v)
l1=[]
for i in range(len(l)):
    if type(l[i]) is dict:
        l1.append(l[i]['bu_podAddress'])
pd.DataFrame(l1).to_excel('ubs.xlsx')


# Home Depot
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time
df1=pd.read_excel(r'C:\Users\Menda Jawahar\Desktop\Zipcodes.xlsx')

name=[]
address=[]
contact=[]
for j in range(len(df1)):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    #         chrome_options.add_argument('--headless')
    #         chrome_options.add_argument('--disable-gpu')
    path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
    browser=webdriver.Chrome(path, chrome_options=chrome_options)
    browser.get(r'https://www.homedepot.com/l/search/{}/full/'.format(int(df1['ZipCode'][j])))
    try:
#         browser.find_element_by_xpath('//*[@id="storeSearchBox"]').click()
#         browser.find_element_by_xpath('//*[@id="storeSearchBox"]').send_keys(int(df1['ZipCode'][j]))
#         browser.find_element_by_xpath('//*[@id="storeSearchBox"]').send_keys(Keys.ENTER)
        soup=BeautifulSoup(browser.page_source)
        s1=soup.findAll('div',{'class':'sfstores'})
        for i in range(len(s1)):
            try:
                name.append(s1[i].findAll('h1')[0].text)
                address.append(s1[i].findAll('div',{'class':'sfstoreamp'})[0].find_all('ul',{'class':'sfstoreinfo'})[0].text)
                contact.append(s1[i].findAll('div',{'class':'sfstoreamp'})[0].find_all('li',{'class':'sfstorephone'})[0].text)
                browser.close()
            except:
                pass
    except:
        pass
pd.DataFrame(name).append(pd.DataFrame(address)).append(pd.DataFrame(contact)).to_excel('homedepot.xlsx')


# Wellsfargo
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time

r=requests.get(r'https://www.branchspot.com/wells-fargo-bank/')
c=r.content
soup=BeautifulSoup(c)
s1=soup.find_all('table',{'class':'two-column'})
s2=s1[0].find_all('a')

details=[]
for i in range(1):
    url=r'https://www.branchspot.com'+s2[i]['href']
    r1=requests.get(url)
    c1=r1.content
    soup1=BeautifulSoup(c1)
    s3=soup1.find_all('table',{'class':'two-column'})
    s4=s3[0].findAll('a')
    for j in range(len(s4)):
        sub_url=r'https://www.branchspot.com'+s4[j]['href']
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        #         chrome_options.add_argument('--headless')
        #         chrome_options.add_argument('--disable-gpu')
        path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
        browser=webdriver.Chrome(path, chrome_options=chrome_options)
        browser.get(sub_url)
        soup2=BeautifulSoup(browser.page_source)
        if 'result-box' in str(soup2):
            if 'pagination' not in str(soup2):
                s7=soup2.find_all('div',{'class':'result-box'})
                for l in range(len(s7)):
                    details.append(s7[l].text)
                    print(details)
                browser.close()
            else:
                s5=soup2.find_all('div',{'class':'pagination'})
                s6=s5[0].find_all('a')
                for k in range(0,len(s6)):
                    if k==0:
                        s10=soup2.find_all('div',{'class':'result-box'})
                        for a in range(len(s10)):
                            details.append(s10[a].text)
                            print(details)
                        browser.close()
                    else:
                        sub_sub_url=sub_url+s6[0].find_all('a')[k]['href']
                        browser.get(sub_sub_url)
                        soup3=BeautifulSoup(browser.page_source)
                        s8=soup2.find_all('div',{'class':'result-box'})
                        for m in range(len(s8)):
                            details.append(s8[m].text)
                            print(details)
                        browser.close()
        elif 'left-column' in str(soup2):
            s9=soup2.find_all('div',{'class':'left-column'})
            details.append(s9[0].find_all('table')[0].text)
            print(details)
            browser.close()


# In[66]:


# US Bancorp
import requests
from bs4 import BeautifulSoup
r=requests.get(r'https://www.usbanklocations.com/u-s-bank-locations.htm')
c=r.content
soup=BeautifulSoup(c)
s1=soup.find_all('div',{'class':'plb'})
s2=soup.find_all('div',{'class':'plw'})
details=[]
for i in range(len(s2)):
    details.append(s2[i].text)
for j in range(1,311):
    try:
        if j!=310:
            r1=requests.get(r'https://www.usbanklocations.com/u-s-bank-locations_{}.htm'.format(j))
            c1=r1.content
            soup1=BeautifulSoup(c1)
            s1=soup.find_all('div',{'class':'plb'})
            s2=soup.find_all('div',{'class':'plw'})
            for i in range(len(s1)):
                details.append(s1[i].text)
                details.append(s2[i].text)
        elif j==310:
            r1=requests.get(r'https://www.usbanklocations.com/u-s-bank-locations_310.htm')
            c1=r1.content
            soup1=BeautifulSoup(c1)
            s1=soup.find_all('div',{'class':'plb'})
            for i in range(len(s1)):
                details.append(s1[i].text)
    except:
        pass
pd.DataFrame(details).to_excel(r'USBancorp.xlsx')


# Banco Bilbao Vizcaya Argentaria S.A.
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time

df1=pd.DataFrame(columns=['add1','add2','add3'])
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-gpu')
path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
browser=webdriver.Chrome(path, chrome_options=chrome_options)
browser.get(r'https://www.bbva.com/en/contact/')

soup=BeautifulSoup(browser.page_source)

s1=soup.find_all('li',{'class':'data-address'})

details=[]
for i in range(len(s1)):
    details.append(s1[i].text)

pd.DataFrame(details).to_excel(r'C:\Users\Menda Jawahar\Desktop\Fortune50\Banco Bilbao.xlsx')


# CVS
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
from itertools import cycle
import time
def get_proxies():
    r=requests.get(r'https://free-proxy-list.net/')
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.findAll('tbody')
    s2=s1[0].find_all('tr')
    proxy_ip=[]
    for i in range(len(s2)):
        proxy_ip.append(s2[i].find_all('td')[0].text+':'+s2[i].find_all('td')[1].text)
    return proxy_ip
proxies = get_proxies()
proxy_pool=cycle(proxies)
df1=pd.DataFrame(columns=['add1','add2','add3'])
pos=0
for i in range(1,201):
    try:
        options = webdriver.ChromeOptions()
        ua = UserAgent()
        userAgent = ua.random
        proxy = next(proxy_pool)
        options.add_argument('--no-sandbox')
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--proxy-server={}'.format(proxy))
        path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
        browser=webdriver.Chrome(path, chrome_options=options)
        browser.set_page_load_timeout(60)
        browser.get(r'https://www.cvsspecialty.com/FASTPROXY/storelocator/#/store-direction/{}'.format(i))
#         time.sleep(2)
        s1=BeautifulSoup(browser.page_source).find_all('div',{'class':'filter-row'})
        s2=s1[0].find_all('p',{'class':'ng-binding'})
        add=[]
        for j in range(len(s2)):
            add.append(s2[j].text)
        print(add)
        df1.loc[pos]=add
        pos+=1
    except:
        pass


# KBC
import requests
from bs4 import BeautifulSoup
import threading
from threading import *
import queue 
queue = queue.Queue()

def bruxelles(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_bruxelles=[]
    for i in range(len(s2)):
        details_bruxelles.append(s2[i].text)
        print(details_bruxelles)

def antwerp(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_antwerp=[]
    for i in range(len(s2)):
        details_antwerp.append(s2[i].text)
        print(details_antwerp)

def ghent(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_ghent=[]
    for i in range(len(s2)):
        details_ghent.append(s2[i].text)
        print(details_ghent)

def charleroi(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_charleroi=[]
    for i in range(len(s2)):
        details_charleroi.append(s2[i].text)
        print(details_charleroi)

def liege(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_liege=[]
    for i in range(len(s2)):
        details_liege.append(s2[i].text)
        print(details_liege)

def brugge(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_brugge=[]
    for i in range(len(s2)):
        details_brugge.append(s2[i].text)
        print(details_brugge)

def schaerbeek(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_schaerbeek=[]
    for i in range(len(s2)):
        details_schaerbeek.append(s2[i].text)
        print(details_schaerbeek)

def leuven(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_leuven=[]
    for i in range(len(s2)):
        details_leuven.append(s2[i].text)
        print(details_leuven)

def ostend(url):
    r=requests.get(url)
    c=r.content
    soup=BeautifulSoup(c)
    s1=soup.find_all('div',{'class':'contenttext lstbranches'})
    s2=s1[0].find_all('p')
    details_ostend=[]
    for i in range(len(s2)):
        details_ostend.append(s2[i].text)
        print(details_ostend)

if __name__ == "__main__":
    t1=threading.Thread(target=bruxelles,args=(r'http://bankbelgium.com/branches/kbc-bruxelles',))
    t1.start()
    t2=threading.Thread(target=antwerp,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-antwerp-belgium',))
    t2.start()
    t3=threading.Thread(target=ghent,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-ghent-belgium',))
    t3.start()
    t4=threading.Thread(target=charleroi,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-charleroi-belgium',))
    t4.start()
    t5=threading.Thread(target=liege,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-liege-belgium',))
    t5.start()
    t6=threading.Thread(target=brugge,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-bruges-belgium',))
    t6.start()
    t7=threading.Thread(target=schaerbeek,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-schaerbeek-belgium',))
    t7.start()
    t8=threading.Thread(target=leuven,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-leuven-belgium',))
    t8.start()
    t9=threading.Thread(target=ostend,args=(r'http://bankbelgium.com/branches/kbc-bank-branches-atms-ostend-belgium',))
    t9.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()

time2=time.time()
print(time2-time1)


# In[4]:


import requests
from bs4 import BeautifulSoup
import re
r=requests.get(r'https://www.inditex.com/about-us/inditex-around-the-world#country/RU')

soup=BeautifulSoup(r.content)
soup=str(soup)
s=re.findall(r".\d+\.\d+", soup)
s=s[11:]
s1=str(s)
s1=s1.replace('[','')
s1=s1.replace("',","'")
s2=s1.split()

lat=[]
long=[]
i=0
for i in range(len(s2)):
    try:
        if i%2==0:
            lat.append(s2[i])
            print(lat)
        else:
            long.append(s2[i])
    except:
        pass


# In[ ]:


# IDENTIFIERS
# \d--anything number
# \D--anything but a number
# \s--anything space
# \S--anything but a space
# \w--anything character
# \W--anything but a character
# . --any character except for a new line
# \b--the whitespace around words
# \.--a period

# MODIFIERS
# {1,3}--we're expecting 1-3 ex:\d{1,3}
# + --Match one or more
# ? --Match 0 or 1
# * --Match 0 or more
# $ --Match the end of a string
# ^ --Match the begining of a string
# ! --either or \d{1,3} ! \w{5,6}
# []--Range or Variance [A-Za-z1-5]
# {x}--expecting x amount

# White space characters
# \n--new line
# \s--space
# \t--tab
# \e--escape
# \f form feed
# \r return


# In[58]:


# HSBC
import requests
from bs4 import BeautifulSoup
import pandas as pd

r=requests.get(r'https://hsbc.banklocationmaps.com/taiwan')
c=r.content
soup=BeautifulSoup(c)
s1=soup.find_all('div',{'class':'list-group list-group-flush'})
s2=s1[0].find_all('a')

df=pd.DataFrame(columns=['name','address','type','contact'])

pos=0
for i in range(len(s2)):
    url=r'https://bankofnovascotia.banklocationmaps.com'+s2[i]['href']
    r1=requests.get(url)
    c1=r1.content
    soup1=BeautifulSoup(c1)
    s3=soup1.find_all('div',{'class':'list-group list-group-flush'})
    s4=s3[0].find_all('a')
    for j in range(len(s4)):
        try:
            details=[]
            sub_url=r'https://bankofnovascotia.banklocationmaps.com'+s4[j]['href']
            r2=requests.get(sub_url)
            c2=r2.content
            soup2=BeautifulSoup(c2)
            s5=soup2.find_all('div',{'class':'col-lg-8 region'})
            s6=s5[0].find_all('div',{'class':'address'})
            s7=s5[0].find_all('h4')
#             s8=s5[0].find_all('div',{'class':'phone'})
            s9=s5[0].find_all('div',{'class':'atm_only'})
            for k in range(len(s6)):
                details.append(s7[k].text)
                details.append(s6[k].text)
                details.append(s9[k].text)
#                 details.append(s8[k].text)
                df.loc[pos]=details
                print(df)
                pos+=1
        except:
            pass

pd.DataFrame(l1+l2+l3).to_excel(r'HSBC1.xlsx')


# bnp paribas
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time
r=requests.get(r'https://www.branchspot.com/bank-of-the-west/')
c=r.content
soup=BeautifulSoup(c)
s1=soup.findAll('tbody')
s2=s1[0].find_all('a')

details=[]
for i in range(2,5):
#     url=r'https://www.branchspot.com'+s2[i]['href']
    url=r'https://www.branchspot.com/bank-of-the-west/ca/?page={}'.format(i)
    r1=requests.get(url)
    c1=r1.content
    soup1=BeautifulSoup(c1)
    s3=soup1.find_all('tbody')
    s4=s3[0].find_all('a')
    for j in range(len(s4)):
        sub_url=r'https://www.branchspot.com'+s4[j]['href']
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        #         chrome_options.add_argument('--headless')
        #         chrome_options.add_argument('--disable-gpu')
        path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
        browser=webdriver.Chrome(path, chrome_options=chrome_options)
        browser.get(sub_url)
        soup2=BeautifulSoup(browser.page_source)
        if 'result-box' in str(soup2):
            if 'pagination' not in str(soup2):
                s7=soup2.find_all('div',{'class':'result-box'})
                for l in range(len(s7)):
                    details.append(s7[l].text)
                browser.close()
            else:
                s5=soup2.find_all('div',{'class':'pagination'})
                s6=s5[0].find_all('a')
                for k in range(0,len(s6)):
                    if k==0:
                        s10=soup2.find_all('div',{'class':'result-box'})
                        for a in range(len(s10)):
                            details.append(s10[a].text)
                        browser.close()
                    else:
                        sub_sub_url=sub_url+s6[0].find_all('a')[k]['href']
                        browser.get(sub_sub_url)
                        soup3=BeautifulSoup(browser.page_source)
                        s8=soup2.find_all('div',{'class':'result-box'})
                        for m in range(len(s8)):
                            details.append(s8[m].text)
                        browser.close()
        elif 'left-column' in str(soup2):
            s9=soup2.find_all('div',{'class':'left-column'})
            details.append(s9[0].find_all('table')[0].text)
            browser.close()


# RiteAid
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import time

r=requests.get(r'https://locations.riteaid.com/')
c=r.content
soup=BeautifulSoup(c)
s1=soup.find_all('div',{'class':'c-directory-list'})
s2=s1[0].find_all('li',{'class':'c-directory-list-content-item'})

df1=pd.DataFrame(columns=['Name','Address','Contact'])

## pos=0
for i in range(4,len(s2)):
    url=r'https://locations.riteaid.com/'+s2[i].find_all('a')[0]['href']
    r1=requests.get(url)
    c1=r1.content
    soup1=BeautifulSoup(c1)
    s3=soup1.find_all('div',{'class':'c-directory-list'})
    s4=s3[0].find_all('li',{'class':'c-directory-list-content-item'})
    for j in range(len(s4)):
        details=[]
        sub_url=r'https://locations.riteaid.com/'+s4[j].find_all('a')[0]['href']
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        path =str(r'C:\Users\Menda Jawahar\Desktop\chromedriver_win32/chromedriver.exe')
        browser=webdriver.Chrome(path, chrome_options=chrome_options)
        browser.get(sub_url)
        time.sleep(1)
        soup2=browser.page_source
        soup2=BeautifulSoup(soup2)
        if 'location-list-wrap' not in str(soup2):
            try:
                details.append(soup2.find_all('h1',{'class':'Nap-title Text--h1'})[0].text)
                details.append(soup2.find_all('div',{'class':'Nap-address'})[0].text)
                details.append(soup2.find_all('div',{'class':'Nap-phone'})[0].text)
                df1.loc[pos]=details
                pos+=1
                browser.close()
            except:
                pass
        elif 'location-list-wrap' in str(soup2):
            try:
                s5=soup2.find_all('div',{'class':'location-list-wrap'})
                s6=s5[0].find_all('div',{'class':'c-location-grid-item'})
                for k in range(len(s6)):
                    details=[]
                    details.append(s6[k].find_all('h5',{'class':'c-location-grid-item-title'})[0].text)
                    details.append(s6[k].find_all('div',{'class':'c-location-grid-item-address'})[0].text)
                    details.append(s6[k].find_all('div',{'class':'c-location-grid-item-phone'})[0].text)
                    df1.loc[pos]=details
                    pos+=1
                    print(len(df1))
                    browser.close()
            except:
                pass


