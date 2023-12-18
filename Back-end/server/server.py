# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_cors import CORS
import sql
import NDVI
import PixelCalc

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

"""
加载影像数据
"""
@app.route('/api/data/modelImg', methods=["GET"])
def modelImg():
    return sql.imgLoading()


"""
加载统计数据
"""
@app.route('/api/data/statistical', methods=["GET"])
def statistics():
    return sql.statisticalLoading()

"""
查找任务列表
"""
@app.route('/api/data/taskList', methods=["GET"])
def taskList():
    return sql.taskSelect()


"""
插入任务
"""
@app.route('/api/model/taskInsert', methods=["POST"])
def saveModelTask():
    name = request.json["name"]
    # 返回插入任务的ID
    lastId = sql.taskIdSql(name)
    # 查询列表
    data = taskList()
    return [lastId, data]


"""
计算NDVI
"""
@app.route('/api/model/NDVI', methods=["POST"])
def calcNDVI():
    id = request.json["id"]
    name = request.json["name"]
    # 执行计算
    NDVI.startNDVI(id, name)
    # 返回查询结果
    data = taskList()
    return data

"""
计算像素数量
"""
@app.route('/api/model/calcPixel', methods=["POST"])
def calcPixel():
    name = request.json["name"]
    return PixelCalc.pixelCount(name)

if __name__ == '__main__':
    app.run()

