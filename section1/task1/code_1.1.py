import requests
import pandas as pd
import numpy as np
from datetime import datetime

class CryptoCompare():
    def __init__(self, cryptocurrency, currency):
        self.cryptoc=cryptocurrency
        self.c=currency
    
    def get_histohour_single(self,target_timestamp):
        target=target_timestamp+3600
        url="https://min-api.cryptocompare.com/data/v2/histohour?fsym={fsym}&tsym={tsym}&toTs={endts}&limit={lim}&e=binance".format(fsym=self.cryptoc,tsym=self.c,endts=target,lim=1)
        r = requests.get(url)
        ipdata = r.json()
        new=pd.DataFrame(ipdata["Data"]["Data"])
        new=new.iloc[0,:]
        return new
    
    def get_histohour_data(self,start_date,end_date):  
        total=(end_date-start_date).days*24+24
        end=end_date.timestamp()
        raw=pd.DataFrame()
        while total>2001:
            url="https://min-api.cryptocompare.com/data/v2/histohour?fsym={fsym}&tsym={tsym}&toTs={endts}&limit={lim}&e=binance".format(fsym=self.cryptoc,tsym=self.c,endts=end,lim=2000)
            r = requests.get(url)
            ipdata = r.json()
            new=pd.DataFrame(ipdata["Data"]["Data"])
            raw=pd.concat([new,raw])
            total-=2001
            end-=2001*3600    
        if total!=1:
            url="https://min-api.cryptocompare.com/data/v2/histohour?fsym={fsym}&tsym={tsym}&toTs={endts}&limit={lim}&e=binance".format(fsym=self.cryptoc,tsym=self.c,endts=end,lim=total-1)
            r = requests.get(url)
            ipdata = r.json()
            new=pd.DataFrame(ipdata["Data"]["Data"])
        else:
            new=get_histohour_single(end)
        raw=pd.concat([new,raw])
        return raw
    
    def fmt_histohour_data(raw):
        drop=[1,2]
        raw.drop(raw.columns[drop],axis=1,inplace=True)
        raw['datetime']=list(map(datetime.fromtimestamp,raw['time']))
        raw.columns=['close', 'high', 'low', 'open', 'time', 'volume', 'baseVolume','datetime']
        raw.drop(["time"],axis=1,inplace=True)
        raw.index=np.arange(len(raw))
        return raw
    
    def get_histohour_data(self,start_date,end_date):  
        total=(end_date-start_date).days*24+24
        end=end_date.timestamp()
        raw=pd.DataFrame()
        while total>2001:
            url="https://min-api.cryptocompare.com/data/v2/histohour?fsym={fsym}&tsym={tsym}&toTs={endts}&limit={lim}&e=binance".format(fsym=self.cryptoc,tsym=self.c,endts=end,lim=2000)
            r = requests.get(url)
            ipdata = r.json()
            new=pd.DataFrame(ipdata["Data"]["Data"])
            raw=pd.concat([new,raw])
            total-=2001
            end-=2001*3600    
        if total!=1:
            url="https://min-api.cryptocompare.com/data/v2/histohour?fsym={fsym}&tsym={tsym}&toTs={endts}&limit={lim}&e=binance".format(fsym=self.cryptoc,tsym=self.c,endts=end,lim=total-1)
            r = requests.get(url)
            ipdata = r.json()
            new=pd.DataFrame(ipdata["Data"]["Data"])
        else:
            new=get_histohour_single(end)
        raw=pd.concat([new,raw])
        return raw
    
    def fmt_histohour_data(raw):
        drop=[1,2]
        raw.drop(raw.columns[drop],axis=1,inplace=True)
        raw['datetime']=list(map(datetime.fromtimestamp,raw['time']))
        raw.columns=['close', 'high', 'low', 'open', 'time', 'volume', 'baseVolume','datetime']
        raw.drop(["time"],axis=1,inplace=True)
        raw.index=np.arange(len(raw))
        return raw
    
    def get_toplist_mktcap_data(self,number):
        url="https://min-api.cryptocompare.com/data/top/mktcapfull?limit={lim}&tsym=USD".format(lim=number)
        r = requests.get(url)
        ipdata = r.json()
        raw=ipdata["Data"]
        name=[]
        marketValue=[]
        for i in range(len(raw)):
            name.append(raw[i]["CoinInfo"]["Name"])
            marketValue.append(raw[i]["DISPLAY"]['USD']['MKTCAP'])
        new=pd.DataFrame({"Rank":range(1,len(raw)+1),"Name":name,"Market Value":marketValue})
        return new
        
ins=CryptoCompare("BTC","USDT")
table1=ins.get_histohour_data(datetime(2017,4,1,00),datetime(2020,4,1,23))
table1Backup=table1[:]
table1=CryptoCompare.fmt_histohour_data(table1)
table1.to_csv('BTC_USDT_1h.csv',sep=" ",index=True,header=True)

table2=ins.get_toplist_mktcap_data(100)
table2.to_csv('Rank_MarketCap.csv',sep=" ",index=False,header=True)










