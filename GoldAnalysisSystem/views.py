import datetime
from tornado import web
from GoldAnalysisSystem.goldanalysis import plot_price_trend, gettime, plot_price_table, getorigintime, plot_animation, \
    plot_3D, plot_diy, plot_price_trend_l
from GoldAnalysisSystem import settings


class ToolsHandler(web.RequestHandler):
    def get(self):
        self.render('tools.html')


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render(settings.setting['template_path'] + '/index.html')


class DashboardHandler(web.RequestHandler):
    def get(self):
        currenttime = getorigintime()
        recordtime = datetime.datetime.strptime('2019-12-16', "%Y-%m-%d")
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
            time, name = plot_price_trend(aweek, '1week')
        elif action == '2weeks':
            # 2 weeks
            twoweeks = (currenttime - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
            time, name = plot_price_trend(twoweeks, '2weeks')
        elif action == '3weeks':
            # 3 weeks
            threeweeks = (currenttime - datetime.timedelta(days=21)).strftime('%Y-%m-%d')
            time, name = plot_price_trend(threeweeks, '3weeks')
        elif action == '1month':
            # 1 month
            onemonth = (currenttime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            time, name = plot_price_trend(onemonth, '1month')
        elif action == '2months':
            # 2 months
            twomonths = (currenttime - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
            time, name = plot_price_trend(twomonths, '2months')
        elif action == '3months':
            # 3 months
            threemonths = (currenttime - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
            time, name = plot_price_trend(threemonths, '3months')
        elif action == '6months':
            # 6 months
            sixmonths = (recordtime - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_l(sixmonths, '6months')
        elif action == '1year':
            # 1 year
            oneyear = (recordtime - datetime.timedelta(days=360)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_l(oneyear, '1year')
        elif action == '2years':
            # 2 years
            twoyears = (recordtime - datetime.timedelta(days=720)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_l(twoyears, '2years')
        elif action == '3years':
            # 3 years
            threeyears = (recordtime - datetime.timedelta(days=1080)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_l(threeyears, '3years')
        elif action == '5years':
            # 5 years
            fiveyears = (recordtime - datetime.timedelta(days=1800)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_l(fiveyears, '5years')
        elif action == '10years':
            # 10 years
            tenyears = (recordtime - datetime.timedelta(days=3600)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_l(tenyears, '10years')
        elif action == '12years':
            # 12 years
            twelveyears = (recordtime - datetime.timedelta(days=4320)).strftime('%Y-%m-%d')
            time, name = plot_price_trend_l(twelveyears, '12years')
        elif action == '':
            time = ''

        if action2 == '1line-animation':
            type, name = plot_animation('All time animation')
        elif action2 == '3d':
            time, name = plot_3D('All time 3D')
            type = ''
        elif action2 == 'diy':
            type = ''
            name = 'Please select Date/Data which you need to analyze'
        else:
            type = ''

        # Transfer parameters
        self.render('dashboard.html', time=time, type=type, name=name, diychart='')

    def post(self, **kwargs):
        date001 = self.get_body_argument('date001', '')
        name001 = self.get_body_argument('name001', '')
        data001 = self.get_body_arguments('data001', '')
        try:
            diychart = plot_diy(date001, name001, *data001)
            self.render('dashboard.html', time='', type='', name='', diychart=diychart)
        except Exception:
            self.render('dashboard.html', time='', type='', name='', diychart='')


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
