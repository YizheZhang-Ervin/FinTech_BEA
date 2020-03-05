import os
from tornado import ioloop, web
from tornado.options import define, options, parse_command_line
from GoldAnalysisSystem.views import IndexHandler, DashboardHandler, EntryHandler, ToolsHandler

define('port', default='8000', type=int)
define('env', default='develop', type=str)


def make_app():
    # URL
    return web.Application(handlers=[
        (r'/', IndexHandler),
        (r'/dashboard/', DashboardHandler),
        (r'/entry_point/', EntryHandler),
        (r'/tools/', ToolsHandler),

    ],
        template_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
        static_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
    )


def make_app_deploy():
    app = make_app()
    app.add_handlers(r'^(www\.)?black8\.top$', [(r'/', IndexHandler), ])
    return app


if __name__ == '__main__':
    # decode start command, use python xx.py --port=xxxx
    parse_command_line()

    # judge environment of running
    if options.env == 'develop':
        # start tornado / application object
        app = make_app()
    elif options.env == 'deploy':
        # start tornado
        app = make_app_deploy()

    # listen on port
    app.listen(options.port)

    # listen to IO instance
    ioloop.IOLoop.current().start()
