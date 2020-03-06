import timeit
import pandas as pd
import quandl


def test(function, times):
    result1 = timeit.timeit(function, number=times)
    print(result1)


def getdataname():
    namelist = []
    wordlist = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
    for i in range(2008, 2020):
        for j in wordlist:
            namelist.append('SHFE/AU' + j + str(i))
    return namelist[5:]


def getdata(timeperiod):
    golddata = quandl.get(timeperiod, authtoken="EDHKCFxMS-fA8rLYvvef")
    return golddata


def get12yearsdata():
    datalist = []
    for tp in getdataname():
        datalist.append(getdata(tp))
    return pd.concat(datalist)


def data_to_file():
    alldata = get12yearsdata()
    alldata.to_excel('../alldata.xlsx')
    return 'success'


if __name__ == '__main__':
    # test(getdata('SHFE/AUZ2020'), 1)
    # print(getdataname())
    # print(getdata())
    # print(get12yearsdata())
    # print(data_to_file())
    pass
