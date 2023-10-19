import re

import pandas as pd
import glob
import datetime

data_title_path = glob.glob('./crawling_data/crawling_data_*.csv')              # 크롤링 주소 변경 해주기
data_intro_path = glob.glob('./crawling_data/crawling_introduction_*.csv')      # 크롤링 주소 변경 해주기
print(data_title_path)
print(data_intro_path)



# 크롤링 데이터 전체 합치기
## 제목, 분류(crawling_data_*)
###
df_temp = pd.read_csv(data_title_path[0])
for i in range(len(df_temp['titles'])):
    df_temp['titles'][i] = re.compile('[^가-힣]').sub(' ', df_temp['titles'][i])
print(df_temp[:30])

df_title = pd.DataFrame()
for path in data_title_path:
    df_temp = pd.read_csv(path)
    df_title = pd.concat([df_title, df_temp])
print(df_title.head())
print(df_title['category'].value_counts())
df_title.info()
df_title.to_csv('./crawling_data/aladin_book_titles_and_classification_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index = False)

df_temp = 0         # 혹시 모를 남은 데이터 초기화

## 책 소개(crawling_introduction_*)
df_intro = pd.DataFrame()
for path in data_intro_path:
    df_temp = pd.read_csv(path)
    df_intro = pd.concat([df_intro, df_temp])
print(df_intro.head())
df_intro.info()
df_intro.to_csv('./crawling_data/aladin_book_intros_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index = False)

# 책 제목 내용과 책 소개 내용 합치기
df = pd.DataFrame()
df = pd.merge(df_intro, df_title, how='outer',on='category')        # category를 기준으로 병합,
