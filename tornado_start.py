import os

import pymysql
from tornado import ioloop, web
from tornado.options import define, options, parse_command_line

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
    def get(self):
        # Transfer parameters
        items = ['a', 'b', 'c']
        self.render('dashboard.html', items=items)


def make_app():
    # URL
    return web.Application(handlers=[
        (r'/', IndexHandler),
        (r'/entry_point/', EntryHandler),
        (r'/dashboard/', DashboardHandler)
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