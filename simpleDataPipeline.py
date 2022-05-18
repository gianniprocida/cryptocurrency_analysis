import sqlite3
import pandas as pd
import os

def clean_data(filename):
    dataset = pd.read_csv(filename, sep = ',', decimal=',',skiprows=1)
    dataset.dropna(inplace=True)
    # Expand = True , It will expand out into separate columns
    dataset[['date', 'time']] = dataset['date'].str.split(' ', 1, expand=True)
    # Convert dataset["date"] to datetime
    dataset["date"] = pd.to_datetime(dataset["date"], infer_datetime_format=True)
    cleansed = dataset.drop(columns=['time', 'tradecount'])
    # Rename column with spaces
    cleansed.rename(columns={cleansed.columns[7]:"Volume_crypto"},inplace=True)
    cleansed.rename(columns={cleansed.columns[8]: "Volume_USDT"},inplace=True)
    tablename = filename.split('.')[0]
    columnname=  filename.split('_')[1].replace("USDT","")
    return cleansed, tablename,columnname

def create_table(dataframe, tablename):

    try:
        db = sqlite3.connect('crypto.db')
        c = db.cursor()
        createTable = "CREATE TABLE IF NOT EXISTS {0} (unix float, date text, symbol text, \
    open float, high float,low float, close float, Volume_crypto float, Volume_USDT float)".format(tablename)
   
        c.execute(createTable)

        dataframe.to_sql(tablename,db,if_exists="replace",index=False) 
       
        db.commit()
        db.close()
    except sqlite3.Error as e:
        print(e)
    return db


def join_tables(tableName1, columnName1, tableName2, columnName2):
    try:
        db = sqlite3.connect('crypto.db')
        c = db.cursor()
        joinedTablename = "price"
        sql_join = "CREATE TABLE {0} as SELECT {1}.date as Date, {1}.close as {2}, {3}.close as {4} \
        FROM {1}, {3}\
         WHERE {1}.date={3}.date".format(joinedTablename, tableName1, columnName1, tableName2,columnName2)


        c.execute(sql_join)

        # Datatype of the two columns is lost when sql_join statement is executed.
        #
        # SQLite does not fully support ALTER TABLE statements.
        # Workaround: 1) rename the table to tmp, 2) create a new table with the new columns datatype/names,
        # 3) copy the content from the tmp table, 4) drop the old table

        sql_alter = "ALTER TABLE {0} RENAME TO tmp".format(joinedTablename)

        c.execute(sql_alter)

        sql_create = "CREATE TABLE {0} (Date TEXT, {1} FLOAT, {2} FLOAT)".format(
            joinedTablename, columnName1, columnName2)

        c.execute(sql_create)

        sql_insert = "INSERT INTO {0} (Date, {1}, {2})\
         SELECT Date, {1}, {2} FROM tmp".format(
            joinedTablename, columnName1, columnName2)

        c.execute(sql_insert)

        sql_drop = "DROP TABLE tmp"

        c.execute(sql_drop)
        print(
            "Price table with {0} and {1} successfully created ..".format(
                columnName1, columnName2))

        db.commit()
        db.close()
    except sqlite3.Error as e:
        print(e)
    return db


def add_table(filename):
    (cleansed3, tableName3, columnName3) = clean_data(filename)
    try:
        db = sqlite3.connect('crypto.db')
        c = db.cursor()
        joinedTablename = "price"
        sql_addcolumn = "ALTER TABLE {0} ADD COLUMN {1} FLOAT".format(joinedTablename,
            columnName3)

        c.execute(sql_addcolumn)

        createTable = "CREATE TABLE IF NOT EXISTS {0} (unix FLOAT, date TEXT, symbol TEXT, \
    open FLOAT, high FLOAT,low FLOAT, close FLOAT, Volume_crypto FLOAT, Volume_USDT FLOAT)".format(
        tableName3)

        c.execute(createTable)

        cleansed3.to_sql(tableName3, db, if_exists="replace",
                     index=False)

        # Update price table

        sql_updatetable = "UPDATE {0} SET {1}=(SELECT close FROM {2} WHERE {2}.date={0}.Date)".format(
            joinedTablename, columnName3, tableName3)
        print("Updating table with {0}".format(columnName3))
        c.execute(sql_updatetable)

        db.commit()
    except sqlite3.Error as e:
       print(e)
    return db

if __name__=='__main__':
    csv_files = [file for file in os.listdir(os.getcwd()) if
                 file.endswith('.csv')]
    (cleansed1, tableName1,columnName1) = clean_data(csv_files.pop())

    (cleansed2, tableName2, columnName2) = clean_data(csv_files.pop())

    create_table(cleansed1,tableName1)

    create_table(cleansed2,tableName2)

    # Base with two tables joined

    join_tables(tableName1,columnName1,tableName2,columnName2)

    # Let's add other tables

    (cleansed3,tableName3, columnName3) = clean_data(csv_files.pop())

    while len(csv_files) > 0:
        add_table(csv_files.pop())







    
    
