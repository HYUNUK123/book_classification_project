import re
import pandas as pd
import glob
import datetime

data_title_path = glob.glob('./crawling_data/titles_test_data/crawling_data_*.csv')    # 크롤링 주소 변경 해주기
# data_intro_path = glob.glob('./crawling_data/crawling_introduction_*.csv')      # 크롤링 주소 변경 해주기
print(data_title_path)
# print(data_intro_path)

############################################ 1. 제목, 분류(crawling_data_*) 파일 합치기 ############################################
df_titles = pd.DataFrame()
for j in range(len(data_title_path)):
    df_temp = pd.read_csv(data_title_path[j])
    for i in range(len(df_temp['titles'])):
        df_temp['titles'][i] = re.compile('[^가-힣]').sub(' ', df_temp['titles'][i])
        if (df_temp['titles'][i].isspace()):        # 한글 외 지우면서 제목이 ' '형태가 된 것 None으로...
            df_temp['titles'][i] = None
    df_titles = pd.concat([df_titles, df_temp])
## 제목값 공백 제거 (중복값은 나중에 합한 후에 처리할 것)
df_titles = df_titles.dropna()
df_titles.drop_duplicates(['titles'],inplace=True, keep='first')      # 책 소개 기준으로 중복 제거

print(df_titles.head())
print(df_titles['category'].value_counts())
df_titles.info()
df_titles.to_csv('./crawling_data/titles_test_data/crawling_titles_concat_{}.csv'.format(datetime.datetime.now().strftime('%y%m%d%H%M')), index = False)