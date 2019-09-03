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
        endDate = str(year) + '-06-30'
        datetype = 3
    elif month_and_days >= '11-01':
        startDate = str(year - 1) + '-07-01'
        endDate = str(year) + '-09-30'
        datetype = 4
    return startDate, endDate, datetype

def cal_stk_mkt_np(report_df, cls_df, datetype):
    '''
    计算股票最近四个计算的净利润，以及当日的A股总市值
    :param report_df:
    :param cls_df:
    :param datetype:
    :return:
    '''

    #1类型，计算的时间在小于T年的5月1日
    #计算方式T-1年的1、2、3季报，T-2年的四季报
    #此时得到的df索引顺序为T-2年3季报、4季报，T-1年1季报、2季报、3季报
    if datetype == 1:
        t_1_q1_q3 = report_df.iloc[4, 4]
        t_2_q4 = report_df.iloc[1,4] - report_df.iloc[0,4]
        ashare_np_sum = t_1_q1_q3 + t_2_q4
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print (syl)

    # 2类型，计算的时间在T年5月1日到9月1日之间
    # 计算方法是T年的1季报，T-1年的2、3、4季报，由T年的年报减去一季度
    # 需要注意计算净利润的时候，需要使用A股数量计算
    # 此时得到df索引顺序为T-1年1季报，2季报，3季报、4季报，T年的1季报
    if datetype == 2:
        t_1_q2_q4 = report_df.iloc[3, 4] - report_df.iloc[0, 4]
        t_q1 = report_df.iloc[4, 4]
        ashare_np_sum = t_1_q2_q4 + t_q1
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print(syl)

    # 3类型，计算的时间在T年9月1日到11月1日之间
    #计算方法是T年的1、2季报，T-1年的3、4季报
    #此时得到df索引顺序为T-1年2季报、3季报、4季报、T年1季报、2季报
    if datetype == 3:
        t_1_q3_q4 = report_df.iloc[2, 4] - report_df.iloc[0, 4]
        t_q1_q2 = report_df.iloc[4,4]
        ashare_np_sum = t_1_q3_q4 + t_q1_q2
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print (syl)

    # 4类型，计算的时间在T年的11月1日之后
    # 计算方法是T年的1、2、3季报，T-1年的4季报
    # 此时得到的df索引顺序为T-1年的3、4季报，T年的1季报、2季报、3季报
    if datetype == 4:
        t_1_q4 = report_df.iloc[1, 4] - report_df.iloc[0, 4]
        t_2_q1_q2_q3 = report_df.iloc[4, 4]
        ashare_np_sum = t_1_q4 + t_2_q1_q2_q3
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print(syl)



def get_stk_report(tradeDate, conslit):
    '''
    得到最近四个季度的报告，需要根据当前的日期，得到交易日范围
    :param tradeDate:
    :return:
    '''

    startDate, endDate, datetype = get_tradeDaysStr(tradeDate)
    print(datetype)
    print(startDate, endDate)
    for cons in conslist:
        wsd_res = w.wsd(cons, "total_shares,share_totala,np_belongto_parcomsh", startDate, endDate,
              "unit=1;rptType=1;Period=Q;Days=Alldays")
        print(wsd_res)
        np_df = pd.DataFrame(wsd_res.Data, index=wsd_res.Fields, columns=wsd_res.Times)
        report_df = np_df.T
        print(report_df)
        report_df.to_csv("../data/" + tradeDate + "/" + cons + "report.csv")
        # 计算A股占比，计算出A股市值占比
        report_df['ASHARE_PCT'] = report_df['SHARE_TOTALA'] / report_df['TOTAL_SHARES']
        report_df['ASHARE_NP'] = report_df['NP_BELONGTO_PARCOMSH'] * report_df['ASHARE_PCT']
        # 将数据整合，得到当天需要计算的净利润、股本
        print(report_df)
        wss_res = w.wss(cons, "close,share_totala", "tradeDate=" + tradeDate + ";priceAdj=U;cycle=D")
        perf_df = pd.DataFrame(wss_res.Data, index=wss_res.Fields, columns=wss_res.Times)
        cls_df = perf_df.T
        print(cls_df)
        cls_df.to_csv("../data/" + tradeDate + "/" + cons + "cls.csv")
        cls_df['ASHARE_MKT'] = cls_df['CLOSE'] * cls_df['SHARE_TOTALA']
        cal_stk_mkt_np(report_df, cls_df, datetype)


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

    cons.to_csv("../data/" + tradeDate + "/" + indexcode + "cons.csv")

    return cons['wind_code'].tolist()


if __name__ == '__main__':
    w.start()
    pd.set_option('display.max_columns', 999)
    tradeDate = "2019-09-02"
    conslist=['600000.SH']
    conslist = getIdxCons("000016.SH", tradeDate)
    get_stk_report(tradeDate, conslist)
