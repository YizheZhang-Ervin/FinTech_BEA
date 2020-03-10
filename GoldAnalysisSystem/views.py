import datetime
import os

import quandl
from tornado import web

from GoldAnalysisSystem.database_handler import store_to_db
from GoldAnalysisSystem.goldanalysis_xlsx_api import gettime, getorigintime, plot_price_table
from GoldAnalysisSystem import settings
from GoldAnalysisSystem.goldvisualiztion_db import plot_price_trend_db, plot_diy_db, plot_3D_db, plot_animation_db, \
    connect_to_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ToolsHandler(web.RequestHandler):
    def get(self):
        self.render('tools.html')


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render(settings.setting['template_path'] + '/index.html')


class DashboardHandler(web.RequestHandler):
    def get(self):
        currenttime = getorigintime()
        recordtime = datetime.datetime.strptime('2019-12-16', "%Y-%m-%d")
        name = ''
        try:
            action = self.get_query_argument('time', '')
            action2 = self.get_query_argument('type', '')
        except Exception:
            action, action2 = '', ''

        if action == 'days' or action == 'tables':
            # 1 week table
            aweek_table = (currenttime - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
            time, name = plot_price_table(aweek_table, gettime())
        elif action == '1week':
            # 1 week
            aweek = (currenttime - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(aweek, '1week')
        elif action == '2weeks':
            # 2 weeks
            twoweeks = (currenttime - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(twoweeks, '2weeks')
        elif action == '3weeks':
            # 3 weeks
            threeweeks = (currenttime - datetime.timedelta(days=21)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(threeweeks, '3weeks')
        elif action == '1month':
            # 1 month
            onemonth = (currenttime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(onemonth, '1month')
        elif action == '2months':
            # 2 months
            twomonths = (currenttime - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(twomonths, '2months')
        elif action == '3months':
            # 3 months
            threemonths = (currenttime - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(threemonths, '3months')
        elif action == '6months':
            # 6 months
            sixmonths = (recordtime - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(sixmonths, '6months')
        elif action == '1year':
            # 1 year
            oneyear = (recordtime - datetime.timedelta(days=360)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(oneyear, '1year')
        elif action == '2years':
            # 2 years
            twoyears = (recordtime - datetime.timedelta(days=720)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(twoyears, '2years')
        elif action == '3years':
            # 3 years
            threeyears = (recordtime - datetime.timedelta(days=1080)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(threeyears, '3years')
        elif action == '5years':
            # 5 years
            fiveyears = (recordtime - datetime.timedelta(days=1800)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(fiveyears, '5years')
        elif action == '10years':
            # 10 years
            tenyears = (recordtime - datetime.timedelta(days=3600)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(tenyears, '10years')
        elif action == '12years':
            # 12 years
            twelveyears = (recordtime - datetime.timedelta(days=4320)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(twelveyears, '12years')
        elif action == '':
            time = ''

        if action2 == '1line-animation':
            type, name = plot_animation_db('All time animation')
        elif action2 == '3d':
            time, name = plot_3D_db('All time 3D')
            type = ''
        elif action2 == 'diy':
            type = ''
            name = 'Please select Date/Data which you need to analyze'
        else:
            type = ''

        # Transfer parameters
        self.render('dashboard.html', time=time, type=type, name=name, diychart='')

    def post(self, **kwargs):
        date001 = self.get_body_argument('date001', '')
        name001 = self.get_body_argument('name001', '')
        data001 = self.get_body_arguments('data001', '')
        try:
            diychart = plot_diy_db(date001, name001, *data001)
            self.render('dashboard.html', time='', type='', name='', diychart=diychart)
        except Exception:
            self.render('dashboard.html', time='', type='', name='', diychart='')


class ErrorHandler(web.RequestHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.write('Something goes wrong>>> <br>The error code is: '
                       + str(status_code) + '>>> <br>Thank you for watching>>>')
        elif status_code == 500:
            self.write('Something goes wrong>>> <br>The error code is: '
                       + str(status_code) + '>>> <br>Thank you for watching>>>')
        else:
            self.write('Something goes wrong>>> <br>The error code is: '
                       + str(status_code) + '>>> <br>Thank you for watching>>>')


class sqlcmdHandler(web.RequestHandler):
    def get(self):
        operate = self.get_query_argument('operate', '')
        if operate == 'insert':
            try:
                sql = 'select date from golddata order by date desc'
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                # current date
                newest_date = rows[0][0]
                origin = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")
                db_newest_date_ymd = (origin + datetime.timedelta(days=newest_date - 2+1)).strftime('%Y-%m-%d')
                # retrieve data
                golddata = quandl.get("SHFE/AUZ2020", authtoken="EDHKCFxMS-fA8rLYvvef")
                now = gettime()
                data = golddata.loc[db_newest_date_ymd:now, ['Open', 'High', 'Low', 'Close', 'Settle', 'Volume']]
                # insert data
                # data.to_sql(name='golddata', con=conn, if_exists='append', index=True, index_label='date')
                data.to_excel(BASE_DIR +'/new.xlsx')
                store_to_db(BASE_DIR + '/new.xlsx')
                conn.commit()
                cursor.close()
                conn.close()
                self.render('sql_backend.html', result='success', history='insert')
            except Exception:
                print(Exception.with_traceback())
                self.render('sql_backend.html', result='Something wrong with DB, please try again', history='')
        elif operate == 'select' or operate == 'update' or operate == 'delete':
            self.render('sql_backend.html', result="BEA Warning: Can't access without Permission", history='')
        else:
            self.render('sql_backend.html', result="", history='')

    def post(self):
        sql = self.get_body_argument('input', '')
        history = self.get_body_argument('history', '')
        # see tables: select name from sqlite_master where type='table' order by name
        # see columns: PRAGMA table_info(golddata)
        if sql.startswith('select') or sql.startswith('SELECT') or sql.startswith('PRAGMA'):
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                conn.commit()
                cursor.close()
                conn.close()
                rows_new = ''
                for r in rows:
                    rows_new += str(r) + '\n'
                if history != '':
                    self.render('sql_backend.html', result=rows_new, history='now:' + sql + '\n\nlast:' + history)
                else:
                    self.render('sql_backend.html', result=rows_new, history='now:' + sql)
            except Exception:
                self.render('sql_backend.html', result='Something wrong with DB, please try again', history=history)
        else:
            self.render('sql_backend.html', result="BEA Warning: Can't access without Permission", history=history)
