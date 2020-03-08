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
}

db_postgre = {
    'host': 'ec2-3-234-169-147.compute-1.amazonaws.com',
    'database': 'd9f3ajslqe7rqs',
    'user': 'gbamypawqyraaw',
    'port': 5432,
    'Password': 'f98054a164f90d6c3354e9e1d68a6db8868cb8f03404a830822081ab72399eba',
}
