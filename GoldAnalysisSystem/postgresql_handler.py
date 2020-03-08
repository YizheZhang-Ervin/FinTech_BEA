import psycopg2
from pandas.tests.io.excel.test_xlrd import xlrd
from tornado import web

db_postgre = {
    'host': 'ec2-3-234-169-147.compute-1.amazonaws.com',
    'database': 'd9f3ajslqe7rqs',
    'user': 'gbamypawqyraaw',
    'port': 5432,
    'Password': 'f98054a164f90d6c3354e9e1d68a6db8868cb8f03404a830822081ab72399eba',
}


def open_excel(file_name):
    try:
        data = xlrd.open_workbook(file_name)
        return data
    except Exception:
        print("open excel failed")


def connect_to_db():
    try:
        db = psycopg2.connect(**db_postgre)
        return db
    except Exception:
        print("connect DB failed")


def create_table():
    sql_create = '''create table golddata
                (Date date primary key not null,
                 Pre_Settle real,
                 Open real,
                 High real,
                 Low real,
                 Close real,
                 Settle real,
                 CH1 real,
                 CH2 real,
                 Volume real,
                 Prev_Day_Open_Interest real,
                 Change real,
                 OI real);'''
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(sql_create)
    effect_row = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if effect_row > 0:
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
            value = (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], \
                     row_data[6], row_data[7], row_data[8], row_data[9], row_data[10], row_data[11], row_data[12])
            lis.append(value)
        sql = "INSERT INTO golddata (Date,Pre_Settle,Open,High,Low,Close,Settle,CH1,CH2,Volume,Prev_Day_Open_Interest," \
              "Change,OI) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.executemany(sql, lis)
        conn.commit()
        lis.clear()
    cursor.close()
    conn.close()


class dataHandler(web.RequestHandler):
    def post(self):
        try:
            xx = self.get_argument('xx', None)
            if not xx:
                self.write({"error": "none input"})
                return
            sql = "insert into xx_table(col1,col2) values('{0}','{1}')".format(xx, xx)
            conn = psycopg2.connect(**db_postgre)
            # cursor
            cursor = conn.cursor()
            # execute sql
            cursor.execute(sql)
            # the rows affected
            effect_row = cursor.rowcount
            # submit data
            conn.commit()
            # close cursor and connection
            cursor.close()
            conn.close()
            # judge success or not
            if effect_row > 0:
                self.write('success')
            else:
                self.write('error')
        except Exception as e:
            print(e)
            self.write('connection error')


class InsertsqlHandler(web.RequestHandler):
    def post(self):
        table_status = create_table()
        operation = self.get_body_argument('operation', '')
        if table_status and operation:
            if operation == 'insert':
                store_to('alldata.xlsx')
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
            self.render('sql.html')
