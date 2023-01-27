
# calc DIFF、DEA、MACD
def MACD(short ,long, middle):
    data['DIFF'] = locals().get('EMA{}'.format(short)) - locals().get('EMA{}'.format(long))
    data['DEA'] = data['DIFF'].ewm(alpha=2 / (middle+1), adjust=False).mean()
    data['MACD'] = 2 * (data['DIFF'] - data['DEA'])
    
# 1st trading day，DIFF、DEA、MACD=0
    data.loc[0,['DIFF','DEA','MACD']]=0

    return data 

#cal kdj
def kdj(data,n=34,m1=3,m2 = 3):
    data['rolling_high'] = (data['adj_high'].rolling(window = n, min_periods = 1).max()).fillna(0)
    data['rolling_low'] = (data['adj_low'].rolling(window = n, min_periods = 1).min()).fillna(0)
    data['fastk'] =  [i*100/j if j!=0 else 0 for i,j  in zip((data['close'] - data['rolling_low']), (data['rolling_high'] - data['rolling_low']))   ]
    data['fastd'] = data['fastk'].ewm(com = m1-1, adjust = False).mean()
    data['K'] = data['fastd']
    data['D'] = data['K'].ewm(com = m2-1, adjust = False).mean()
    
    return data.fillna(value=0)


#get all opened stock code and other info

# sma函数；c/列表，n/周期，m/权重，返回sma列表


#SMA(X,N,M),X's N days moving average, M is weight ,if Y=SMA(X,N,M) then Y=(X*M+Y'*(N-M))/N=x*(m/n)+y'(1-m/n)


def get_sma(c, n, m):
    c_re = [c[0]]
    for i in range(1, len(c)):
        sma_temp = c[i]*(m/n) + c_re[i-1]*(1 - (m/n))
        c_re.append(sma_temp)
    return c_re

#用法:SMA(X,N,M),X的N日移动平均,M为权重,若Y=SMA(X,N,M)则Y=(X*M+Y'*(N-M))/N=x*(m/n)+y'(1-m/n)
# 平滑rsi函数；输入一个列表和周期，返回rsi列表
# is0为True的时候，将首个值赋0，序列少的时候使用，软件中就是这样


def rsi(data, n=9, m=1 ):
     # input X: list，N: period for calc sma,  M: weight, return RSI to dataframe
    data.loc[:,['diff']] = data['adj_close']-data['adj_close'].shift(1)
    data = data.fillna(value=0)
    data.loc[:,['max_diff']] = np.maximum(data['diff'],0)
    data.loc[:,['abs_diff']] = np.abs(data['diff'])
    max_diff = np.array(get_sma(np.array(data['max_diff']), n, m))
    abs_diff = np.array(get_sma(np.array(data['abs_diff']), n, m))
    
    data.loc[:,['rsi_{}'.format(n)]] = np.array([round(e_temp, 3) if e_temp != np.inf and not np.isnan(e_temp) else 0 
             for e_temp in max_diff*100/abs_diff ])
    
    return data

# DMA  Y=A*X+(1-A)*Y'
def get_dma(x,a):
# DMA(AMOUNT/(100*volume),volume/CAPITAL);
# DIF:=(EMA(CLOSE,SHORT)-EMA(CLOSE,LONG))*100/EMA(CLOSE,LONG);
# DEA:=EMA(DIF,MIDDLE);
    for i in range(0, len(x)):
        if i==0:
            c_re = [x[0]]
        if i>0 :
            
            dma_temp = x[i]*a[i] + c_re[i-1]*abs(1-a[i]) 
            
            
            c_re.append(dma_temp)    
        
    return np.asarray(c_re)
#calc marketing average cost (MCST)
def get_avg_cost(data,short = 7, long = 11, peri = 9):
    
    
    
    amount = data.amount
    volume = data.volume
    float_share = data.fc
    
    x = amount/volume
    a = volume/(float_share)
    
    locals()['EMA{}'.format(short)] = data['close'].ewm(alpha=2 / (short+1), adjust=False).mean()
    locals()['EMA{}'.format(long)] = data['close'].ewm(alpha=2 / (long+1), adjust=False).mean()
    data.loc[:,'avg_cost']=get_dma(x.fillna(0).values,a.values)
    data.loc[:,'avg_dif'] = (locals().get('EMA{}'.format(short)) -locals().get('EMA{}'.format(long)))*100/locals().get('EMA{}'.format(long))
    data.loc[:,'avg_dea'] = data['avg_dif'].ewm(alpha=2 / (peri+1), adjust=False).mean()
    
    return data
    


    
    return data

Calc EMA BBI LINE 
def embbi(data,malist=[2,3,5,8,13,21]):
    
    data.loc[:,'embbi'] = sum([(data['close'].ewm(alpha=2 / (i+1), adjust=False).mean()).fillna(value=0) for i in malist])/len(malist)
    
    return data
def bbi(data,malist=[2,3,5,8,13,21]):
    
    data.loc[:,'bbi'] = sum([(data['close'].rolling(i).mean()).fillna(value=0) for i in malist])/len(malist)
    
    return data
        
Calc boolean_belt
def boolean_belt(data,n=11,m=2):
    
    bool_std= (data['bbi'].rolling(window=n,min_periods=1).std()).fillna(value=0)
    
    data.loc[:,'bbi_bool_upr'] = data['bbi']+2*bool_std
    data.loc[:,'bbi_bool_dwn'] = data['bbi']-2*bool_std
    
    return data
  

