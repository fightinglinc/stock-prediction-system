import os, sys
from flask import Flask, render_template, jsonify, send_from_directory, request
import time
import json
from datetime import *
import mysql.connector
import json
import operations
curPath = os.path.abspath(os.path.dirname(__file__))

base_dir = os.path.abspath('../public')
app = Flask(__name__, template_folder=base_dir, static_folder=base_dir, static_url_path="")
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
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT id, DATE_FORMAT(time, '%Y-%m-%d')  AS time, open, high, low, close,volume FROM " + tableName
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return json.dumps(records)

    if request.method == 'PUT':
        operations.getDataFromApiAndWriteToDisk(curPath + '/data', company)
        operations.writeToDB(curPath + '/data', company)
        return "sucess"

@app.route('/historical-stock-data/<company>/query', methods=['POST'])
def getStockByTimeFrame(company):
    fromDate = "2018-12-01"
    toDate = "2019-04-24"
    tableName = "historical_data_" + company
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    sql = "SELECT DATE_FORMAT(time, '%Y-%m-%d')  AS time, close " + \
          "FROM %s " %(tableName) + \
          "WHERE DATE(time) BETWEEN DATE('%s') AND DATE('%s') order by time asc" %(fromDate, toDate)

    print(sql)
    cursor.execute(sql)
    records = cursor.fetchall()
    print(records)
    stockData = {"dates": [record[0] for record in records], "prices": [record[1] for record in records]}
    cursor.close()
    db.close()
    print(stockData)
    return json.dumps(stockData)


@app.route('/latest-price/', methods=['GET'])
def get_latest_price():
    if request.method == 'GET':
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT sc.cmp_name, DATE_FORMAT(lp.time, '%Y-%m-%d'), lp.price " \
              "FROM latest_price as lp, stock_company as sc " \
              "WHERE sc.name = lp.name"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return json.dumps(records)


@app.route('/high-price/<company>', methods=['GET'])
def get_highest_price(company):
    if request.method == 'GET':
        tableName = "historical_data_" + company
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT name, DATE_FORMAT(NOW(), '%Y-%m-%d') AS time, MAX(close) AS highest_price " \
              "FROM " + tableName + " WHERE DATE_SUB(CURDATE(), INTERVAL 10 DAY) <= DATE(time)"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return json.dumps(records)


@app.route('/avg-price/<company>', methods=['GET'])
def get_avg_price(company):
    if request.method == 'GET':
        tableName = "historical_data_" + company
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT name,  avg(close) as avg_price " \
              "FROM " + tableName + " WHERE DATE_SUB(CURDATE(), INTERVAL 1 YEAR) < DATE(time)"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return json.dumps(records)


@app.route('/low-price/<company>', methods=['GET'])
def get_lowest_price(company):
    if request.method == 'GET':
        tableName = "historical_data_" + company
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        sql = "SELECT name, MIN(close) AS lowest_price " \
              "FROM " + tableName + " WHERE DATE_SUB(CURDATE(), INTERVAL 1 YEAR) < DATE(time)"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return json.dumps(records)


# @app.route('/list-company/<company>', methods=['GET'])
# def get__price(company):
#     if request.method == 'GET':
#         tableName = "historical_data_" + company
#         db = mysql.connector.connect(**config)
#         cursor = db.cursor()
#         sql = "SELECT name, MIN(close) AS lowest_price " \
#               "FROM " + tableName + " WHERE DATE_SUB(CURDATE(), INTERVAL 1 YEAR) < DATE(time)"
#         cursor.execute(sql)
#         records = cursor.fetchall()
#         cursor.close()
#         db.close()
#         return json.dumps(records)


if __name__ == '__main__':
    app.run(debug=True)
