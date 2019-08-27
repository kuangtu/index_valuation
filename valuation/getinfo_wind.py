# -*- coding: UTF-8 -*-
from WindPy import *
import pandas as pd


def get_tradeDaysStr(tradeDate):
    '''
    根据当前日期，得到交易日范围
    1、如果是T年的5月1日之前，采用T-1年的前三季度报告，以及T-2年的第4季度报告
    （1）日期从T-2年的7月1日开始，至T-1年的09月30日
    （2）此时得到了5个财务报告期，序号为T-2-Q3、T-2-Q4，T-1-Q1、T-1-Q2、T-1-Q3
    （3）净利润r1 = T-2-Q4 - T-2-Q3、
        r2=T-1-Q3
    （4）然后结合当期的股本计算A股净利润
    （5）wind中日期范围是“YYYYMDD(T-2)-07-01”至“YYYYMMD（T-1）-09-30”
    2、如果是5月1日至9月1日之前，采用T年的一季度报告，以及T-1年第2、3、4季度财报
    （1）日期从T-1年的1月1日开始，至T年的3月31日
    （2）此时得到的5个财务报告期，序号为T-1-Q1、T-1-Q2、T-1-Q3、T-1-Q4、T-Q1
    （3）净利润r1 = T-1-Q1 - T-1-Q2、
        r2 = T-1-Q3 - T-1-Q2、
        r3 = T-1-Q4 - T-1-Q3
        r4 = T-Q1
    （4）然后结合当期的股本计算A股净利润
    （5）wind中日期范围是“YYYYMMDD(-1)-01-01”至“YYYYMMDD-03-31”
    3、如果是9月1日至11月1日，采用T年第1、2季度财报，以及T-1年第3、4季度财报
    （1）日期从T-1年的4月1日，至T年的6月30日
    （2）此时得到5个财务报告期，序号为T-1-Q2、T-1-Q3、T-1-Q4、T-Q1、T-Q2
    （3）净利润r1 = T-1-Q3 - T-1-Q2
        r2=  T-1-Q4 - T-1-Q3
        r3 + r4 = T-Q2
    （4）然后结合当期的股本计算A股净利润
    （5）wind中日期范围是“YYYYMMDD(-1)-04-01”至“YYYYMMDD-06-30”
    4、11月1日至次年5月1日，T年前三个季度财报、上年度第4季度财报
    （1）日期从T-1年7月1日，至T年的9月30日
    （2）此时得到5个财务报告期，序号为T-1-Q3、T-1-Q4、T-Q1、T-Q2、T-Q3
    （3）净利润：
    （4）然后结合当期的股本计算A股净利润
    （5）wind中日期范围是“YYYYMMDD(-1)-07-01”至“YYYYMMDD-09-30”
    :param tradeDate:
    :return: tradeDayStr，wind
    '''

    # 得到交易月和日
    startDate = ""
    endDate = ""
    datetype = -1
    year = int(tradeDate[:4])
    month_and_days = tradeDate[5:10]
    print(month_and_days)
    tradeDayStr = ""
    if month_and_days < "05-01":
        startDate = str(year - 2) + "-07-01"
        endDate = str(year - 1) + "-09-30"
        datetype = 1
    elif month_and_days >= '05-01' and month_and_days < '09-01':
        startDate = str(year - 1) + "-01-01"
        endDate = str(year) + "-03-31"
        datetype = 2
    elif month_and_days >= '09-01' and month_and_days < '11-01':
        startDate = str(year - 1) + '-04-01'
        endDate = str(year - 1) + '-06-30'
        datetype = 3
    elif month_and_days >= '11-01':
        startDate = str(year - 1) + '-07-01'
        endDate = str(year) + '-09-30'
        datetype = 4
    return startDate, endDate, datetype


def get_stk_report(tradeDate, conslit):
    '''
    得到最近四个季度的报告，需要根据当前的日期，得到交易日范围
    :param tradeDate:
    :return:
    '''

    startDate, endDate, datetype = get_tradeDaysStr(tradeDate)
    print(startDate, endDate)
    for cons in conslist:
        wsd_res = w.wsd(cons, "total_shares,share_totala,np_belongto_parcomsh", startDate, endDate,
              "unit=1;rptType=1;Period=Q;Days=Alldays")
        print (wsd_res)
        df = pd.DataFrame(wsd_res.Data, index=wsd_res.Fields, columns=wsd_res.Times)
        report = df.T
        # 将数据整合，得到当天需要计算的净利润、股本
        print(report)

        wss_res = w.wss(cons, "close", "tradeDate=" + tradeDate + ";priceAdj=U;cycle=D")
        print(wss_res)
        break


def getIdxCons(indexcode, tradeDate):
    '''
    得到指数成分券
    :param indexcode:
    :return: list
    '''
    queryStr = "date=" + tradeDate + ";windcode=" + indexcode
    wind_res = w.wset("sectorconstituent", queryStr)
    # print(wind_res)
    # print(wind_res.Codes)
    # print(wind_res.Fields)
    df = pd.DataFrame(
        wind_res.Data,
        index=wind_res.Fields,
        columns=wind_res.Codes)
    cons = df.T

    return cons['windcode'].tolist()


if __name__ == '__main__':
    w.start()
    tradeDate = "2019-08-26"
    conslist=['600000.SH']
    # cons = getIdxCons("000016.SH", tradeDate)
    get_stk_report(tradeDate, conslist)
