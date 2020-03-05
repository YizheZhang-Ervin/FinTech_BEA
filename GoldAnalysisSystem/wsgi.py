import wsgiref

import tornado
from tornado.options import options


def start_by_wsgi(app):
    wsgi_app = tornado.wsgi.WSGIAdapter(app)
    server = wsgiref.simple_server.make_server('', options.port, wsgi_app)
    server.serve_forever()


def start_for_other_framework(app):
    # tornado can be used for running Django/Flask/Bottle
    container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()