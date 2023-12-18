# -*- coding: utf-8 -*-
import pymysql, json
from datetime import datetime


# 重新构造类解决无法json.dumps() datetime的问题
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

host = "localhost"
user = "root"
password = "root"
db_name = "Ningbo_Project"

# 连接数据库
db = pymysql.connect(host = host, user = user, password = password, database = db_name, autocommit=True)

# 请求影像数据
def imgLoading():
    # 创建游标对象
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 创建 sql 语句
    sql = "SELECT * FROM carbon_img"
    # 执行sql语句
    cursor.execute(sql)

    data = cursor.fetchall()
    cursor.close()

    return json.dumps(data)

# 请求统计数据
def statisticalLoading():
    # 创建游标对象
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 创建 sql 语句
    sql = "SELECT * FROM carbon"
    # 执行sql语句
    cursor.execute(sql)

    data = cursor.fetchall()
    cursor.close()

    return json.dumps(data)

# 查询模型任务列表
def taskSelect():
    # 创建游标对象
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 查询表
    sql = "SELECT * FROM carbon_task ORDER BY `id` DESC"
    # 执行sql语句
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    cursor.close()
    return json.dumps(data, cls=ComplexEncoder)

# 将任务插入数据库，并返回任务ID
def taskIdSql(name):
    # 插入时间
    timer = datetime.now()
    # 插入任务
    # 创建游标对象
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 创建 sql 语句
    sql = "INSERT INTO `carbon_task`(name, status, timer) VALUES(%s, %s, %s)"
    # 执行sql语句
    cursor.execute(sql, (name, 0, timer))
    # 获取ID
    last_insert_id = cursor.lastrowid
    db.commit()
    cursor.close()

    return last_insert_id

# 将 url 存入数据库
def resSaveSql(url, id, type):
    # 创建游标对象
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 创建sql语句
    if type == 'res':
        sql = "UPDATE `carbon_task` SET `res_url` = %s WHERE `id` = %s"
    elif type == 'tile':
        sql = "UPDATE `carbon_task` SET `tiles_url` = %s, `status` = 1 WHERE `id` = %s"

    # 执行sql语句
    cursor.execute(sql, (url, id))

    # 提交更改
    db.commit()

    # 关闭游标
    cursor.close()


