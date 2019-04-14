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
        sql = "SELECT id, DATE_FORMAT(NOW(), '%Y-%m-%d')  AS time, open, high, low, close,volume FROM " + tableName
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        db.close()
        return json.dumps(records)

    if request.method == 'PUT':
        operations.getDataFromApiAndWriteToDisk(curPath + '/data', company)
        operations.writeToDB(curPath + '/data', company)
        return "sucess"
if __name__ == '__main__':
    app.run(debug=True)
