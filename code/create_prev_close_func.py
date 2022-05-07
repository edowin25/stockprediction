# %% [markdown]
# ## Part 1: Feature Engineering
# - This script is used to create the features required for the model to learn

# %%
import datetime
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
from pandas_datareader import data as pdr

from ta.volatility import BollingerBands

# %% [markdown]
# ### 1. Setting the start and end date to request stock data from yfinance

# %%
days_sub = datetime.timedelta(1)
start_date = '2016-01-01'
end_date = datetime.date.today() - days_sub
# end_date = '2022-04-28'

# %% [markdown]
# ### 2. Request stock data from yfinance and filtering adjusted close column

# %%
tick = 'AAPL'

yf.pdr_override()

df_raw = pdr.get_data_yahoo(tick, start = start_date, end = end_date)

# %%
df_raw.reset_index().iloc[22]

# %%
plt.plot(df_raw['Adj Close'])

# %%
df = df_raw.filter(['Adj Close'])
df

# %% [markdown]
# ### 3. Create features for the model
# - Create 1 to 3 days lag prices data 
# - Calculate Bollinger Band Data
# - Combining all data created with Adj Close as label

# %%
# form df with prev close of 3 days
def create_prev_close_df(df, col_name:str):
    count = 3
    while count > 0:
        df[f"D_m{count}"] = df[col_name].shift(count)
        count -= 1
    #rearrange df with more days shift at the start -  here need to make it more dynamic
    df = df[[f"D_m{3}", f"D_m{2}", f"D_m{1}",col_name]]
    
    return df


# %%
df_main = create_prev_close_df(df, "Adj Close")
df_main

# %%
#Calc Bollinger Band(Volatility)
## Shift bband data down by 1 as we are using previous day
bb_data = BollingerBands(df['Adj Close']).bollinger_wband()
df_bb = pd.DataFrame(bb_data).shift(1)
df_bb

# %%
df_train = df_main.merge(df_bb, how = "left", left_index =  True, right_index=True)
df_train = df_train.dropna()
df_train = df_train.rename(columns = {'bbiwband':'bb_m1'})
df_train = df_train.reset_index()


# %%
#Check if there are null values
df_train.isnull().sum()

# %%
df_train.info()

# %% [markdown]
# ### 4.Treatment of features
# - transformation using pct_change
# - data splitting through slicing

# %%
# To create col of previous close price for comparison
df_train['prev_close'] = df_train['D_m1']
df_train

# %%
#pct change prices and bb
df_train[['bb_m1', 'D_m3', 'D_m2', 'D_m1','Adj Close']] = df_train[['bb_m1', 'D_m3', 'D_m2', 'D_m1', 'Adj Close']].pct_change()
df_train = df_train.dropna().reset_index(drop=True)
df_train

# %%
#split into dates, x , y data
dates = df_train[['Date']]
x = df_train[['bb_m1', 'D_m3', 'D_m2', 'D_m1',]]
y = df_train[['Adj Close']]
print(dates)
print(x)
print(y)

# %%
#Train-val-test split
pct_lm = int(len(df_train)*0.85) 
pct_um = int(len(df_train)*0.92) 

dates_train, x_train, y_train = dates.loc[:pct_lm-1],x.loc[:pct_lm-1], y.loc[:pct_lm-1]
dates_val,x_val, y_val = dates.loc[pct_lm:pct_um-1],x.loc[pct_lm:pct_um-1], y.loc[pct_lm:pct_um-1]
dates_test,x_test, y_test = dates.loc[pct_um:],x.loc[pct_um:], y.loc[pct_um:]

# %%
dates_val,x_val, y_val

# %%
x_train

# %%
plt.figure(figsize=(16,4))
sns.heatmap(x_train.corr(),annot =True, annot_kws={"fontsize":12})

#Little correlation between features which shows that they are independent

# %%
fig,axis = plt.subplots(2,2,figsize=(14,7))
sns.histplot(x_train.iloc[:,0],ax = axis[0,0])
sns.histplot(x_train.iloc[:,1],ax = axis[0,1])
sns.histplot(x_train.iloc[:,2],ax = axis[1,0])
sns.histplot(x_train.iloc[:,3],ax = axis[1,1])

plt.show()

#Graphical visualisation also shows that with pct_change, data is normalised for modelling

# %% [markdown]
# ### 5. Creating validation and test set for prediction and evaluation

# %%
x_val = x_val.reset_index(drop=True)
x_val

# %%
x_test = x_test.reset_index(drop = True)
x_test


