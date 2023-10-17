from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time


options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

category = ['Economy', 'Novel', 'Poetry', 'Humanities', 'Self_development','History', 'Cartoon', 'Magazine']
category_pages = [170, 50917, 50940, 656, 336, 74, 2551, 2913]

url1 = 'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=25&ViewType=Detail&PublishMonth=0&SortOrder=2&page='

df_titles = pd.DataFrame()
for i in range(0,2):
    url2 = '&Stockstatus=1&PublishDay=84&CID={}&SearchOption='.format(category_pages[i])
    titles = []
    links = []
    for j in range(1,1000):
        url = url1 + str(j) + url2
        driver.get(url)
        time.sleep(0.5)
        print(j)
        for k in range(1, 26):
            try:
                title = driver.find_element('xpath', '//*[@id="Myform"]/div[2]/div[{}]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[2]/a/b'.format(k)).text
                links_selector = driver.find_elements(By.CSS_SELECTOR, '#Myform > div:nth-child(2) > div:nth-child({}) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(2) > a.bo3'.format(k))
                titles.append(title)
                for link_selector in links_selector:
                    link = link_selector.get_attribute('href')
                    links.append(link)
            except:
                try:
                    title = driver.find_element('xpath', '//*[@id="Myform"]/div[2]/div[{}]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[1]/a/b'.format(k)).text
                    links_selector = driver.find_elements(By.CSS_SELECTOR, '#Myform > div:nth-child(2) > div:nth-child({}) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(2) > a.bo3'.format(k))
                    titles.append(title)
                    for link_selector in links_selector:
                        link = link_selector.get_attribute('href')
                        links.append(link)
                except:
                    try:
                        title = driver.find_element('xpath', '//*[@id="Myform"]/div[2]/div[{}]/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/div[1]/ul/li[1]/a[1/b'.format(k)).text
                        links_selector = driver.find_elements(By.CSS_SELECTOR, '#Myform > div:nth-child(2) > div:nth-child({}) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(2) > a.bo3'.format(k))
                        titles.append(title)
                        for link_selector in links_selector:
                            link = link_selector.get_attribute('href')
                            links.append(link)
                    except:
                        print('NoSuchElementException : {}페이지 {}번째'.format(j, k))
        if(j%100 ==0):
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[i]
            df_section_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(i,j), index = False)
            titles = []
            df_section_link = pd.DataFrame(links, columns= ['links'])
            df_section_link.to_csv('./crawling_data/crawling_link_{}_{}.csv'.format(i,j), index = False)
            links = []

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

