import os
from tornado.options import define
from manage import BASE_DIR

define('port', default='8000', type=int)
define('env', default='develop', type=str)
define('processtype', default='single', type=str)
define('daemon', default='off', type=str)
define('wsgi', default='off', type=str)

setting = {
    'template_path': os.path.join(BASE_DIR, 'templates'),
    'static_path': os.path.join(BASE_DIR, 'static'),
    'debug': False,
    'xsrf_cookies': True,
}
