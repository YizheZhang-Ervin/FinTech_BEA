import datetime
import os
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import quandl
from matplotlib import animation
from GoldAnalysisSystem.goldanalysis_xlsx_api import getorigintime, time_judge

BASE_DIR = os.path.dirname(os.path.abspath('manage.py'))


def get_xau_data_tosql():
    conn = connect_to_db_xau()
    xau_data = quandl.get("LBMA/GOLD", authtoken="EDHKCFxMS-fA8rLYvvef")
    xau_data.to_sql(name='golddata_xau', con=conn, if_exists='append', index=True, index_label='date')


def connect_to_db_xau():
    try:
        # db = psycopg2.connect(**db_postgre, sslmode='require')
        db = sqlite3.connect(database=os.path.join(BASE_DIR, 'golddata.db'))
        return db
    except Exception:
        print("connect DB failed")


def exe_sql_xau(cursor, col, ymdhms):
    sql0 = 'select "'
    sql1 = '" from golddata_xau where golddata_xau.date>="'
    sql2 = '" order by date asc'

    cursor.execute(sql0 + col + sql1 + str(ymdhms) + sql2)
    rows = cursor.fetchall()
    data = [x for r in rows for x in r]
    return data


def write_xdisplay_db_xau(name, x, i):
    if name:
        x_display = []
        for index, value in enumerate(x):
            if name == '1week' or name == '2weeks' or name == '3weeks' or name == '1month' or name == '2months' or name == '3 month':
                x_new = value.strftime('%m-%d')
                if index % i == 0:
                    x_display.append(x_new)
                else:
                    x_display.append('')
            else:
                x_new = value.strftime('%Y-%m')
                if index % i == 0:
                    x_display.append(x_new)
                else:
                    x_display.append('')
    else:
        x_display = []
        for index, value in enumerate(x):
            x_display.append(value.strftime('%m-%d'))
    return x_display


def plot_price_trend_db_xau(start_time, name):
    # connect db
    conn = connect_to_db_xau()
    cursor = conn.cursor()
    # time handling
    ymdhms = start_time + ' 00:00:00'
    usd_am = exe_sql_xau(cursor, 'USD (AM)', ymdhms)
    usd_pm = exe_sql_xau(cursor, 'USD (PM)', ymdhms)
    gbp_am = exe_sql_xau(cursor, 'GBP (AM)', ymdhms)
    gbp_pm = exe_sql_xau(cursor, 'GBP (PM)', ymdhms)
    euro_am = exe_sql_xau(cursor, 'EURO (AM)', ymdhms)
    euro_pm = exe_sql_xau(cursor, 'EURO (PM)', ymdhms)
    date = exe_sql_xau(cursor, 'date', ymdhms)
    conn.commit()
    cursor.close()
    conn.close()

    x = [datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date() for d in date]
    y_usdam = usd_am
    y_usdpm = usd_pm
    y_gbpam = gbp_am
    y_gbppm = gbp_pm
    plt.title(name, color='Navy', fontsize='large', fontweight='bold')
    plt.figure(dpi=300)
    # plt.figure(figsize=(10,5))
    # border of axis x and y
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('Navy')
    ax.spines['left'].set_color('Navy')
    ax.spines['right'].set_color('none')
    plt.plot(x, y_usdam, label="USD(AM)")
    plt.plot(x, y_usdpm, label="USD(PM)")
    plt.plot(x, y_gbpam, label="GBP(AM)", ls='--')
    plt.plot(x, y_gbppm, label="GBP(PM)", ls='--')

    # change axis value for longer than 1 month
    if name == '2months':
        x_display = write_xdisplay_db_xau(name, x, 3)
    elif name == '3months':
        x_display = write_xdisplay_db_xau(name, x, 7)
    elif name == '6months':
        x_display = write_xdisplay_db_xau(name, x, 15)
    elif name == '1year':
        x_display = write_xdisplay_db_xau(name, x, 30)
    elif name == '2years':
        x_display = write_xdisplay_db_xau(name, x, 60)
    elif name == '3years':
        x_display = write_xdisplay_db_xau(name, x, 90)
    elif name == '5years':
        x_display = write_xdisplay_db_xau(name, x, 180)
    elif name == '10years':
        x_display = write_xdisplay_db_xau(name, x, 360)
    elif name == '12years':
        x_display = write_xdisplay_db_xau(name, x, 420)
    else:
        x_display = write_xdisplay_db_xau(name, x, 1)
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


def plot_diy_db_xau(start_time, name, *datatype):
    # connect db
    conn = connect_to_db_xau()
    cursor = conn.cursor()
    # cols
    columns = list(datatype)
    # time handling
    ymdhms = start_time + ' 00:00:00'
    # get data
    cols = {}
    for i in columns:
        cols[i] = exe_sql_xau(cursor, str(i), ymdhms)
    date = exe_sql_xau(cursor, 'date', ymdhms)
    conn.commit()
    cursor.close()
    conn.close()

    # set x
    x = [datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S').date() for d in date]
    plt.title(name, color='Navy', fontsize='large', fontweight='bold')
    plt.figure(dpi=300)

    # border of axis x and y
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('Navy')
    ax.spines['left'].set_color('Navy')
    ax.spines['right'].set_color('none')

    # change axis value for longer than 1 month
    if 0 <= len(date) <= 29:
        x_display = write_xdisplay_db_xau(name, x, 1)
    elif 30 <= len(date) <= 89:
        x_display = write_xdisplay_db_xau(name, x, 7)
    elif 90 <= len(date) <= 179:
        x_display = write_xdisplay_db_xau(name, x, 15)
    elif 180 <= len(date) <= 359:
        x_display = write_xdisplay_db_xau(name, x, 30)
    elif 360 <= len(date) <= 719:
        x_display = write_xdisplay_db_xau(name, x, 60)
    elif 720 <= len(date) <= 1079:
        x_display = write_xdisplay_db_xau(name, x, 90)
    elif 1080 <= len(date) <= 1799:
        x_display = write_xdisplay_db_xau(name, x, 180)
    elif 1800 <= len(date) <= 3599:
        x_display = write_xdisplay_db_xau(name, x, 360)
    elif len(date) >= 3599:
        x_display = write_xdisplay_db_xau(name, x, 420)

    # diy plot
    for i in columns:
        if i == 'USD (AM)':
            plt.plot(x, cols[i], label=i + ' Price', marker='.')
        elif i == 'GBP (AM)' or i == 'GBP (PM)':
            plt.plot(x, cols[i], label=i + ' Price', ls='--')
        else:
            plt.plot(x, cols[i], label=i + ' Price')
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


def plot_3D_db_xau(name):
    # connect db
    conn = connect_to_db_xau()
    cursor = conn.cursor()
    # time handling
    currenttime = getorigintime()
    threemonths = (currenttime - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    ymdhms = threemonths + ' 00:00:00'

    usd_am = exe_sql_xau(cursor, 'USD (AM)', ymdhms)
    usd_pm = exe_sql_xau(cursor, 'USD (PM)', ymdhms)

    date = exe_sql_xau(cursor, 'date', ymdhms)
    conn.commit()
    cursor.close()
    conn.close()

    # data
    x = [i for i in range(1, len(date) + 1)]
    y = [i if i else 0 for i in usd_am]
    z = [i if i else 0 for i in usd_pm]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot(x, y, zs=0, zdir='z', label='curve in (x,y)', color='Gold')
    ax.scatter(xs=x, zs=z, ys=y, zdir='z', label='points in (x,y,z)', c='Gold')
    ax.legend()
    ax.title.set_color('Navy')
    ax.w_xaxis.set_pane_color((0.2, 0.2, 0.2, 1.0))
    ax.w_yaxis.set_pane_color((0.2, 0.2, 0.2, 1.0))
    ax.w_zaxis.set_pane_color((0.25, 0.25, 0.25, 1.0))
    ax.set_xlabel('Days')
    ax.set_ylabel('USD (AM)')
    ax.set_zlabel('USD (PM)')
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


def plot_animation_db_xau(name):
    # connect db
    conn = connect_to_db_xau()
    cursor = conn.cursor()
    # time handling
    currenttime = getorigintime()
    threemonths = (currenttime - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    ymdhms = threemonths + ' 00:00:00'

    usd_am = exe_sql_xau(cursor, 'USD (AM)', ymdhms)
    date = exe_sql_xau(cursor, 'date', ymdhms)

    conn.commit()
    cursor.close()
    conn.close()

    # data
    y = [i if i else 0 for i in usd_am]
    x = [i for i in range(1, len(date) + 1)]
    # moving average for 3 days
    y_new = [(y[i] + y[i + 1] + y[i + 2]) / 3 if 0 < i < len(y) - 3 else np.NaN for i in range(len(y) - 2)]
    x_new = [i for i in range(1, len(y) + 1)]
    x_new.pop(0)
    x_new.pop(-1)

    # plot
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel('Days')
    ax.set_ylabel('USD (AM) Price')
    ax.xaxis.label.set_color('#0028FF')
    ax.yaxis.label.set_color('#0028FF')
    line, = ax.plot(x, y, color='#0028FF', label='USD (AM) Price')
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


def plot_price_table_xau(time, name):
    golddata = quandl.get("LBMA/GOLD", authtoken="EDHKCFxMS-fA8rLYvvef")
    timenow = datetime.datetime.now().strftime('%Y-%m-%d')
    currenttime_ymd = str(timenow)
    start = time_judge(time, golddata, 'forward', 'short')
    end = time_judge(currenttime_ymd, golddata, 'back', 'short')
    data = golddata.loc[start:end, ['USD (AM)', 'USD (PM)', 'GBP (AM)', 'GBP (PM)']]
    plt.figure()
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.xticks([])
    plt.yticks([])
    col_labels = ['USD (AM)', 'USD (PM)', 'GBP (AM)', 'GBP (PM)']
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