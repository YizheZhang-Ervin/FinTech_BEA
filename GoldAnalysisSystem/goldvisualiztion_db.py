import datetime
import os
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64
BASE_DIR = os.path.dirname(os.path.abspath('manage.py'))


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


def write_xdisplay_db(name, x, i):
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


def plot_price_trend_l_db(start_time, name):
    # connect db
    conn = connect_to_db()
    cursor = conn.cursor()
    # time handling
    st_new = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    origin = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")
    delta = (st_new - origin).days + 2
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
        x_display = write_xdisplay_db(name, x, 15)
    elif name == '1year':
        x_display = write_xdisplay_db(name, x, 30)
    elif name == '2years':
        x_display = write_xdisplay_db(name, x, 60)
    elif name == '3years':
        x_display = write_xdisplay_db(name, x, 90)
    elif name == '5years':
        x_display = write_xdisplay_db(name, x, 180)
    elif name == '10years':
        x_display = write_xdisplay_db(name, x, 360)
    elif name == '12years':
        x_display = write_xdisplay_db(name, x, 420)

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


def plot_diy_db(start_time, name, *datatype):
    # connect db
    conn = connect_to_db()
    cursor = conn.cursor()
    # cols
    columns = list(datatype)
    # time handling
    st_new = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    origin = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")
    delta = (st_new - origin).days + 2
    # get data
    cols = {}
    for i in columns:
        cols[i] = exe_sql(cursor, str(i), delta)
    date = exe_sql(cursor, 'date', delta)
    conn.commit()
    cursor.close()
    conn.close()

    # set x
    x = date
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
        x_display = write_xdisplay_db(name, x, 1)
    elif 30 <= len(date) <= 89:
        x_display = write_xdisplay_db(name, x, 7)
    elif 90 <= len(date) <= 179:
        x_display = write_xdisplay_db(name, x, 15)
    elif 180 <= len(date) <= 359:
        x_display = write_xdisplay_db(name, x, 30)
    elif 360 <= len(date) <= 719:
        x_display = write_xdisplay_db(name, x, 60)
    elif 720 <= len(date) <= 1079:
        x_display = write_xdisplay_db(name, x, 90)
    elif 1080 <= len(date) <= 1799:
        x_display = write_xdisplay_db(name, x, 180)
    elif 1800 <= len(date) <= 3599:
        x_display = write_xdisplay_db(name, x, 360)
    elif len(date) >= 3599:
        x_display = write_xdisplay_db(name, x, 420)

    # diy plot
    for i in columns:
        if i == 'settle':
            plt.plot(x, cols[i], label=i + ' Price', marker='.')
        elif i == 'high' or i == 'low':
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








