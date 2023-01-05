import csv
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as md
from datetime import date, datetime, timedelta
import datetime
from dateutil import rrule

plt.rcParams["date.autoformatter.month"] = "%b %Y"
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['font.size'] = 12


'''
流感併發重症
侵襲性肺炎鏈球菌感染症(IPD)
腸病毒健保就診人次
'''

# 匯入資料
df_flu = pd.read_csv('Flu_severe.csv')
df_ipd = pd.read_csv('IPD.csv')
df_ev = pd.read_csv('EV_Visits.csv')
df_ev_sc = pd.read_csv('EV_severe.csv')



#建立計算病例數之自訂函數
def case_sum(s_year, e_year, mask_info, data, info, target):
    for i in range(s_year,e_year):
        mask = (data[mask_info]==i)
        x = data[mask]
        print('{:d}年{}為:{:d}'.format(i,info,x[target].values.sum()))
    print()
    
lis_yearsum = []
def case_sum1(mask_info, data, info, target):
    for i in range(2008,2023):
        mask = (data[mask_info]==i)
        x = data[mask]
        lis_yearsum.append(x[target].values.sum())

        
# 統計每年流感併發重症之人數
case_sum(2005, 2022, '研判年份', df_flu, '流感併發重症人數', '確定病例數')

# 統計每年侵襲性肺炎鏈球菌感染症之人數
case_sum(2007, 2023, '研判年份', df_ipd, '侵襲性肺炎鏈球菌感染人數', '確定病例數')

# 統計每年腸病毒健保就診人次之人數
case_sum(2008, 2023, '年', df_ev, '腸病毒健保就診人次', '腸病毒健保就診人次')

# 統計每年腸病毒感染併發重症之人數
case_sum(2003, 2023, '發病年份', df_ev_sc, '腸病毒感染併發重症人數', '確定病例數')
#https://od.cdc.gov.tw/eic/NHI_EnteroviralInfection.json



years = list(range(2008,2023))

def fig_show_year(info):
    plt.figure(dpi=300,figsize=(10,4))
    plt.bar(years, y, label=info)
    plt.legend()
    plt.xlabel('年')
    plt.ylabel('人\n數',rotation=0)
    plt.xticks(years,rotation=45)
    plt.title(info)
    plt.show()

lis_yearsum = []
case_sum1('研判年份', df_flu, '流感併發重症人數', '確定病例數')
y = lis_yearsum
fig_show_year('流感併發重症人數')

lis_yearsum = []
case_sum1('研判年份', df_ipd, '侵襲性肺炎鏈球菌感染人數', '確定病例數')
y = lis_yearsum
fig_show_year('侵襲性肺炎鏈球菌感染人數')

lis_yearsum = []
case_sum1('年', df_ev, '腸病毒健保就診人次', '腸病毒健保就診人次')
y = lis_yearsum
fig_show_year('腸病毒健保就診人次')

lis_yearsum = []
case_sum1('發病年份', df_ev_sc, '腸病毒感染併發重症人數', '確定病例數')
y = lis_yearsum
fig_show_year('腸病毒感染併發重症人數')



# 以週為單位計算

lis_weeksum = []
def case_sum_week2(s_year, e_year, mask_info1, mask_info2, data, info, target):
    for i in range(s_year,e_year):
        mask1 = (data[mask_info1]==i)
        # print('{:d}年'.format(i))
        for j in range(1,54):
            mask2 = (data[mask_info2]==j)
            x = data[mask1 & mask2]
            lis_weeksum.append(x[target].values.sum())
            # lis_year.append(i)
            
            
# 繪製圖表

def fig_show(info,height):
    plt.figure(dpi=300,figsize=(30,height))
    plt.bar(dates, y, label=info,width=5)
    plt.legend()
    plt.xlabel('月份')
    plt.ylabel('人\n數',rotation=0)
    plt.xticks(rotation=45)
    plt.xlim(date(2019,12,25),date(2022,4,11))
    plt.title(info)
    plt.show()
    
    
    
# 流感併發重症
case_sum_week2(2020, 2023, '研判年份','研判週別', df_flu, '流感併發重症人數', '確定病例數')

  # 數據整理
week = (rrule.rrule(rrule.WEEKLY, dtstart = date(2020,1,1), until = date(2022,4,3)).count()+1)
lis_weeksum = lis_weeksum[:week]
dates = np.array([date(2020,1,1) + datetime.timedelta(weeks=i) for i in range(119)])
y = lis_weeksum


fig_show('流感併發重症人數',6)



# 侵襲性肺炎鏈球菌
lis_weeksum = []
case_sum_week2(2020, 2023, '研判年份','研判週別', df_ipd, '侵襲性肺炎鏈球菌感染人數', '確定病例數')

  # 數據整理
lis_weeksum.pop(105)
lis_weeksum = lis_weeksum[:week]
dates = np.array([date(2020,1,1) + datetime.timedelta(weeks=i) for i in range(week)])
y = lis_weeksum

fig_show('侵襲性肺炎鏈球菌感染人數',6)



# 腸病毒就診人數
lis_weeksum = []
case_sum_week2(2020, 2023, '年','週', df_ev, '腸病毒健保就診人次', '腸病毒健保就診人次')

  # 數據整理
lis_weeksum.pop(105)
lis_weeksum = lis_weeksum[:week]
dates = np.array([date(2020,1,1) + datetime.timedelta(weeks=i) for i in range(week)])
y = lis_weeksum

fig_show('腸病毒健保就診人次',6)


# 腸病毒併發重症
lis_weeksum = []
case_sum_week2(2020, 2023, '發病年份','發病週別', df_ev_sc, '腸病毒感染併發重症人數', '確定病例數')

  # 數據整理
lis_weeksum.pop(105)
lis_weeksum = lis_weeksum[:week]
dates = np.array([date(2020,1,1) + datetime.timedelta(weeks=i) for i in range(week)])
y = lis_weeksum

fig_show('腸病毒感染併發重症人數',6)


# COVID-19確診數
  # 讀取json檔
cov = pd.read_json('Weekly_19CoV.json')

lis_weeksum = []
case_sum_week2(2020, 2023, '發病年份','發病週別', cov, '新冠肺炎確診人數', '確定病例數')
  # 數據整理
lis_weeksum.pop(105)
lis_weeksum = lis_weeksum[:week]
y = lis_weeksum
dates = np.array([date(2020,1,1) + datetime.timedelta(weeks=i) for i in range(week)])
fig_show('新冠肺炎確診人數',12)




# 錯誤寫法
# dates = np.array([date(2022,4,3) - datetime.timedelta(weeks=i) for i in range(len(week))])
# plt.figure(dpi=300,figsize=(30,6))
# plt.bar(dates, y, label='流感併發重症人數')
# plt.legend()
# plt.xlabel('週')
# plt.ylabel('人數')
# plt.xticks(rotation=45)
# plt.title('流感併發重症人數')

# plt.show()
