import os
import sqlite3
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd
from pandas.plotting import scatter_matrix
import  scipy


conn = sqlite3.connect('crypto.db')

price=pd.read_sql_query("select * from price",conn)


# Expand = True , It will expand out into separate columns

price[['Date', 'time']] = price['Date'].str.split(' ', 1, expand=True)

# Drop time column

price = price.drop(columns=['time'])

price["Date"] = pd.to_datetime(price["Date"], infer_datetime_format=True)

# Drop column with nan
price.dropna(axis=1, how='all',inplace=True)

price.index = price["Date"]

price = price.drop(columns=['Date'])


# Drop date column

# Expected return for ETH
exp_rets=price['ETH']/price['ETH'].shift(1)-1





#Analysing competitors cryptocurrencies

rets=price.pct_change() # % change between the current and prior

corr=rets.corr()

plt.figure()
plt.scatter(rets.ETH, rets.LINK)
plt.xlabel('return ETH')
plt.ylabel('return LINK')

plt.show()

plt.figure()
scatter_matrix(rets, diagonal='kde', figsize=(10, 10))
plt.show()

plt.figure()
plt.imshow(corr, cmap='hot', interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns)
plt.yticks(range(len(corr)), corr.columns)

plt.show()


# Plot expected return vs risk
plt.figure()
plt.scatter(rets.mean(), rets.std())
plt.xlabel('Expected returns')
plt.ylabel('Risk')
# for label, x, y in zip(rets.columns, rets.mean(),
#                        rets.std()):
#     plt.annotate(
#         label,
#         xy=(x, y), xytext=(20, -20),
#         textcoords='offset points', ha='right', va='bottom',
#         bbox=dict(boxstyle='round,pad=0.5', fc='yellow',
#                   alpha=0.5),
#         arrowprops=dict(arrowstyle='->',
#                         connectionstyle='arc3,rad=0'))
#
# plt.show()
