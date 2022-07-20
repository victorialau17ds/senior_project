# -*- coding: utf-8 -*-
"""kmeans_clustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_JOwSIk2RjkXaJz7ib_IHPcE4YB-Zzbm
"""

# Commented out IPython magic to ensure Python compatibility.
'''main'''
import pandas as pd 
import numpy as np 
import os, time 
import pickle, gzip

'''Data viz'''
import matplotlib.pyplot as plt
import seaborn as sns 
color = sns.color_palette()
# %matplotlib inline 

'''Data Prep and Model Evaluation'''
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, average_precision_score 
from sklearn.metrics import roc_curve, auc, roc_auc_score

df = pd.read_csv("/content/drive/MyDrive/CSE 499 Senior Project/data files/constituents-financials.csv")
df.head()

df1 = df.iloc[:, 5:7].values

import scipy.cluster.hierarchy as shc

plt.figure(figsize=(10, 7))
plt.title("stocks hierarchy")
dend = shc.dendrogram(shc.linkage(df1, method = 'ward'))

from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=2,
                                  affinity='euclidean',
                                  linkage='ward'
                                  )
cluster.fit_predict(df1)

plt.figure(figsize=(10,7))
plt.scatter(df1[:,0], df1[:,1], c=cluster.labels_,
            cmap='rainbow')

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[("encoder", OneHotEncoder(),[-1])], remainder="passthrough")
X_train = np.array(ct.fit_transform(X))
X.head()



from sklearn.cluster import KMeans

kmeans = KMeans(n_cluster=4)

!pip install -q yfinance

import yfinance as yf
import pandas as pd 
import warnings 
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

stock_list = pd.read_csv("/content/drive/MyDrive/CSE 499 Senior Project/data files/constituents-financials.csv")['Symbol']
#drop_list = ['MCK', 'KMB']
#stock_list = pd.Seriesstock_list[stock_list.Symbol.isin(drop_list) == False]

df = pd.DataFrame(columns=['ROE(%)', 'Beta'])
bad_tickers = []

for i in stock_list:

  stock = yf.Ticker(i)
  try:
    ROE = stock.financials.loc['Net Income']/stock.balance_sheet.loc['Total Stockholder Equity'] * 100
    Mean_ROE = pd.Series(ROE.mean())
    Beta = pd.Series(stock.get_info()['beta'])

    values_to_add = {'ROE(%)': Mean_ROE.values[0].round(2), 'Beta' : Beta.values[0].round(2)}
    row_to_add = pd.Series(values_to_add, name=i)
    df = df.append(row_to_add)
    #print('Downloaded:',i)
  except:
    bad_tickers.append(i)

stock_list = pd.read_csv("/content/drive/MyDrive/CSE 499 Senior Project/data files/constituents-financials.csv")['Symbol']

df = pd.DataFrame(columns=['Volatility', 'Beta'])
bad_tickers = []

for i in stock_list:

  stock = yf.Ticker(i)
  try:
    log_return = np.log(stock.financials.loc['Close']/stock.financials.loc['Close'].shift())
    Volatility = log_return.std() *252**.5
    #Mean_ROE = pd.Series(ROE.mean())
    #Volatility = pd.Series(stock.get_info()['volatility'])
    Beta = pd.Series(stock.get_info()['beta'])

    values_to_add = {'Volatility': Volatility.values[0].round(2), 'Beta' : Beta.values[0].round(2)}
    row_to_add = pd.Series(values_to_add, name=i)
    df = df.append(row_to_add)
    #print('Downloaded:',i)
  except:
    bad_tickers.append(i)

#bad_tickers

df1 = df.copy()

#preprocessing  
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df_values = scaler.fit_transform(df1.values)

print(df_values)

#fit df_values into kmeans model
from sklearn.cluster import KMeans

km_model = KMeans(n_clusters = 16).fit(df_values)

#assign cluster to each stock
clusters = km_model.labels_

df1['cluster'] = clusters
df1

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12,8))

sns.set_style('whitegrid')
ax = sns.scatterplot(y="ROE(%)", x = "Beta",
                     edgecolor ='face',
                     hue="cluster",
                     data = df1,
                     palette = 'bright',
                     s = 60)

plt.xlabel('Beta', size=17)
plt.ylabel('ROE(%)', size=17)
plt.setp(ax.get_legend().get_texts(), fontsize='17') #for text in legend 
plt.setp(ax.get_legend().get_title(), fontsize='17') #for title in legend 
plt.title('Clusters from KMeans algorithm with k=16', fontsize='x-large')

for i in range(0, df1.shape[0]):
  plt.text(df1.Beta[i]+0.07, df1['ROE(%)'][i]+0.01,
           df1.index[i],
           horizontalalignment='right',
           verticalalignment='bottom',
           size='small',
           color='black',
           weight='semibold')