import re
import pandas as pd
import glob
import datetime

data_title_path = glob.glob('./crawling_data/titles_data/crawling_data_*.csv')    # 크롤링 주소 변경 해주기
data_intro_path = glob.glob('./crawling_data/intros_data/crawling_*.csv')      # 크롤링 주소 변경 해주기
# print(data_title_path)
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
# df_titles.drop_duplicates(['titles'],inplace=True, keep='first')      # 책 소개 기준으로 중복 제거

print(df_titles.head())
print(df_titles['category'].value_counts())
df_titles.info()
df_titles.to_csv('./crawling_data/result/crawling_titles_concat_{}.csv'.format(datetime.datetime.now().strftime('%y%m%d%H%M')), index = False)

############################################### 2. 책 소개(crawling_introduction_*) 파일 합치기 ##########################################################
df_intros = pd.DataFrame()
for path in data_intro_path:
    df_temp = pd.read_csv(path)
    df_temp.rename(columns={'intro':'contents','title':'titles'}, inplace=True)      # crawling_introdution_* 컬럼명 다른거 통일
    df_intros = pd.concat([df_intros, df_temp])
print(df_intros.head())
df_intros.info()
df_intros.to_csv('./crawling_data/result/crawling_intros_concat_{}.csv'.format(datetime.datetime.now().strftime('%y%m%d%H%M%S')), index = False)

###############################################  책 제목 내용과 책 소개 내용 합치기 및 중복 제거 ###############################################
df = pd.DataFrame()
df = pd.merge(df_intros, df_titles, how='outer',on='titles')        # category를 기준으로 병합
df.to_csv('./crawling_data/merge_titles_intros_step1_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index = False)
## +) '가' Nan값으로 바꾸고, 중복값 & Nan값 지우기 추가
df.loc[df['contents']=='가', 'contents'] = None
df.loc[df['titles']==' ', 'contents'] = None
df = df.dropna()
print(df.info())
df.to_csv('./crawling_data/merge_titles_intros_step2_dropna{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index = False)
df.drop_duplicates(['titles'],inplace=True, keep='first')      # 책 소개 기준으로 중복 제거
df['book_data'] = df['contents']+' '+df['titles']     # titles, intros한 행으로 합치기
df_final = pd.DataFrame(df['book_data'], columns=['book_data'] )
df_final['category'] =  df['category']
print(df_final.head())
df_final.info()
df_final.to_csv('./crawling_data/merge_titles_intros_step3_book_data{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index = False)
df_final.to_csv('./crawling_data/result/crawling_book_data_final_{}.csv'.format(datetime.datetime.now().strftime('%y%m%d%h%M%S')), index = False)


