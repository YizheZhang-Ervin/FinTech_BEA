import base64
import datetime
import os
import sqlite3
import time
from io import BytesIO
import pandas as pd
import numpy as np
import quandl
import matplotlib.pyplot as plt
from dateutil import tz
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3
from pandas.plotting import register_matplotlib_converters
from mpl_toolkits.mplot3d import Axes3D
import GoldAnalysisSystem.database_handler as dh

BASE_DIR = os.path.dirname(os.path.abspath('manage.py'))

register_matplotlib_converters()


def time_judge(times, data, move_type, timeperiod):
    while True:
        if timeperiod == 'short':
            timeduration = data.index
        elif timeperiod == 'long':
            timeduration = data['Date']

        if times in timeduration or np.any(times == timeduration):
            return str(times)
        else:
            b = datetime.datetime.strptime(times, "%Y-%m-%d")
            if move_type == 'back':
                c = b + datetime.timedelta(days=-1)
                times = c.strftime("%Y-%m-%d")
            elif move_type == 'forward':
                c = b + datetime.timedelta(days=1)
                times = c.strftime("%Y-%m-%d")


def getorigintime():
    tz_sh = tz.gettz('Asia/Shanghai')
    now = datetime.datetime.now(tz=tz_sh)
    return now


def gettime():
    return getorigintime().strftime('%Y-%m-%d')


def getdata():
    golddata = quandl.get("SHFE/AUZ2020", authtoken="EDHKCFxMS-fA8rLYvvef", start_date="2019-11-18",
                          end_date=gettime())
    return golddata


def getdata_l():
    data = pd.read_excel(dh.BASE_DIR + '/alldata_filter.xlsx')
    return data


def getcurrentdata():
    golddata = getdata()
    currentdate = gettime()
    try:
        currentdata = golddata.loc[str(currentdate), ['Open', 'Close', 'High', 'Low', 'Settle']].values
    except Exception:
        currentdata = []
        for i in range(1, 10):
            currentdate = (getorigintime() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            try:
                currentdata = golddata.loc[str(currentdate), ['Open', 'Close', 'High', 'Low', 'Settle']].values
            except Exception:
                pass
            if len(currentdata) > 0:
                break
        return currentdate, currentdata.tolist()
    else:
        return currentdate, currentdata.tolist()


def plot_price_trend(time, name):
    golddata = getdata()
    currenttime_ymd = str(gettime())
    start = time_judge(time, golddata, 'forward', 'short')
    end = time_judge(currenttime_ymd, golddata, 'back', 'short')
    data = golddata.loc[start:end, ['Open', 'Close', 'High', 'Low', 'Settle']]
    x = data.index
    y_open = data['Open'].values
    y_close = data['Close'].values
    y_high = data['High'].values
    y_low = data['Low'].values
    y_settle = data['Settle'].values
    plt.title(name, color='Navy', fontsize='large', fontweight='bold')
    plt.figure(dpi=300)
    # border of axis x and y
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('Navy')
    ax.spines['left'].set_color('Navy')
    ax.spines['right'].set_color('none')
    plt.plot(x, y_open, label="Open Price")
    plt.plot(x, y_close, label="Close Price")
    plt.plot(x, y_high, label="High Price", ls='--')
    plt.plot(x, y_low, label="Low Price", ls='--')
    plt.plot(x, y_settle, label="Settle Price", marker='.')
    # change axis value for longer than 1 month
    if name == '2months' or name == '3months':
        x_display = []
        for index, value in enumerate(x):
            if index % 7 == 0:
                x_display.append(value.strftime('%m-%d'))
            else:
                x_display.append('')
    else:
        x_display = []
        for index, value in enumerate(x):
            x_display.append(value.strftime('%m-%d'))
    # axis x and y
    plt.xticks(x, x_display, color='Navy', rotation='45')
    plt.yticks(color='Navy')
    plt.legend()
    # pwd = os.path.dirname(os.path.dirname(__file__))
    # saveplace = pwd + '/static/pfas/img/' + name + '.png'
    # plt.savefig(saveplace, transparent=True)
    # use ascii save and load png
    # put this in html :<embed id="pic0" src="data:image/png;base64,{{pic_1}}" />
    buf = BytesIO()
    plt.savefig(buf, transparent=True, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data, name


def write_xdisplay(name, x, i):
    origin = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")

    if name:
        x_display = []
        for index, value in enumerate(x):
            x_new = (origin + datetime.timedelta(days=value)).strftime('%Y-%m')
            if index % i == 0:
                x_display.append(x_new)
            else:
                x_display.append('')
    else:
        x_display = []
        for index, value in enumerate(x):
            x_display.append(value.strftime('%m-%d'))
    return x_display


def plot_price_trend_l(time, name):
    golddata = getdata_l()
    start1 = time_judge(time, golddata, 'forward', 'long')
    # end = time_judge('2019-12-16', golddata, 'back', 'long')
    start = pd.Timestamp(start1)
    start64 = np.datetime64(start)
    end = datetime.datetime(2019, 12, 16)
    end64 = np.datetime64(end)
    df = golddata.loc[:, ['Date', 'Open', 'Close', 'High', 'Low', 'Settle']]
    data = df[(df['Date'] >= start64) & (df['Date'] <= end64)]
    x = data['Date']
    y_open = data['Open'].values
    y_close = data['Close'].values
    y_high = data['High'].values
    y_low = data['Low'].values
    y_settle = data['Settle'].values
    plt.title(name, color='Navy', fontsize='large', fontweight='bold')
    plt.figure(dpi=300)
    # plt.figure(figsize=(10,5))
    # border of axis x and y
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('Navy')
    ax.spines['left'].set_color('Navy')
    ax.spines['right'].set_color('none')
    plt.plot(x, y_open, label="Open Price")
    plt.plot(x, y_close, label="Close Price")
    plt.plot(x, y_high, label="High Price", ls='--')
    plt.plot(x, y_low, label="Low Price", ls='--')
    plt.plot(x, y_settle, label="Settle Price", marker='.')
    # change axis value for longer than 1 month
    if name == '6months':
        x_display = write_xdisplay(name, x, 15)
    elif name == '1year':
        x_display = write_xdisplay(name, x, 30)
    elif name == '2years':
        x_display = write_xdisplay(name, x, 60)
    elif name == '3years':
        x_display = write_xdisplay(name, x, 90)
    elif name == '5years':
        x_display = write_xdisplay(name, x, 180)
    elif name == '10years':
        x_display = write_xdisplay(name, x, 360)
    elif name == '12years':
        x_display = write_xdisplay(name, x, 420)

    # axis x and y
    plt.xticks(x, x_display, color='Navy', rotation='45')
    plt.yticks(color='Navy')
    plt.legend()
    # pwd = os.path.dirname(os.path.dirname(__file__))
    # saveplace = pwd + '/static/pfas/img/' + name + '.png'
    # plt.savefig(saveplace, transparent=True)
    # use ascii save and load png
    # put this in html :<embed id="pic0" src="data:image/png;base64,{{pic_1}}" />
    buf = BytesIO()
    plt.savefig(buf, transparent=True, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data, name


def connect_to_db():
    try:
        # db = psycopg2.connect(**db_postgre, sslmode='require')
        db = sqlite3.connect(database=os.path.join(BASE_DIR, 'golddata.db'))
        return db
    except Exception:
        print("connect DB failed")


def exe_sql(cursor, col, delta):
    sql0 = 'select '
    sql1 = ' from golddata where golddata.date>='
    sql2 = ' order by date asc'

    i = 1
    while True:
        cursor.execute(sql0 + col + sql1 + str(delta) + sql2)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute(sql0 + col + sql1 + str(delta - i) + sql2)
            i += 1
        else:
            break
    data = [x for r in rows for x in r]
    return data


def plot_price_trend_l_db(start_time, name):
    # connect db
    conn = connect_to_db()
    cursor = conn.cursor()
    # time handling
    st_new = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    origin = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")
    delta = (st_new-origin).days+2
    open_p = exe_sql(cursor, 'open', delta)
    close_p = exe_sql(cursor, 'close', delta)
    high_p = exe_sql(cursor, 'high', delta)
    low_p = exe_sql(cursor, 'low', delta)
    settle_p = exe_sql(cursor, 'settle', delta)
    # volume = exe_sql(cursor, 'volume', delta)
    date = exe_sql(cursor, 'date', delta)
    conn.commit()
    cursor.close()
    conn.close()

    x = date
    y_open = open_p
    y_close = close_p
    y_high = high_p
    y_low = low_p
    y_settle = settle_p
    plt.title(name, color='Navy', fontsize='large', fontweight='bold')
    plt.figure(dpi=300)
    # plt.figure(figsize=(10,5))
    # border of axis x and y
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('Navy')
    ax.spines['left'].set_color('Navy')
    ax.spines['right'].set_color('none')
    plt.plot(x, y_open, label="Open Price")
    plt.plot(x, y_close, label="Close Price")
    plt.plot(x, y_high, label="High Price", ls='--')
    plt.plot(x, y_low, label="Low Price", ls='--')
    plt.plot(x, y_settle, label="Settle Price", marker='.')
    # change axis value for longer than 1 month
    if name == '6months':
        x_display = write_xdisplay(name, x, 15)
    elif name == '1year':
        x_display = write_xdisplay(name, x, 30)
    elif name == '2years':
        x_display = write_xdisplay(name, x, 60)
    elif name == '3years':
        x_display = write_xdisplay(name, x, 90)
    elif name == '5years':
        x_display = write_xdisplay(name, x, 180)
    elif name == '10years':
        x_display = write_xdisplay(name, x, 360)
    elif name == '12years':
        x_display = write_xdisplay(name, x, 420)

    # axis x and y
    plt.xticks(x, x_display, color='Navy', rotation='45')
    plt.yticks(color='Navy')
    plt.legend()
    # pwd = os.path.dirname(os.path.dirname(__file__))
    # saveplace = pwd + '/static/pfas/img/' + name + '.png'
    # plt.savefig(saveplace, transparent=True)
    # use ascii save and load png
    # put this in html :<embed id="pic0" src="data:image/png;base64,{{pic_1}}" />
    buf = BytesIO()
    plt.savefig(buf, transparent=True, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data, name


def plot_price_table(time, name):
    golddata = getdata()
    currenttime_ymd = str(gettime())
    start = time_judge(time, golddata, 'forward', 'short')
    end = time_judge(currenttime_ymd, golddata, 'back', 'short')
    data = golddata.loc[start:end, ['Open', 'Close', 'High', 'Low', 'Settle']]
    plt.figure()
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.xticks([])
    plt.yticks([])
    col_labels = ['Open', 'Close', 'High', 'Low', 'Settle']
    row_labels = data.index.strftime('%m-%d')
    table_vals = data.values.tolist()
    cc_col = ['none' for i in range(len(col_labels))]
    cc = [cc_col for i in range(len(row_labels))]
    cc_row = ['none' for i in range(len(row_labels))]
    plt.table(cellText=table_vals, rowLabels=row_labels, colLabels=col_labels, loc='center', cellColours=cc,
              rowColours=cc_row, colColours=cc_col)
    # pwd = os.path.dirname(os.path.dirname(__file__))
    # saveplace = pwd + '/static/pfas/img/' + name + '.png'
    # plt.savefig(saveplace, transparent=True)
    buf = BytesIO()
    plt.savefig(buf, transparent=True, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data, name


def plot_3D(name):
    golddata = getdata()
    data = golddata.loc[:, ['Settle']]
    data2 = golddata.loc[:, ['Volume']]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    y = data.values.tolist()
    y_new = [float(v) for i in y for v in i]
    y = y_new
    z = data2.values.tolist()
    z_new = [float(v) for i in z for v in i]
    z = z_new
    x = [i for i in range(len(y))]
    ax.plot(x, y, zs=0, zdir='z', label='curve in (x,y)', color='Gold')
    ax.scatter(xs=x, zs=z, ys=y, zdir='z', label='points in (x,y,z)', c='Gold')
    ax.legend()
    ax.title.set_color('Navy')
    ax.w_xaxis.set_pane_color((0.2, 0.2, 0.2, 1.0))
    ax.w_yaxis.set_pane_color((0.2, 0.2, 0.2, 1.0))
    ax.w_zaxis.set_pane_color((0.25, 0.25, 0.25, 1.0))
    ax.set_xlabel('Days')
    ax.set_ylabel('Settle Price')
    ax.set_zlabel('Volume')
    ax.view_init(elev=35, azim=-45)
    plt.xticks(color='Navy')
    plt.yticks(color='Navy')
    ax.tick_params(axis='z', colors='Navy')
    ax.xaxis.label.set_color('Navy')
    ax.yaxis.label.set_color('Navy')
    ax.zaxis.label.set_color('Navy')

    # pwd = os.path.dirname(os.path.dirname(__file__))
    # saveplace = pwd + '/static/pfas/img/' + name + '.png'
    # plt.savefig(saveplace, transparent=True)
    buf = BytesIO()
    plt.savefig(buf, transparent=True, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data, name


def plot_animation(name):
    golddata = getdata()
    data = golddata.loc[:, ['Settle']]
    data2 = golddata.loc[:, ['High']]
    y = [float(v) for i in data.values.tolist() for v in i]
    x = [i for i in range(len(y))]
    # moving average for 3 days
    y_new = [(y[i] + y[i + 1] + y[i + 2]) / 3 if 0 < i < len(y) - 3 else np.NaN for i in range(len(y) - 2)]
    x_new = [i for i in range(len(y))]
    x_new.pop(0)
    x_new.pop(-1)
    # head-tail line
    # x1, y1, x2, y2 = x[0], y[0], x[-1], y[-1]
    # for i in range(len(y)):
    #     (y[i]+y[i+1]+y[i+2])/3
    # def yy(x):
    #     return (x - x1) / (x2 - x1) * (y2 - y1) + y1
    # yyy = [yy(index) for index in x]
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel('Days')
    ax.set_ylabel('Settle Price')
    ax.xaxis.label.set_color('#0028FF')
    ax.yaxis.label.set_color('#0028FF')
    line, = ax.plot(x, y, color='#0028FF', label='Settle Price')
    line2, = ax.plot(x_new, y_new, color='#9B6A12', label='Moving Average(3days)')
    ax.legend()
    text_pt = plt.text(4, 0.8, '', fontsize=10, color='#0028FF')
    point_ani, = plt.plot(x[0], y[0], "ro", color='#0028FF')

    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('#0028FF')
    ax.spines['left'].set_color('#0028FF')
    ax.spines['right'].set_color('none')
    plt.xticks(color='#0028FF')
    plt.yticks(color='#0028FF')
    ax1 = plt.gca()
    # ax1.patch.set_facecolor("black")
    xdata = []
    ydata = []

    def init():  # only required for blitting to give a clean slate.
        line.set_ydata(y[0])
        line.set_xdata(x[0])
        return line,

    def animate(i):
        xdata.append(x[i])
        ydata.append(y[i])
        line.set_data(xdata, ydata)
        text_pt.set_position((x[i], y[i]))
        text_pt.set_text("x=%.3f,\n y=%.3f" % (x[i], y[i]))
        point_ani.set_data(x[i], y[i])
        point_ani.set_marker("o")
        point_ani.set_markersize(5)
        return line, point_ani, text_pt

    ani = animation.FuncAnimation(
        fig, animate, init_func=init, interval=120, blit=True, save_count=len(y))

    # pwd = os.path.dirname(os.path.dirname(__file__))
    # saveplace = pwd + '/static/pfas/img/' + name + '.gif'
    # ani.save(saveplace, savefig_kwargs={'transparent': True}, writer='imagemagick')
    # plt.savefig(saveplace, transparent=True)
    # return ani.to_html5_video()
    return ani.to_jshtml(), name


def plot_diy(time, name, *datatype):
    columns = list(datatype)
    golddata = getdata()
    currenttime_ymd = str(gettime())
    start = time_judge(time, golddata, 'forward', 'short')
    end = time_judge(currenttime_ymd, golddata, 'back', 'short')
    data = golddata.loc[start:end, columns]
    x = data.index
    plt.title(name, color='Navy', fontsize='large', fontweight='bold')
    plt.figure(dpi=300)

    # border of axis x and y
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('Navy')
    ax.spines['left'].set_color('Navy')
    ax.spines['right'].set_color('none')

    # change axis value for longer than 1 month
    delta = datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")
    if delta.days > 30:
        x_display = []
        for index, value in enumerate(x):
            if index % 7 == 0:
                x_display.append(value.strftime('%m-%d'))
            else:
                x_display.append('')
    else:
        x_display = []
        for index, value in enumerate(x):
            x_display.append(value.strftime('%m-%d'))

    # diy plot
    for i in columns:
        if i == 'Settle':
            plt.plot(x, data[i].values, label=i + ' Price', marker='.')
        elif i == 'High' or i == 'Low':
            plt.plot(x, data[i].values, label=i + ' Price', ls='--')
        else:
            plt.plot(x, data[i].values, label=i + ' Price')
    # axis x and y
    plt.xticks(x, x_display, color='Navy', rotation='45')
    plt.yticks(color='Navy')
    plt.legend()
    # pwd = os.path.dirname(os.path.dirname(__file__))
    # saveplace = pwd + '/static/pfas/img/' + name + '.png'
    # plt.savefig(saveplace, transparent=True)
    # use ascii save and load png
    # put this in html :<embed id="pic0" src="data:image/png;base64,{{pic_1}}" />
    buf = BytesIO()
    plt.savefig(buf, transparent=True, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


if __name__ == '__main__':
    pass
    # dt = getdata_l()
    # print(dt['Date'])
    # recordtime = datetime.datetime.strptime('2019-12-16', "%Y-%m-%d")
    # sixmonths = (recordtime - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
    # plot_price_trend_l(sixmonths, '6months')
    # plot_price_trend_l_db('2020-01-03', '3m')
