# written by: Linchen Xie
# assisted by: Linchen Xie
# debugged by: Linchen Xie
import csv
import time

import mysql.connector
import requests

API_KEY = 'demo'
config = {
    'user': 'test',
    'password': 'test',
    'host': 'localhost',
    'database': '568Project',
    'port': 3306
}


def get_text(name):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + \
          name + '&apikey=' + API_KEY + '&datatype=csv'
    r = requests.get(url)
    return r.text


def write_csv(name, data):
    file_name = 'latest_price.csv'
    with open(file_name, 'w') as f:
        f.writelines(data)


def create_table():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    drop_sql = "DROP TABLE IF EXISTS `latest_price`"
    cursor.execute(drop_sql)
    sql = """
         CREATE TABLE latest_price (
         id int(11) AUTO_INCREMENT NOT NULL,
         name VARCHAR(30) NOT NULL,
         open FLOAT NOT NULL,
         high FLOAT NOT NULL,
         low FLOAT NOT NULL,
         price FLOAT NOT NULL,
         volume FLOAT NOT NULL,
         time DATETIME NOT NULL,
         previous_close FLOAT NOT NULL,
         change_price FLOAT NOT NULL,
         change_percent VARCHAR(15) NOT NULL,
         PRIMARY KEY (`id`))
      """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def write_name(name):
    data = []
    with open('latest_price.csv', 'r') as f:
        next(f)
        reader = csv.reader(f)
        for index, row in enumerate(reader, 1):
            # row.insert(0, name)
            data.append(row)
    return data


def insert_db(data):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    insert_sql = """
                    INSERT INTO latest_price
                    (name, open, high, low, price, volume, time, previous_close, change_price, change_percent)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 """
    cursor.executemany(insert_sql, data)
    conn.commit()
    cursor.close()
    conn.close()


def get_latest_price():
    count = 0
    company_list = ["GOOG", "WMT", "MSFT", "IBM", "AMZN", "CSCO", "ORCL", "EBAY", "JPM", "FB"]
    create_table()
    for company in company_list:
        if count == 5:
            time.sleep(60)
        content = get_text(company)
        write_csv(company, content)
        lines = write_name(company)
        insert_db(lines)
        count += 1


if __name__ == '__main__':
    get_latest_price()
