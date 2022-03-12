import sqlite3
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd
import os


def set_base(filename1,filename2):
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


    table_1 = filename1.split('.')[0]
    table_2 = filename2.split('.')[0]
    column1=filename1.split('_')[1].replace("USDT","")
    column2=filename2.split('_')[1].replace("USDT","")



    conn = sqlite3.connect('database.db')

    c = conn.cursor()


    createTable1 = "create table if not exists {0} (unix float, date text, symbol text, \
    open float, high float,low float, close float, Volume_crypto float, Volume_USDT float)".format(table_1)
    c.execute(createTable1)

    createTable2 = "create table if not exists {0} (unix float, date text, symbol text, \
    open float, high float,low float, close float, Volume_crypto float, Volume_USDT float)".format(table_2)

    c.execute(createTable1)

    c.execute(createTable2)

    cleansed1.to_sql(table_1,conn,if_exists='replace',index=False)
    cleansed2.to_sql(table_2, conn, if_exists='replace',index=False)
    conn.commit()
    try:
       table_joined='price'

       sql_join = "CREATE TABLE {0} as SELECT {1}.date as Date, {1}.close as {2}, {3}.close as {4} \
FROM {1}, {3} where {1}.date={3}.date".format(table_joined,table_1,column1,table_2,column2)

       c.execute(sql_join)


    # Datatype of the two column is lost when sql_join statement is executed.
    #
    # SQLite does not fully support ALTER TABLE statements.
    # Workaround: 1) rename the table to tmp, 2) create a new table with the new columns datatype/names, 3) copy the content from the tmp table, 4) drop the old table

       sql_alter="alter table {0} rename to tmp".format(table_joined)

       c.execute(sql_alter)


       sql_create="create table {0} (Date text, {1} float, {2} float)".format(table_joined,column1,column2)

       c.execute(sql_create)

       sql_insert="insert into {0} (Date, {1}, {2}) SELECT Date, {1}, {2} from tmp".format(table_joined,column1,column2)

       c.execute(sql_insert)

       sql_drop="drop table tmp"

       c.execute(sql_drop)
       print("Price table with {0} and {1} successfully created ..".format(column1,column2))

       conn.commit()
    except sqlite3.Error as e:
       print(e)
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
    print("Updating table with {0}".format(column))
    c.execute(sql_updatetable)

    conn.commit()

    return conn



if __name__=='__main__':
    csv_files = [file for file in os.listdir(os.getcwd()) if file.endswith('.csv')]
    c_1=set_base(csv_files[0],csv_files[1])
    c_2=add(csv_files[2],c_1)
    c_3=add(csv_files[3],c_2)
    c_4=add(csv_files[4],c_3)
