from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time
from selenium.webdriver.common.keys import Keys

df_introductions = pd.DataFrame()

for z in range(4,6):
    for y in range(1,10):
        link = pd.read_csv('./crawling_data/crawling_link_{}_{}.0.csv'.format(z,y))

        options = ChromeOptions()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        options.add_argument('user-agent=' + user_agent)
        options.add_argument("lang=ko_KR")

        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경


        # 스크롤 내리는 부분
        actions = driver.find_element(By.CSS_SELECTOR, 'body')
        actions.send_keys(Keys.END)
        time.sleep(0.5)
        for k in range(2500):
            # print(link['links'][k])
            url = link['links'][k]

            df_titles = pd.DataFrame()
            titles = []
            df_intros = pd.DataFrame()
            intros = []
            driver.get(url)
            try:
                title = driver.find_element('xpath', '//*[@id="Ere_prod_allwrap"]/div[3]/div[2]/div[1]/div/ul/li[2]/div/span').text
                titles.append(title)
            except:
                title = ['가']

            actions = driver.find_element(By.CSS_SELECTOR, 'body')
            actions.send_keys(Keys.END)
            time.sleep(0.5)

            i_found, j_found = None, None
            for i in range(8,10):
                for j in range(3,7):
                    try:
                         intro = driver.find_element('xpath', '/html/body/div[5]/div[{}]/div[{}]/div[1]'.format(i,j)).text
                    except:
                        continue
                    if '책소개' in intro:
                        i_found,j_found= i,j
                        break
                if i_found is not None:
                    break  # 바깥 루프를 빠져나옴

            if i_found is not None and j_found is not None:
                try:
                    intro = driver.find_element('xpath', '/html/body/div[5]/div[{}]/div[{}]/div[3]'.format(i_found, j_found)).text
                except:
                    intro = driver.find_element('xpath', '/html/body/div[5]/div[{}]/div[{}]/div[4]'.format(i_found, j_found)).text
                if intro == []:
                    intro = ['가']
                intro = re.compile('[^가-힣]').sub(' ', intro)
                intros.append(intro)
                intro = []
                # print("책소개가 발견되었습니다. i={}, j={}, intro: {}".format(i_found, j_found, intro))
            else:
                print("책소개를 찾을 수 없습니다.")

            print(titles)
            print(intros)

            # 인덱스 컬럼을 추가하기
            df_index = pd.DataFrame([k], columns=['index'])
            df_titles = pd.DataFrame(titles, columns=['title'])
            df_intros = pd.DataFrame(intros, columns=['intro'])

            # 데이터프레임을 합치기
            df_temp = pd.concat([df_index, df_titles, df_intros], axis=1)
            df_introductions = pd.concat([df_introductions, df_temp])

            print(df_introductions)
            if (k % 2499 == 0 and k!=0):
                df_introductions.to_csv('./crawling_data/crawling_introduction_{}_{}.0.csv'.format(z,y), index = False)
                df_introductions=pd.DataFrame()