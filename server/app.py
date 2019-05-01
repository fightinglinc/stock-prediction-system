import os
from flask import Flask, render_template, request
from flask_cors import *
import mysql.connector
import json
import operations
import task

curPath = os.path.abspath(os.path.dirname(__file__))

base_dir = os.path.abspath('../public')
app = Flask(__name__, template_folder=base_dir, static_folder=base_dir, static_url_path="")
CORS(app, supports_credentials=True)
config = {
    'user': 'Arabella',
    'password': '12345678',
    'host': 'cs539-database.ciyg1obu7hnf.us-east-2.rds.amazonaws.com',
    'database': '568Project',
    'port': 3306
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/historical-stock-data/<company>', methods=['GET', 'PUT'])
def historicalData(company):
    if request.method == 'GET':
        tableName = "historical_data_" + company
        if len(request.args) == 0:
            db = mysql.connector.connect(**config)
            cursor = db.cursor()
            sql = "SELECT id, DATE_FORMAT(time, '%Y-%m-%d')  AS time, open, high, low, close,volume FROM " + tableName
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()
            db.close()
            return json.dumps(records)
        else:
            startDate = request.args.get('from')
            endDate = request.args.get('to')
            db = mysql.connector.connect(**config)
            cursor = db.cursor()
            sql = "SELECT DATE_FORMAT(time, '%Y-%m-%d')  AS time, close " + \
                  "FROM %s " % (tableName) + \
                  "WHERE DATE(time) BETWEEN DATE('%s') AND DATE('%s') order by time asc" % (startDate, endDate)
            cursor.execute(sql)
            records = cursor.fetchall()
            stockData = {"dates": [record[0] for record in records], "prices": [record[1] for record in records]}
            cursor.close()
            db.close()
            return json.dumps(stockData)

    if request.method == 'PUT':
        operations.getDataFromApiAndWriteToDisk(curPath + '/data', company)
        operations.writeToDB(curPath + '/data', company)
        return "sucess"


@app.route('/latest-price/', methods=['GET'])
def get_latest_price():
    # task.timed_task()
    if request.method == 'GET':
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT sc.cmp_name, DATE_FORMAT(lp.time, '%Y-%m-%d'), lp.price, lp.volume " \
              "FROM latest_price as lp, stock_company as sc " \
              "WHERE sc.name = lp.name"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        items = []
        for i in range(len(records)):
            items.append(dict(name=records[i][0], time=records[i][1],
                              price=records[i][2], volume=records[i][3]))
        items = dict(data=items)
        return json.dumps(items)


@app.route('/high-price/<company>', methods=['GET'])
def get_highest_price(company):
    if request.method == 'GET':
        tableName = "historical_data_" + company
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT t.name, DATE_FORMAT(t.time, '%Y-%m-%d') AS time, t.close " \
              "FROM " + tableName + " t " \
              "JOIN " \
              "(SELECT Name, MAX(close) maxVal " \
              "FROM " + tableName + \
              " WHERE DATE_SUB(CURDATE(), INTERVAL 10 DAY) < DATE(time) " \
              "GROUP BY Name)" + \
              "t2 ON t.close = t2.maxVal AND t.name = t2.name"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        items = [{'name': records[0][0], 'time': records[0][1], 'price': records[0][2]}]
        items = dict(data=items)
        return json.dumps(items)


@app.route('/avg-price/<company>', methods=['GET'])
def get_avg_price(company):
    if request.method == 'GET':
        tableName = "historical_data_" + company
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT name, avg(close) as avg_price " \
              "FROM " + tableName + " WHERE DATE_SUB(CURDATE(), INTERVAL 1 YEAR) < DATE(time)"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        items = [{'name': records[0][0], 'price': records[0][1]}]
        items = dict(data=items)
        return json.dumps(items)


@app.route('/low-price/<company>', methods=['GET'])
def get_lowest_price(company):
    if request.method == 'GET':
        tableName = "historical_data_" + company
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT t.name, DATE_FORMAT(t.time, '%Y-%m-%d') AS time, t.close " \
              "FROM " + tableName + " t " \
              "JOIN " \
              "(SELECT Name, MIN(close) minVal " \
              "FROM " + tableName + \
              " WHERE DATE_SUB(CURDATE(), INTERVAL 1 YEAR) < DATE(time) " \
              "GROUP BY Name)" + \
              "t2 ON t.close = t2.minVal AND t.name = t2.name"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        items = [{'name': records[0][0], 'time': records[0][1], 'price': records[0][2]}]
        items = dict(data=items)
        return json.dumps(items)


@app.route('/list-company/<company>', methods=['GET'])
def get_company(company):
    if request.method == 'GET':
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT sc.id, sc.cmp_name, AVG(sd.close) " \
              "FROM StockData AS sd, stock_company AS sc " \
              "WHERE sc.name = sd.name " \
              "GROUP BY sc.name " \
              "HAVING AVG(sd.close) < (select MIN(close) from StockData " \
              "WHERE name= " + repr(company) + \
              " AND DATE_SUB(CURDATE(), INTERVAL 1 YEAR) < DATE(occurred_at))"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        items = []
        for i in range(len(records)):
            items.append(dict(id=records[i][0], name=records[i][1], price=records[i][2]))
        items = dict(data=items)
        return json.dumps(items)


if __name__ == '__main__':
    app.run(debug=True)
