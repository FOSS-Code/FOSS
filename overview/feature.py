
import os
import pandas as pd

lu='/mnt/split/'
chu='/mnt/benign/'

col=['pro','packnum','timesum','ack','urg','push','reset','syn','fin','flagdf','flagmf','offset','lenmax', 'lenmin', 'lenmean', 'lenstd', 'deltamax', 'deltamin', 'deltamean', 'deltastd', 'ttlmax', 'ttlmin', 'ttlmean', 'ttlstd', 'sizemax', 'sizemin', 'sizemean', 'sizestd', 'factormax', 'factormin', 'factormean', 'factorstd', 'valuemax', 'valuemin', 'valuemean', 'valuestd','packnumfor', 'timesumfor', 'ackfor', 'urgfor', 'pushfor', 'resetfor', 'synfor', 'finfor', 'flagdffor', 'flagmffor', 'offsetfor', 'lenmaxfor', 'lenminfor', 'lenmeanfor', 'lenstdfor', 'deltamaxfor', 'deltaminfor', 'deltameanfor', 'deltastdfor', 'ttlmaxfor', 'ttlminfor', 'ttlmeanfor', 'ttlstdfor', 'sizemaxfor', 'sizeminfor', 'sizemeanfor', 'sizestdfor', 'factormaxfor', 'factorminfor', 'factormeanfor', 'factorstdfor', 'valuemaxfor', 'valueminfor', 'valuemeanfor', 'valuestdfor','packnumbac', 'timesumbac', 'ackbac', 'urgbac', 'pushbac', 'resetbac', 'synbac', 'finbac', 'flagdfbac', 'flagmfbac', 'offsetbac', 'lenmaxbac', 'lenminbac', 'lenmeanbac', 'lenstdbac', 'deltamaxbac', 'deltaminbac', 'deltameanbac', 'deltastdbac', 'ttlmaxbac', 'ttlminbac', 'ttlmeanbac', 'ttlstdbac', 'sizemaxbac', 'sizeminbac', 'sizemeanbac', 'sizestdbac', 'factormaxbac', 'factorminbac', 'factormeanbac', 'factorstdbac', 'valuemaxbac', 'valueminbac', 'valuemeanbac', 'valuestdbac']

lie=['frame.len','timedelta','ip.ttl','tcp.window_size','tcp.window_size_scalefactor','tcp.window_size_value']

for i1 in os.listdir(lu):
  w1=lu+i1+'/'
  c1=chu+i1+'.csv'
  p=pd.DataFrame()
  for i2 in os.listdir(w1):
    w2=w1+i2
    datazong=pd.read_csv(w2)
    zheng=datazong.iloc[0,3]
    datazong['dri']=-1
    datazong['dri'][datazong['ip.src']==zheng]=0
    datazong['dri'][datazong['ip.src']!=zheng]=1
    pro=0
    if datazong['udp.stream'][0]!=-1:
      pro=1
    fea=[pro]
    for fang in range(3):
      if fang==0:
        data=datazong.copy()
      if fang==1:
        data=datazong[datazong['dri']==0].copy()
      if fang==2:
        data=datazong[datazong['dri']==1].copy()
      if data.shape[0]==0:
        fea.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        continue
      timesum=data.iloc[-1,1]-data.iloc[0,1]
      data['time-1']=data['frame.time_epoch'].shift(1)
      data['timedelta']=data['frame.time_epoch']-data['time-1']
      data['timedelta'][0]=0
      fea.extend([data.shape[0],timesum,data['tcp.flags.ack'].sum(),data['tcp.flags.urg'].sum(),data['tcp.flags.push'].sum(),data['tcp.flags.reset'].sum(),data['tcp.flags.syn'].sum(),data['tcp.flags.fin'].sum(),data['ip.flags.df'].sum(),data['ip.flags.mf'].sum(),data['ip.frag_offset'].sum()])
      for l1 in lie:
        fea.extend([data[l1].max(),data[l1].min(),data[l1].mean(),data[l1].std()])
    p=pd.concat([p,pd.DataFrame(fea)],axis=1)
  p=p.fillna(0)
  (p.T).to_csv(c1,index=False,header=col)


