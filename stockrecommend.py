# -*- coding: utf-8 -*-
"""stockrecommend.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n-rPjtokXJMe9URd-6jIXu-BjjOEIXaZ
"""

import pandas as pd
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import CountVectorizer

from google.colab import files 
upload = files.upload()

from google.colab import drive
drive.mount('/content/drive/constituents-financials_csv.csv')

df = pd.read_csv('constituents-financials_csv.csv')
df.head(3)

df = df.assign(stock_id=(df['Market Cap']).astype('category').cat.codes)
df.head(5)

df.shape

columns = ['Sector', 'Price', 'Dividend Yield', 'Earnings/Share', '52 Week Low', '52 Week High', 'Market Cap', 'EBITDA', 'Price/Sales']

df[columns]

#any missing values
df.isnull().sum()

#create a function to combine the values of the important columns into a single string
def get_important_features(data):
  important_features = []
  for i in range(0, data.shape[0]):
    important_features.append(str(data['Sector'][i]) + ' ' + str(data['Price'][i])+' '+str(data['Dividend Yield'][i])+' '+str(data['Earnings/Share'][i]))

  return important_features

#Create a column to hold the combine strings
df['important_features'] = get_important_features(df)

df.head(3)

#convert the text to a matrix of token counts
cm = CountVectorizer().fit_transform(df['important_features'])

#get the cosine similarity matrix from the count matrix
cs = cosine_similarity(cm)
print(cs)

#get the shape of the cosine similarity matrix
cs.shape

#get the title of the movie that the user likes
symbol = 'AAPL'

#find the movie id
stock_id = df[df.Symbol == symbol]['stock_id'].values[0]

#create a list of eumerations for the similaritiy score[(stock_id, similarity score), (...)]
scores = list(enumerate(cs[stock_id]))

#sort the list
sorted_scores = sorted(scores, key = lambda x:x[1], reverse = True)
sorted_scores = sorted_scores[1:]

print(sorted_scores)

#create a loop to print the first 7 similary stocks 
j = 0 
print('The 7 most recommended stocks to', symbol, 'are:\n')
for item in sorted_scores:
  stock_symbol = df[df.stock_id == item[0]]['Name'].values[0]                
  print(j+1, stock_symbol)
  j = j+1
  if j>6:
    break

