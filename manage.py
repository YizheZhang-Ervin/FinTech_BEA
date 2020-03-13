import os
from tornado import ioloop, web, httpserver
from tornado.options import options, parse_command_line
from GoldAnalysisSystem import settings
from GoldAnalysisSystem.daemon import daemon
from GoldAnalysisSystem.urls import urlpatterns
from GoldAnalysisSystem.wsgi import start_by_wsgi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def make_app():
    # URL
    return web.Application(handlers=urlpatterns,
                           template_path=settings.setting['template_path'],
                           static_path=settings.setting['static_path'],
                           )


def make_app_deploy():
    app = make_app()
    app.add_handlers(r'^(www\.)?black8\.top$', urlpatterns)
    return app


def main():
    # decode start command, use python xx.py --port=xxxx
    parse_command_line()

    # judge environment of running
    if options.env == 'produce':
        # start tornado
        app = make_app_deploy()
    else:
        # start tornado / application object
        app = make_app()

    # judge multi-process or not
    if options.processtype == 'multiple':
        server = httpserver.HTTPServer(app)
        server.bind(options.port)
        server.start(0)
    else:
        # listen on port
        app.listen(options.port)

    # listen to IO instance
    ioloop.IOLoop.current().start()

    # judge whether fork backend
    if options.daemon == 'on':
        pid = daemon()
        if pid:
            return pid


if __name__ == '__main__':
    # judge whether start by wsgi
    if options.wsgi == 'on':
        app = make_app()
        start_by_wsgi(app)
    else:
        main()