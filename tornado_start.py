import datetime
import os

import pymysql
from tornado import ioloop, web
from tornado.options import define, options, parse_command_line

from goldanalysis import getorigintime, plot_price_trend, plot_price_table, gettime, plot_animation, plot_3D

define('port', default='8000', type=int)


class MainHandler(web.RequestHandler):
    def get(self):
        self.write('hello get')
        # receive values
        # GET/POST: self.get_argument()/ self.get_arguments()
        # GET: self.get_query_argument()/ self.get_query_arguments()
        # POST: self.get_body_argument()/ self.get_body_arguments()
        # status code
        # self.set_status(200)
        # set/clear cookie
        # self.set_cookie('abc', '123', expires_days=1)
        # self.clear_cookie('abc')/ self.clear_all_cookies()
        # redirect
        # self.redirect('/res/')

    def post(self):
        # add content
        self.write('hello post')


class EntryHandler(web.RequestHandler):
    def initialize(self):
        # visit DB
        self.conn = pymysql.Connection(host='', password='', database='', user='', port='')
        self.cursor = self.conn.cursor()

    def prepare(self):
        pass

    def get(self):
        sql = 'select * from xx;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.write('query here')

    def post(self):
        pass

    def on_finish(self):
        # execute at last
        self.conn.close()


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')


class DashboardHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        currenttime = getorigintime()
        try:
            action = self.get_query_argument('time', '')
            action2 = self.get_query_argument('type', '')
        except Exception:
            action, action2 = '', ''

        if action == 'days' or action == 'tables':
            # 1 week table
            aweek_table = (currenttime - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
            time = plot_price_table(aweek_table, gettime())
        elif action == '1week':
            # 1 week
            aweek = (currenttime - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            time = plot_price_trend(aweek, '1week')
        elif action == '2weeks':
            # 2 weeks
            twoweeks = (currenttime - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
            time = plot_price_trend(twoweeks, '2weeks')
        elif action == '3weeks':
            # 3 weeks
            threeweeks = (currenttime - datetime.timedelta(days=21)).strftime('%Y-%m-%d')
            time = plot_price_trend(threeweeks, '3weeks')
        elif action == '1month':
            # 1 month
            onemonth = (currenttime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            time = plot_price_trend(onemonth, '1month')
        elif action == '2months':
            # 2 months
            twomonths = (currenttime - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
            time = plot_price_trend(twomonths, '2months')
        elif action == '3months':
            # 3 months
            threemonths = (currenttime - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
            time = plot_price_trend(threemonths, '3months')
        elif action == '':
            time = ''

        if action2 == '1line-animation':
            type = plot_animation('allin_animation')
        elif action2 == '3d':
            time = plot_3D('allin_3D')
            type = ''
        else:
            type = ''

        # Transfer parameters
        self.render('dashboard.html', time=time, type=type)


def make_app():
    # URL
    return web.Application(handlers=[
        (r'/', IndexHandler),
        (r'/dashboard/', DashboardHandler),
        (r'/entry_point/', EntryHandler),

    ],
        template_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
        static_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
    )


if __name__ == '__main__':
    # decode start command, use python xx.py --port=xxxx
    parse_command_line()
    # start tornado / application object
    app = make_app()
    # listen port
    app.listen(options.port)
    # listen to IO instance
    ioloop.IOLoop.current().start()
