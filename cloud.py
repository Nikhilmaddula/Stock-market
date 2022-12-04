#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[4]:


from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
from nsepy import get_history


# In[5]:


portfolio = ['RELIANCE','HDFC','INFY','ICICIBANK','TCS','KOTAKBANK','HINDUNILVR','ITC','AXISBANK','LT','SBIN','BAJFINANCE','BHARTIARTL','ASIANPAINT','HCLTECH',
'MARUTI','ULTRACEMCO','M&M','SUNPHARMA','NESTLEIND','TATASTEEL','TECHM','WIPRO','BAJAJFINSV','GRASIM','POWERGRID','DRREDDY',
'INDUSINDBK','TATAMOTORS','ADANIPORTS','NTPC','HINDALCO','DIVISLAB','JSWSTEEL','BRITANNIA','CIPLA','BPCL','SHREECEM','TATACONSUM','HEROMOTOCO','ONGC','EICHERMOT','UPL','SBILIFE','COALINDIA','IOC']



# In[6]:


from datetime import date,timedelta


start_data = date.today() - timedelta(days=3)
# for i in portfolio:
#     display(get_history(symbol=i, start=start_data, end=start_data))

x = 0
for i in portfolio:
    
    if x == 0:
        data = pd.DataFrame(get_history(symbol=i , start=start_data, end=start_data))
        x=+1
    else:
        j=get_history(symbol=i, start=start_data, end=start_data)
        data = data.append(j)
    
data = data.set_index('Symbol')


# In[8]:


import numpy as np


# In[9]:


list(data.columns)
#data_mapper = data.drop(data.columns[[5,6,7,9,10,11,12]], axis = 1, inplace = True)
data_mapper = data[['Open','Close','High','Volume','Low','Prev Close']]
#print(data_mapper)
data_Volumne = data_mapper.sort_values('Volume',ascending=False)

data_mapper['Day Gain In %'] = ((data['Close'] - data['Prev Close'])/data['Close'])*100
data_daygain = data_mapper.sort_values('Day Gain In %',ascending= False)


# In[10]:


data_head = data_Volumne.head()
data_tail = data_Volumne.tail()
data_head2 = data_daygain.head()
data_tail2 = data_daygain.tail()


# In[11]:


data_head = data_head[data_head.columns[[5, 0, 1,3]]]
data_tail = data_tail[data_tail.columns[[5, 0, 1,3]]]
day_gain= [data_head,data_tail]

data_head2 = data_head2[data_head2.columns[[6, 0, 1,3]]]
data_tail2 = data_tail2[data_tail2.columns[[6, 0, 1,3]]]
volumne = [data_head2,data_tail2]


# In[12]:


day_gain=  pd.concat(day_gain)
volumne = pd.concat(volumne)


# In[13]:


day_gain.to_csv('daygain.txt')
volumne.to_csv('volumne.txt')


# In[14]:


vol = open("volumne.txt","r")

string_head = str()
string_tail = str()

for i in range(10):
    x = vol.readline().strip()
    if i <5:
        string_head = string_head +'\n'+ x 
    else : 
        string_tail = string_tail + '\n'+ x


# In[29]:


daygain = open("daygain.txt","r")

string_head_daygain = str()
string_tail_daygain = str()

for i in range(10):
    x = daygain.readline().strip()
    if i <5:
        string_head_daygain = string_head_daygain +'\n'+ x 
    else : 
        string_tail_daygain = string_tail_daygain +'\n'+ x


# In[15]:


import matplotlib.pyplot as plt
import pandas as pd
from nsepy import get_history
from datetime import date,timedelta


# In[16]:


start_date = date.today() - timedelta(days=21)
end_date = date.today() - timedelta(days=2)


# In[17]:


x=0
for i in portfolio:
    
    if x == 0:
        trial = get_history(symbol=i , start=start_date, end=end_date)
        data = pd.DataFrame(trial['Close']).transpose()
        x=+1
    else:
        j=get_history(symbol=i, start=start_date, end=end_date)
        j=j['Close'].transpose()
        data = data.append(j)


# In[18]:


x = len(list(data.columns))
#print(x)
while x < 15:
    col.clear()
    start_date1 = start_date - timedelta(days=1)
    print(start_date1)
    col = list()
    for i in portfolio:
        j=get_history(symbol=i, start=start_date1, end=start_date1)
        if len(j['Close'].values) != 0:
            j1=j['Close'].transpose()
            col.append((j1.values)[0])
        else :
            start_date1 = start_date1 - timedelta(days=1)
            continue 
    data.insert(0,start_date1,col,True)
    x=x+1


# In[19]:


data.insert(0,'Name',portfolio,True)
data.set_index("Name", inplace = True)


# In[20]:


q =  data.sum(axis=1)/15


# In[21]:


sma = data[data.columns[14]] -q
sma = pd.DataFrame(sma)


# In[22]:


sma.reset_index(level=0, inplace=True)


# In[23]:


above  = str()
below = str()


# In[24]:


for ind in sma.index:
    if sma[sma.columns[1]][ind] > 0 and sma[sma.columns[1]][ind] < 10:
        above = above + '\n' + sma['Name'][ind]
    if sma[sma.columns[1]][ind] < 0 and sma[sma.columns[1]][ind] > -10:
        below = below + '\n' + sma['Name'][ind]


# In[25]:


email_id = "bdaassgn@gmail.com"
password = "doalkifgnetzwdpt"


# In[31]:


import ssl
import smtplib # simple mail tranfer protocol
Body_of_Email = """\
Subject: Daily Stock Report


Highest ranked by Volume stocks of the day:

VOLUME        STOCKNAME CLOSE OPEN 
""" +'\n'+string_head+'\n'+ """\

Lowest ranked by Volume stocks of the day:

VOLUME        STOCKNAME CLOSE OPEN 
""" + '\n'+string_tail +'\n'+"""\

Highest ranked by day gain stocks of the day:

DAYGAIN%      STOCKNAME CLOSE OPEN
"""+'\n'+ string_head_daygain + '\n'+"""\

Lowest ranked by day gain stocks of the day:

DAYGAIN%      STOCKNAME CLOSE OPEN
"""+'\n'+ string_tail_daygain +'\n' + """\

These are the stocks to look out for which have a buy call """ + '\n'+ above +'\n' +"""\

These are the stocks to look out for which have a sell call """ + '\n'+ below +'\n'+ """\

Sincerely,
Your Computer"""
context = ssl.create_default_context()
Email_Port = 465  # If you are not using a gmail account, you will need to look up the port for your specific email host
with smtplib.SMTP_SSL("smtp.gmail.com", Email_Port, context=context) as server:
    server.login(email_id, password)  #  This statement is of the form: server.login(<Your email>, "Your email password")
    server.sendmail("bdaassgn@gmail.com", "nikhilmaddula2060@gmail.com", Body_of_Email)  # This statement is of the form: server.sendmail(<Your email>, <Email receiving message>, Body_of_Email)

