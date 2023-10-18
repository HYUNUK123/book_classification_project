import glob
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data_path = glob.glob('./crawling_data/*data*.csv')
link_path = glob.glob('./crawling_data/*link*.csv')

# df = pd.read_csv('./crawling_data/crawling_link_0_1.0.csv')
# df_title = pd.read_csv('./crawling_data/crawling_data_0_1.0.csv')



contents = []
bk_title = []
count =0

for num in range(len(link_path)):
    df = pd.read_csv(link_path[num])
    df_title = pd.read_csv(data_path[num])
    link = df['links']
    book_title = df_title['titles']
    for i in link:
        url = str(i)
        driver.get(url)
        actions = driver.find_element(By.CSS_SELECTOR, 'body')
        actions.send_keys(Keys.END)
        time.sleep(0.5)

        for j in range(1,10):
            for k in range(1,10):
                try:
                    title = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[{}]/div[{}]/div[1]'.format(j,k)).text
                    if title == '책소개':
                        try:
                             content = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[{}]/div[{}]/div[3]'.format(j,k)).text
                        except:
                            content = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[{}]/div[{}]/div[4]'.format(j, k)).text
                except:
                    continue
        if content != []:
            content = "가"
        content = re.compile('[^가-힣]').sub(' ', content)
        contents.append(content)
        bk_title.append(book_title[count])
        print('{}.{}'.format(count,content))
        content =[]
        count +=1
        if count%10 ==0:
            df_contents = pd.DataFrame(contents, columns=['contents'])
            df_contents['titles'] = bk_title
            df_contents.to_csv('./crawling_data/crawling_last_{}.csv'.format(count), index=False)
    contents = []
    bk_title = []
    count = 0
