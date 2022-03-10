import csv
import os
import sqlite3
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os


def set_database(filename1,filename2):
    dataset1 = pd.read_csv(filename1, sep = ',', decimal=',',skiprows=1)
    dataset2 = pd.read_csv(filename2, sep = ',', decimal=',',skiprows=1)



    dataset1.dropna(inplace=True)
    dataset2.dropna(inplace=True)

    # Expand = True , It will expand out into separate columns
    dataset1[['date', 'time']] = dataset1['date'].str.split(' ', 1, expand=True)
    dataset2[['date', 'time']] = dataset2['date'].str.split(' ', 1, expand=True)

    # Convert dataset["date"] to datetime
    dataset1["date"] = pd.to_datetime(dataset1["date"], infer_datetime_format=True)
    dataset2["date"] = pd.to_datetime(dataset2["date"], infer_datetime_format=True)


    cleansed1 = dataset1.drop(columns=['time', 'tradecount'])
    cleansed2 = dataset2.drop(columns=['time', 'tradecount'])

    cleansed1.rename(columns={cleansed1.columns[7]:"Volume_crypto"},inplace=True)
    cleansed1.rename(columns={cleansed1.columns[8]: "Volume_USDT"}, inplace=True)

    cleansed2.rename(columns={cleansed2.columns[7]: "Volume_crypto"},inplace=True)
    cleansed2.rename(columns={cleansed2.columns[8]: "Volume_USDT"},inplace=True)


    table_name1 = filename1.split('.')[0]
    table_name2 = filename2.split('.')[0]
    column1=filename1.split('_')[1].replace("USDT","")
    column2=filename2.split('_')[1].replace("USDT","")



    conn = sqlite3.connect('database.db')

    c = conn.cursor()


    createTable1 = "create table if not exists " + table_name1 + " (unix float, date text,\
        symbol text, open float, high float,low float, close float, Volume_crypto float, Volume_USDT float);"
    c.execute(createTable1)

    createTable2 = "create table if not exists " + table_name2 + " (unix float, date text,\
            symbol text, open float, high float,low float, close float, Volume_crypto float, Volume_USDT float);"

    c.execute(createTable1)

    c.execute(createTable2)

    cleansed1.to_sql(table_name1,conn,if_exists='replace',index=False)
    cleansed2.to_sql(table_name2, conn, if_exists='replace',index=False)
    conn.commit()
    table='price'
    sql1 = "CREATE TABLE " + table + " as SELECT " + table_name1 + ".date as Date, " + table_name1 + ".close as " + column1 + ", " + table_name2 + ".close as " + column2+\
 " FROM " + table_name2 + ", " + table_name1 + " where " + table_name2 + ".date=" + table_name1 + ".date"


    c.execute(sql1)

    conn.commit()
    return conn


def add(filename,conn):
    dataset = pd.read_csv(filename, sep = ',', decimal=',',skiprows=1)

    dataset.dropna(inplace=True)

    # Expand = True , It will expand out into separate columns
    dataset[['date', 'time']] = dataset['date'].str.split(' ', 1, expand=True)

    # Convert dataset["date"] to datetime
    dataset["date"] = pd.to_datetime(dataset["date"], infer_datetime_format=True)

    #dataset.index = dataset["date"]
    cleansed = dataset.drop(columns=['time', 'tradecount'])

    cleansed.rename(columns={cleansed.columns[7]:"Volume_crypto"},inplace=True)
    cleansed.rename(columns={cleansed.columns[8]: "Volume_USDT"}, inplace=True)

    table_name1 = filename.split('.')[0]
    column = filename.split('_')[1].replace("USDT", "")

    conn = sqlite3.connect('database.db')

    c = conn.cursor()


    sql_addcolumn="alter table price add column {0} float".format(column)

    c.execute(sql_addcolumn)


    sql_createTable = "create table if not exists {0} (unix float, date text,\
            symbol text, open float, high float,low float, close float, Volume_crypto float, Volume_USDT float)".format(table_name1)
    c.execute(sql_createTable)
    cleansed.to_sql(table_name1, conn, if_exists='replace',index=False)

    # Update price table

    sql_updatetable="update price set {1}=(select close from {0} where price.Date={0}.date)".format(table_name1,column)
    print(sql_updatetable)
    c.execute(sql_updatetable)

    conn.commit()

    return conn



if __name__=='__main__':
    csv_files = [file for file in os.listdir(os.getcwd()) if file.endswith('.csv')]
    c_1=set_database(csv_files[0],csv_files[1])
    c_2=add(csv_files[2],c_1)
    c_3=add(csv_files[3],c_2)
    c_4=add(csv_files[4],c_3)















#conns=list(map(toDataFrame,csv_files))
# sql = """
#     SELECT TimeSeriesValue
#     FROM dbo.TimeSeriesPosition
#     WHERE
#     TimeSeriesTypeID = {0} AND
#     FundID = {1} AND
#     SecurityMasterID = 45889 AND
#     EffectiveDate = '{2}'""".format(self.LAST_PRICE_ID, self.FUND_ID, date)
#final=conns[-3]

# sql3="SELECT Binance_BTCUSDT_d.close as BTC, Binance_BTCUSDT_d.date as Date, Binance_ETHUSDT_d.close as ETH FROM Binance_BTCUSDT_d, Binance_ETHUSDT_d;"
#
# sql3="SELECT Binance_BTCUSDT_d.close as BTC, Binance_ETHUSDT_d.close as ETH FROM Binance_BTCUSDT_d INNER JOIN Binance_ETHUSDT_d on Binance_BTCUSDT_d.date=Binance_ETHUSDT_d.date"
#
# sql1="SELECT Binance_BTCUSDT_d.close as BTC, Binance_ETHUSDT_d.close as ETH FROM Binance_BTCUSDT_d, Binance_ETHUSDT_d where Binance_BTCUSDT_d.date=Binance_ETHUSDT_d.date"
#
#
# sql1="CREATE TABLE new as SELECT Binance_BTCUSDT_d.close as BTC Binance_BTCUSDT_d.date, Binance_ETHUSDT_d.close as ETH\
#  FROM Binance_BTCUSDT_d, Binance_ETHUSDT_d\
#   where Binance_BTCUSDT_d.date=Binance_ETHUSDT_d.date"

# sql1="CREATE TABLE new as SELECT Binance_BTCUSDT_d.close as BTC Binance_BTCUSDT_d.date, Binance_ETHUSDT_d.close as ETH\
#  FROM Binance_BTCUSDT_d, Binance_ETHUSDT_d\
#   where Binance_BTCUSDT_d.date=Binance_ETHUSDT_d.date.format


