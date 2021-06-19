# BTCwithNeuralNet
# 使用神经网络(Neural Net)预测比特币价格
* 项目代码压缩包密码见简历
## 工具：

Python  Requests、Pandas、Numpy、Matplotlib等研究库；

开源数据挖掘工具Rapidminer；

Coincap比特币分钟级价格数据API。

## 构想：

区块链技术应用到加密货币上，使得一系列新型加密货币迅速发展。比特币作为加密货币中的翘楚，具有“去中心化”的特点。与各国央行发行的传统货币和数字货币相比，比特币在美国等国家已经出现支付职能的现象。许多商家开始直接收比特币。据Coin Desk估算, 目前全球大约有60000个商家接受比特币。在线下世界, 大概有4000个经营场所允许使用比特币, 其中, 食品经营场所占多数。[1]人们对比特币似乎和法币一样，具有投机性需求和交易性需求。

比特币交易所的出现, 鼓励投资者用各国法币进行兑换。在大量投资者参与下, 比特币价格一路上升, 从最初的零点几美元, 到2013年11月29日, 仅用了四年时间, 就达到历史高峰, 盘中高达1242美元 (如图1所示) , 一度超过1盎司黄金, 当时仅公开交易的比特币市值高达144亿美元。[1]

![1624075378442](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624075378442.png)

![1624075356941](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624075356941.png)

（图片来源：https://www.sohu.com/a/458249973_120969658）

由于监管缺失，相比基金、期货、股票等金融工具，比特币成为一种完美的金融投机对象。投机因素是比特币价格泡沫产生的主要原因。另外，比特币的优点被过度夸大而产生的价值高估,以及可能存在的市场操控，也是比特币价格泡沫得以长期存在的重要因素。[2]



为此，我希望通过本次研究，能够建立一个预测比特币价格的模型，从而试图规避价格泡沫，降低投资风险，辅助交易员进行投资决策。



## 概述

最开始本次实验发生在2020年7月，但是由于距离当前时间较为久远，故选取最新数据以使得模型更符合当前市场状况。采集从2021-06-18T05:10:00.000Z-2021-06-19T04:29:00.000Z的五分钟级比特币-美元价格，生成窗口为40的时间序列数据，将80%设置为训练数据，20%设置为打分数据，利用开源数据挖掘工具Rapidminer和神经网络（Neural Net）模型训练、应用预测模型，并对比原始结果进行打分，最终评判该模型的预测准确度。



## 可复现过程：

### 1. 使用Python下载比特币(BTC)兑美元(USD)价格示例数据

数据来源：https://api.coincap.io/v2/assets/bitcoin/history?interval=m5

时间戳范围：2021-06-18T05:10:00.000Z-2021-06-19T04:29:00.000Z


（完整代码见example.py）

```
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
```



### 2. 生成时间序列数据

**窗口大小：40**

（完整代码见example.py）

```
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
```



### 3. 导入Rapidminer，拖动操作器建立并应用模型

#### 导入数据

![1624075317013](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624075317013.png)

#### 标记数据

![1624075455387](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624075455387.png)

#### 建立模型并执行

![1624075420086](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624075420086.png)



#### 输出结果

![1624077588848](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624077588848.png)



![1624077603695](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624077603695.png)

### 4. 将结果导入到Excel进行分析

![1624077641812](https://vincentvor.github.io/imgpages/btcwithnn.assets/1624077641812.png)



## 结果

经过多次测试，使用窗口为40的时间序列和Training Cycles为200的数据准确性较高，达到了54.58%。



### 局限性

观察到结果数值的方差较大，为1158580.234。并且，在实验过程中，窗口为20的数据甚至出现了50%的准确率，因此该模型对于投研决策的效果存疑，并有待进一步检验。

希望能够用Python实现全部的NN/Decision Tree/ LSTM模型，结合前端展示，实现比特币价格实时采集、预测价格实时更新，并定期自动优化模型。



## 参考文献

[1]闵敏,柳永明.互联网货币的价值来源与货币职能——以比特币为例[J].学术月刊,2014,46(12):97-108.

[2]邓伟.比特币价格泡沫:证据、原因与启示[J].上海财经大学学报,2017,19(02):50-62.

[3]陈豪. 比特币的经济学分析[D].浙江大学,2015.

[4]李继红,吴筱潇,燕浩扬.基于VEC模型的比特币的需求与价格关系研究[J].西南民族大学学报(自然科学版),2016,42(06):702-708.

[5]李靖.运用BP神经网络构建比特币市场预测模型[J].财会月刊,2016(21):33-36.
 
