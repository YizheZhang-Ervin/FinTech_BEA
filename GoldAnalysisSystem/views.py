import datetime
import os
import traceback

import quandl
from numpy.core.defchararray import isalpha, isalnum
from tornado import web

from GoldAnalysisSystem.database_handler import store_to_db
from GoldAnalysisSystem.goldanalysis_xlsx_api import gettime, getorigintime, plot_price_table
from GoldAnalysisSystem import settings
from GoldAnalysisSystem.goldvisualization_db import plot_price_trend_db, plot_diy_db, plot_3D_db, plot_animation_db, \
    connect_to_db
from GoldAnalysisSystem.goldvisualization_xau_db import plot_price_trend_db_xau, plot_animation_db_xau, plot_3D_db_xau, \
    plot_diy_db_xau, plot_price_table_xau, connect_to_db_xau

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ToolsHandler(web.RequestHandler):
    def get(self):
        self.render('tools.html')


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render(settings.setting['template_path'] + '/index.html')

    def post(self):
        name = self.get_body_argument('Name', '')
        email = self.get_body_argument('Email', '')
        self.write('succeed!' + name + email)


class DashboardHandler(web.RequestHandler):
    def get(self):
        currenttime = getorigintime()
        # recordtime = datetime.datetime.strptime('2019-12-16', "%Y-%m-%d")
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
            sixmonths = (currenttime - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(sixmonths, '6months')
        elif action == '1year':
            # 1 year
            oneyear = (currenttime - datetime.timedelta(days=360)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(oneyear, '1year')
        elif action == '2years':
            # 2 years
            twoyears = (currenttime - datetime.timedelta(days=720)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(twoyears, '2years')
        elif action == '3years':
            # 3 years
            threeyears = (currenttime - datetime.timedelta(days=1080)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(threeyears, '3years')
        elif action == '5years':
            # 5 years
            fiveyears = (currenttime - datetime.timedelta(days=1800)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(fiveyears, '5years')
        elif action == '10years':
            # 10 years
            tenyears = (currenttime - datetime.timedelta(days=3600)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db(tenyears, '10years')
        elif action == '12years':
            # 12 years
            twelveyears = (currenttime - datetime.timedelta(days=4320)).strftime('%Y-%m-%d')
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
        self.render('dashboard_SHFE.html', time=time, type=type, name=name, diychart='')

    def post(self, **kwargs):
        date001 = self.get_body_argument('date001', '')
        name001 = self.get_body_argument('name001', '')
        data001 = self.get_body_arguments('data001', '')
        try:
            diychart = plot_diy_db(date001, name001, *data001)
            self.render('dashboard_SHFE.html', time='', type='', name='', diychart=diychart)
        except Exception:
            self.render('dashboard_SHFE.html', time='', type='', name='', diychart='')


class XAUDashboardHandler(web.RequestHandler):
    def get(self):
        currenttime = getorigintime()
        name = ''
        try:
            action = self.get_query_argument('time', '')
            action2 = self.get_query_argument('type', '')
        except Exception:
            action, action2 = '', ''

        if action == 'days' or action == 'tables':
            # 1 week table
            aweek_table = (currenttime - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
            time, name = plot_price_table_xau(aweek_table, gettime())
        elif action == '1week':
            # 1 week
            aweek = (currenttime - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(aweek, '1week')
        elif action == '2weeks':
            # 2 weeks
            twoweeks = (currenttime - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(twoweeks, '2weeks')
        elif action == '3weeks':
            # 3 weeks
            threeweeks = (currenttime - datetime.timedelta(days=21)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(threeweeks, '3weeks')
        elif action == '1month':
            # 1 month
            onemonth = (currenttime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(onemonth, '1month')
        elif action == '2months':
            # 2 months
            twomonths = (currenttime - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(twomonths, '2months')
        elif action == '3months':
            # 3 months
            threemonths = (currenttime - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(threemonths, '3months')
        elif action == '6months':
            # 6 months
            sixmonths = (currenttime - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(sixmonths, '6months')
        elif action == '1year':
            # 1 year
            oneyear = (currenttime - datetime.timedelta(days=360)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(oneyear, '1year')
        elif action == '2years':
            # 2 years
            twoyears = (currenttime - datetime.timedelta(days=720)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(twoyears, '2years')
        elif action == '3years':
            # 3 years
            threeyears = (currenttime - datetime.timedelta(days=1080)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(threeyears, '3years')
        elif action == '5years':
            # 5 years
            fiveyears = (currenttime - datetime.timedelta(days=1800)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(fiveyears, '5years')
        elif action == '10years':
            # 10 years
            tenyears = (currenttime - datetime.timedelta(days=3600)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(tenyears, '10years')
        elif action == '12years':
            # 12 years
            twelveyears = (currenttime - datetime.timedelta(days=4320)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_db_xau(twelveyears, '12years')
        elif action == '':
            time = ''

        if action2 == '1line-animation':
            type, name = plot_animation_db_xau('All time animation')
        elif action2 == '3d':
            time, name = plot_3D_db_xau('All time 3D')
            type = ''
        elif action2 == 'diy':
            type = ''
            name = 'Please select Date/Data which you need to analyze'
        else:
            type = ''

        # Transfer parameters
        self.render('dashboard_LBMA.html', time=time, type=type, name=name, diychart='')

    def post(self, **kwargs):
        date001 = self.get_body_argument('date001', '')
        name001 = self.get_body_argument('name001', '')
        data001 = self.get_body_arguments('data001', '')
        try:
            diychart = plot_diy_db_xau(date001, name001, *data001)
            self.render('dashboard_LBMA.html', time='', type='', name='', diychart=diychart)
        except Exception:
            print(Exception.with_traceback())
            self.render('dashboard_LBMA.html', time='', type='', name='', diychart='')


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
                # golddata (SHFE) insert
                sql = 'select date from golddata order by date desc'
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                # current date
                newest_date = rows[0][0]
                origin = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")
                db_newest_date_ymd = (origin + datetime.timedelta(days=newest_date - 2 + 1)).strftime('%Y-%m-%d')
                # retrieve data
                golddata = quandl.get("SHFE/AUZ2020", authtoken="EDHKCFxMS-fA8rLYvvef")
                now = gettime()
                data = golddata.loc[db_newest_date_ymd:now, ['Open', 'High', 'Low', 'Close', 'Settle', 'Volume']]
                # insert data
                # data.to_sql(name='golddata', con=conn, if_exists='append', index=True, index_label='date')
                data.to_excel(BASE_DIR + '/new.xlsx')
                store_to_db(BASE_DIR + '/new.xlsx')
                conn.commit()
                cursor.close()
                conn.close()

                # golddata (LBMA) insert
                sql2 = 'select date from golddata_xau order by date desc'
                conn2 = connect_to_db_xau()
                cursor2 = conn2.cursor()
                cursor2.execute(sql2)
                rows_xau = cursor2.fetchall()
                # current date
                newest_date = rows_xau[0][0]
                newest_date_ymd = datetime.datetime.strptime(newest_date, '%Y-%m-%d %H:%M:%S').date()
                newest_date_ymd_plus = (newest_date_ymd + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                # retrieve data
                xau_gold_data = quandl.get("LBMA/GOLD", authtoken="EDHKCFxMS-fA8rLYvvef")
                data_xau = xau_gold_data.loc[newest_date_ymd_plus:,
                           ['USD (AM)', 'USD (PM)', 'GBP (AM)', 'GBP (PM)', 'EURO (AM)', 'EURO (PM)']]
                # insert data
                data_xau.to_sql(name='golddata_xau', con=conn2, if_exists='append', index=True, index_label='date')
                conn2.commit()
                cursor2.close()
                conn2.close()
                self.render('sql_backend.html', result='success', history='insert', lastsql='')
            except Exception:
                traceback.print_exc()
                self.render('sql_backend.html', result='Something wrong with DB, please try again', history='',
                            lastsql='')
        elif operate == 'select' or operate == 'update' or operate == 'delete':
            self.render('sql_backend.html', result="BEA Warning: Can't access without Permission", history='',
                        lastsql='')
        else:
            self.render('sql_backend.html', result="", history='', lastsql='')

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
                # column name of table
                titles = cursor.description
                if titles:
                    titles_new = [t[0] for t in titles]
                else:
                    titles_new = ''
                conn.commit()
                cursor.close()
                conn.close()
                rows_new = str(titles_new) + '\n'
                for r in rows:
                    rows_new += str(r) + '\n'

                times = datetime.datetime.now()
                if history != '':
                    self.render('sql_backend.html', result=rows_new,
                                history=str(times) + ':\n' + sql + '\n\n' + history, lastsql=sql)
                else:
                    self.render('sql_backend.html', result=rows_new, history=str(times) + ':\n' + sql, lastsql=sql)
            except Exception:
                traceback.print_exc()
                self.render('sql_backend.html', result='Something wrong with DB, please try again', history=history,
                            lastsql='')
        else:
            self.render('sql_backend.html', result="BEA Warning: Can't access without Permission", history=history,
                        lastsql='')


class pyjscmdHandler(web.RequestHandler):
    def get(self):
        self.render('cmd.html', input='', output='')

    def post(self):
        inputs = self.get_body_argument('input', '')
        result_eval = lambda x: eval(x)
        try:
            result_output = result_eval(inputs)
        except Exception:
            result_output = "please enter correct Python instruction"
        self.render('cmd.html', input=inputs, output=result_output)


class webHandler(web.RequestHandler):
    def get(self):
        self.render('quickatt.html')


class TranslatorHandler(web.RequestHandler):
    def get(self):
        self.render('translator.html', origin='', translate='', pos='', position='', keywords='')

    def post(self):
        ta_origin = self.get_body_argument('ta_origin', '')
        import jieba
        import pinyin.cedict
        from jieba import posseg as pseg
        from jieba import analyse

        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass

            try:
                import unicodedata
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass

            return False

        def callg(word):
            from googletrans import Translator
            translator_g = Translator()
            return translator_g.translate(word, src='zh-cn', dest='en').text.lower()

        def translator(sentence):
            if is_number(sentence) or isalpha(sentence) or isalnum(sentence):
                return sentence
            else:
                modal = ['吧', '罢', '呗,''啵', '的', '家', '啦,''来', '了', '嘞', '哩', '咧', '咯', '啰', '喽,''吗', '嘛', '么', '哪',
                         '呢', '呐', '呵', '哈', '则', '哉', '呸', '罢了', '啊', '呃', '欸', '哇', '呀', '耶', '哟', '呕', '噢', '呦']
                # divide sentence
                words = jieba.cut(sentence, cut_all=False)
                words_list = [x if x not in modal else '' for x in words]
                # translation
                translate_list = [pinyin.cedict.translate_word(s)[0] + ' '
                                  if pinyin.cedict.translate_word(s)
                                     and '[' not in pinyin.cedict.translate_word(s)[0] else callg(s)
                                  for s in words_list]
                translate_list2 = []
                for k in translate_list:
                    ix = k.find('(')
                    if ix != -1:
                        translate_list2.append(k[:ix])
                    else:
                        translate_list2.append(k[:])
                return ''.join(translate_list2).replace(' to ', ' ')

        def pos_position_kw(sentence):
            words_pseg = pseg.cut(sentence)
            word_token = jieba.tokenize(sentence)
            keywords = analyse.textrank(sentence, withWeight=True)

            word_tag_l = [i + ' ' + j if i != "\u3000" or i != "\n" else '' for i, j in words_pseg]
            word_token_l = [str(a) + ' ' + str(b) + ' ' + str(c) for a, b, c in word_token]
            if len(keywords) != 0:
                keywords_l = [i for i in keywords]
            else:
                keywords_l = 'Short Sentence, No Keywords Here'
            # print(len(keywords_l))
            return word_tag_l, word_token_l, keywords_l

        ta_translate = translator(ta_origin)
        ta_other = pos_position_kw(ta_origin)

        self.render('translator.html', origin=ta_origin, translate=ta_translate, pos=ta_other[0], position=ta_other[1],
                    keywords=ta_other[2])
