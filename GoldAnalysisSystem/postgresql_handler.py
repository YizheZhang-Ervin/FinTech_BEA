from urllib.request import BaseHandler

import psycopg2

from GoldAnalysisSystem.settings import db_postgre


class dataHandler(BaseHandler):

    def post(self):
        try:
            xx = self.get_argument('xx', None)
            if not xx:
                self.write({"error": "none input"})
                return
            sql = "insert into xx_table(col1,col2) values('{0}','{1}')".format(xx,xx)
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