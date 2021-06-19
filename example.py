# -*- coding: utf-8 -*-

import requests
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

basedir='D:/bitcoin/showcase';
predict=40; # 窗口为多少的时间序列数据

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

url = "https://api.coincap.io/v2/assets/bitcoin/history?interval=m1"
payload = {}
headers= {}

arrres = requests.request("GET", url, headers=headers, data = payload).json()
# arrres=json.loads(response.text.encode('utf8'))
btclist=[];

if(not os.path.exists(basedir)):
    os.mkdir(basedir)

def saveCSV(ilt):
    columns_list=['time','前40','前39','前38','前37','前36','前35','前34','前33','前32','前31','前30','前29','前28','前27','前26','前25','前24','前23','前22','前21','前20','前19','前18','前17','前16','前15','前14','前13','前12','前11','前10','前9','前8','前7','前6','前5','前4','前3','前2','前1','当前']

    print(len(columns_list))
    df=pd.DataFrame(ilt,columns=columns_list)
    df.head(int(len(df)*0.8)).to_csv(basedir+'/btc_training.csv',index=False,encoding="gbk")
    df.tail(int(len(df)*0.2)).to_csv(basedir+'/btc_scoring_raw.csv',index=False,encoding="gbk")
    #输出打分数据
    cur=df
    del cur['当前']
    cur.tail(int(len(df)*0.2)).to_csv(basedir+'/btc_scoring.csv',index=False,encoding="gbk")
def out_ten(i):
    tmplist=[]
    tmplist.append(arrres['data'][i]['date'])
    for j in range(i-predict,i+1): #到i本身
        tmplist.append(arrres['data'][j]['priceUsd'])
    return tmplist;
for i in range(predict,len(arrres['data'])):
    btclist.append(out_ten(i))
    
saveCSV(btclist)
