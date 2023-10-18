import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/*data*.csv')
content_path = glob.glob('./crawling_data/*content*.csv')

print(data_path)


for content, path in content_path, data_path:
    df_temp = pd.read_csv(path)
    df_content = pd.read_csv(content)
    df = pd.DataFrame(df_temp, columns=['titles'])
    df['contents'] = df_content
    print(df.head())

    # df = pd.concat([df, df_temp])

df.info()
df.to_csv('./crawling_data/book_titles_{}.csv'.format(
    datetime.datetime.now().strftime(('%Y%m%d'))), index = False)