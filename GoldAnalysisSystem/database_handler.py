import os

import psycopg2
from pandas.tests.io.excel.test_xlrd import xlrd
from tornado import web
import sqlite3

db_postgre = {
    'host': 'ec2-3-234-169-147.compute-1.amazonaws.com',
    'database': 'd9f3ajslqe7rqs',
    'user': 'gbamypawqyraaw',
    'port': 5432,
    'Password': 'f98054a164f90d6c3354e9e1d68a6db8868cb8f03404a830822081ab72399eba',
    'URI': 'postgres://gbamypawqyraaw:f98054a164f90d6c3354e9e1d68a6db8868cb8f03404a830822081ab72399eba@ec2-3-234-169'
           '-147.compute-1.amazonaws.com:5432/d9f3ajslqe7rqs ',
    'Heroku CLI': 'heroku pg:psql postgresql-dimensional-12453 --app bea-analysis'
}
db_sqlite3 = {'database': 'golddata.db'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def open_excel(file_name):
    try:
        data = xlrd.open_workbook(file_name)
        return data
    except Exception:
        print("open excel failed")


def connect_to_db():
    try:
        # db = psycopg2.connect(**db_postgre, sslmode='require')
        db = sqlite3.connect(**db_sqlite3)
        return db
    except Exception:
        print("connect DB failed")


def create_table():
    sql_create = '''create table golddata
                (Date date primary key not null,
                 Open real,
                 High real,
                 Low real,
                 Close real,
                 Settle real,
                 Volume real);'''
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(sql_create)
    conn.commit()
    cursor.close()
    conn.close()
    return 'success'


def store_to(file_name):
    # connect DB
    conn = connect_to_db()
    cursor = conn.cursor()
    # open excel & get sheet names
    data = open_excel(file_name)
    sheets = data.sheet_names()

    for sheet in sheets:
        sh = data.sheet_by_name(sheet)
        row_num = sh.nrows
        lis = []
        for i in range(1, row_num):
            row_data = sh.row_values(i)
            value = (
                row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6])
            lis.append(value)
        sql = "INSERT INTO golddata (Date,Open,High,Low,Close,Settle,Volume) VALUES(?,?,?,?,?,?,?)"
        cursor.executemany(sql, lis)
        conn.commit()
        lis.clear()
    cursor.close()
    conn.close()


class InsertsqlHandler(web.RequestHandler):
    def post(self):
        # table_status = create_table()
        operation = self.get_body_argument('operation', '')
        if operation:
            if operation == 'insert':
                store_to(BASE_DIR + '/alldata_filter.xlsx')
        try:
            self.write('succeed')
        except Exception:
            self.write('error')

    def get(self):
        oper = self.get_query_argument('oper', '')
        if oper == 'select':
            sql = 'select * from golddata limit 0,10;'
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            self.render('sql.html', sqltext=rows)
        else:
            self.render('sql.html', sqltext='')
