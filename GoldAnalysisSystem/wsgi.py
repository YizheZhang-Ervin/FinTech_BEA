import tornado
from tornado.options import options

from manage import make_app

container = tornado.wsgi.WSGIContainer(make_app())
http_server = tornado.httpserver.HTTPServer(container)
http_server.listen(options.port)
tornado.ioloop.IOLoop.current().start()
