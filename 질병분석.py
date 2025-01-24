import pandas as pd
import os
import matplotlib.pyplot as plt
plt.rc('font', family='malgun gothic')


def dataopen():
    path = '3rd_data/'
    file_list = os.listdir(path)
    # file_list


    df = pd.DataFrame()
    keywords = ['감기', '눈병', '천식', '피부염']
    for i in file_list:
        if i.endswith('_시도.csv'):
            # print(i)
            data = pd.read_csv(path+i, encoding='EUC_KR')
            # if '감기' in i:
            #     data['구분'] = '감기'
            # elif '눈병' in i:
            #     data['구분'] = '눈병'
            # elif '천식' in i:
            #     data['구분'] = '천식'
            # elif '피부염' in i:
            #     data['구분'] = '피부염'

            for key in keywords:
                if key in i:
                    data['구분']=key
                    break
            df = pd.concat([df, data])

            
    sido = pd.read_csv('3rd_data\시도지역코드.csv', encoding='EUC_KR')

    return df, sido

def dataprepocessing(df, sido):
    data_merge = pd.merge(df, sido,how='left', on='시도지역코드')
    data_merge['년/월'] = data_merge['날짜'].str[:7]
    df_data = data_merge[data_merge['지역명'] != '전국']
    df_data.dropna(axis=0, how='any',inplace=True)
    #년/월, 구분별 발생건수의 평균
    yearmonthdf = df_data.groupby(['년/월','구분'], as_index=False)[['발생건수(건)']].mean()

    return yearmonthdf

def visualization(yearmonthdf):
    yearmonthin = input('조회 년/월 입력 >>')
    yearmonthsearch = yearmonthdf[yearmonthdf['년/월']==yearmonthin]
    print(yearmonthsearch)
    yearmonthsearch.plot(kind='bar', x='구분', rot = 0, title=yearmonthin+' 현황')
    plt.show()


if __name__== '__main__':
    df, sido = dataopen()
    # print(df)
    # print(sido)
    yearmonthdf = dataprepocessing(df,sido)
    visualization(yearmonthdf)

