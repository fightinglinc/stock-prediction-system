import requests
import mysql.connector
import os.path
import requests
import csv
import time
import mysql.connector

API_KEY = '8ATXKFFXNC10W9J8'
curPath = os.path.abspath(os.path.dirname(__file__))

config = {
    'user': 'Arabella',
    'password': '12345678',
    'host': 'cs539-database.ciyg1obu7hnf.us-east-2.rds.amazonaws.com',
    'database': '568Project',
    'port': 3306
}

def getDataFromApiAndWriteToDisk(path, company):
    apiName = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + \
          company + '&interval=1min&outputsize=full&apikey=' + API_KEY + '&datatype=csv'
    r = requests.get(apiName)
    fileName = path + "/" + company + "_realtime.csv"
    with open(fileName, "w") as f:
        f.write(r.text)

def createTable(tableName):
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    drop_sql = "DROP TABLE IF EXISTS " + "`" + tableName + "`"
    cursor.execute(drop_sql)
    sql = """
         CREATE TABLE %s (
         id int(11) AUTO_INCREMENT NOT NULL,
         name VARCHAR(30) NOT NULL,
         time DATETIME NOT NULL,
         open FLOAT NOT NULL,
         high FLOAT NOT NULL,
         low FLOAT NOT NULL,
         close FLOAT NOT NULL,
         volume FLOAT NOT NULL,
         PRIMARY KEY (`id`))
      """%(tableName)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

def writeToDB(path, company):
    fileName = path + "/" + company + "_realtime.csv"
    tableName = "realtime_data_" + company
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    createTable(tableName)
    with open(fileName, "r") as f:
        next(f)
        i = 1
        for line in f:
            if i > 390:
                break
            data = line.split(",")
            name, time, op, high, low, close, vol = company, data[0], data[1], data[2], data[3], data[4], data[5]
            sql = "INSERT INTO " + tableName + " (name, time, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (name, time, op, high, low, close, vol)
            cursor.execute(sql, val)
            db.commit()
            i += 1

    cursor.close()
    db.close()


def readFromDB(company):
    tableName = "realtime_data_" + company
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    sql = "SELECT * FROM " + tableName
    cursor.execute(sql)
    records = cursor.fetchall()
    print(records[0])

    cursor.close()
    db.close()



# if __name__ == "__main__":
    # companyList = ["GOOG", "WMT", "MSFT", "IBM", "AMZN", "CSCO", "ORCL", "EBAY", "JPM", "FB"]
    # for company in companyList:
    #     getData(API_PREFIX, company)
    #     writeToDB("", company)

    # test_company = "FB"
    #getDataFromApi(API_PREFIX, curPath + '/data', test_company)
    #writeToDB(curPath + '/data', test_company)
    # readFromDB("FB")
