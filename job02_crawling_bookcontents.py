import glob
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)

# data_path = glob.glob('./crawling_data/*data*.csv')
link_path = glob.glob('./crawling_data/*link*.csv')

# df = pd.read_csv('./crawling_data/crawling_link_0_1.0.csv')
# df_title = pd.read_csv('./crawling_data/crawling_data_0_1.0.csv')



contents = []
titles = []
count = 0

for link in link_path:
    df = pd.read_csv(link)
    df_link = df['links']
    for i in df_link:
        url = str(i)
        driver.get(url)
        try:
            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.END)
            time.sleep(1)
        except:
            continue
        try:
            bk_title = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/span').text
            bk_title = re.compile('[^가-힣]').sub(' ', bk_title)
            titles.append(bk_title)
        except:
            bk_title = '가'
        for j in range(15, 1, -1):
            for k in range(15, 1, -1):
                try:
                    act = ActionChains(driver)
                    title = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[{}]/div[{}]/div[1]'.format(j,k)).text
                    if '책소개' in title:
                        try:
                             content = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[{}]/div[{}]/div[3]'.format(j,k)).text
                        except:
                            content = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[{}]/div[{}]/div[4]'.format(j, k)).text
                except:
                    continue
        if content == []:
            content = "가"
        content = re.compile('[^가-힣]').sub(' ', content)
        contents.append(content)
        print('{}.{} : {}'.format(count, bk_title, content))
        content =[]
        count +=1
        if count%10 ==0:
            df_contents = pd.DataFrame(contents, columns=['contents'])
            df_contents['titles'] = titles
            df_contents.to_csv('./crawling_data/crawling_last_{}.csv'.format(count), index=False)
    df_contents = pd.DataFrame(contents, columns=['contents'])
    df_contents['titles'] = titles
    df_contents.to_csv('./crawling_data/crawling_final_{}.csv'.format(link), index = False)
    contents = []
    titles = []
    count = 0
