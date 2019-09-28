import math, random
import numpy as np
import tensorflow as tf
import pandas_datareader as data_reader
from collections import deque
from tqdm import tqdm
import pandas as pd
import plotly.offline as offline
import plotly.graph_objs as go
class Machine:
    def __int__(self):
        self.code_df = pd.DataFrame({'name':[],'code':[]})

    def krx_crawl(self):
        self.code_df = \
        pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
        self.code_df.종목코드 = self.code_df.종목코드.map('{:06d}'.format())
        self.code_df = self.code_df[['회사명', '종목코드']]
        self.code_df = self.code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
    def code_df_head(self):
        print(self.code_df.head())
    def get_url(self, item_name, code_df):
        code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=Fasle)
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code='005930')
        print('요청 URL = {}'.format(url))
        return url
    def test(self,code):
        # item_name = '삼성전자'
        # url = self.get_url(item_name, self.code_df)
        df = pd.DataFrame()
        for page in range(1,21):
            pg_url ='http://finance.naver.com/item/sise_day.nhn?code={url}&page={page}'.format(url=code,page=page)
            df = df.append(pd.read_html(pg_url,header=0)[0], ignore_index=True)
        df.dropna(inplace=True)# na행제거
        return df
    def rename_item_name(self,param):
        df = param.rename(columns= {'날짜':'date','종가':"close",'전일비':"diff",
                                          '시가':"open",'고가':"high",'저가':"low",'거래량':"volume"})
        df[['close','diff','open','high','low','volume']] =\
        df[['close','diff','open','high','low','volume']].astype(int)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by=['date'],ascending=True)
        return df
if __name__ == '__main__':
    m = Machine()
    def print_menu():
        print('0, EXIT\n'
              '1. 종목헤드\n'
              '2. 네이버 종목컬럼명 보기\n'
              '3. 전처리결과 보기\n'
              '\n')
        return int(input('Choose one \n'))
    while True:
        menu = print_menu()
        print('Menu %s \n'%menu)
        if menu == 0:
            break
        elif menu == 1:
            m.code_df_head()
        elif menu == 2:
            print(m.test('005930'))
        elif menu ==3:

            print(m.rename_item_name(m.test('005930')))