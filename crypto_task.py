import csv
import os
import sqlite3
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs




class cryptodata:
    def __init__(self, filename):
       self.filename=filename

    """
       :param conn: filename.csv ( from binance)
       :return:  dataset with closing price, ema20, ema200, connection object
    """

    def toDataFrame(self):
        dataset = pd.read_csv(self.filename, sep = ',', decimal=',',skiprows=1)
        nRow, nCol = dataset.shape
        print(f'There are {nRow} rows and {nCol} columns')
        print(' ')
        print(dataset.isna().sum())
        dataset.dropna(inplace=True)
        print(dataset.isna().sum())
        # Expand = True , It will expand out into separate columns
        dataset[['date', 'time']] = dataset['date'].str.split(' ', 1, expand=True)

        # Convert dataset["date"] to datetime
        dataset["date"] = pd.to_datetime(dataset["date"], infer_datetime_format=True)

        dataset.index = dataset["date"]


        new_dataset = pd.DataFrame(dataset["close"])
        new_dataset[["close"]] = new_dataset[["close"]].apply(pd.to_numeric, errors='ignore')

        # Calculate EMA_20

        new_dataset["EMA_200"] = new_dataset.iloc[:, 0].ewm(span=200, adjust=False).mean()
        plt.figure()
        plt.plot(new_dataset["EMA_200"], label='EMA_200')
        # Calculate EMA_200

        new_dataset["EMA_20"] = new_dataset.iloc[:, 0].ewm(span=20, adjust=False).mean()

        # Write records stored in a DataFrame to a SQL database.
        conn = sqlite3.connect('database.db')

        c = conn.cursor()

        table_name = self.filename[:-4]

        createTable = "create table if not exists " + table_name + " (close float, ema_200 float, ema_20 float);"

        c.execute(createTable)

        new_dataset.to_sql(table_name, conn, if_exists='replace',index=True)
        conn.commit()
        print(pd.read_sql_query("select * from sqlite_master where type='table'", conn))
        print(pd.read_sql_query("PRAGMA table_info('Binance_BTCUSDT_d')", conn))
        items = c.execute("select * from Binance_BTCUSDT_d LIMIT 3")
        for i in items:
            print(i)
        print(new_dataset.head(3))
        return new_dataset, conn



