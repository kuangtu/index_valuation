# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np

def get_dataType(tradeDate):
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
    datetype = -1
    month_and_days = tradeDate[5:10]
    print(month_and_days)
    if month_and_days < "05-01":
        datetype = 1
    elif month_and_days >= '05-01' and month_and_days < '09-01':
        datetype = 2
    elif month_and_days >= '09-01' and month_and_days < '11-01':
        datetype = 3
    elif month_and_days >= '11-01':
        datetype = 4
    return datetype

def read_pro_mkt(reportdf, clsdf, datatype):
    '''
    读取报告和市值数据
    :param reportdf:
    :param clsdf:
    :return:
    '''
    #如果数据类型是3，表示交易日期在<= 09-01 <11-01之间
    if datatype == 3:
        t_1_q3_q4 = reportdf.iloc[2, 4] - reportdf.iloc[0, 4]
        t_q1_q2 = reportdf.iloc[4,4]
        ashare_np_sum = t_1_q3_q4 + t_q1_q2
        ashare_mkt = clsdf.iloc[0, 2]

    return ashare_np_sum, ashare_mkt


def load_stk_data(tradeDate, cons_list, datatype):
    '''
    根据数据类型和交易日得到数据
    :param tradeDate:
    :param datatype:
    :return:
    '''

    # 遍历指数样本的报告和市值信息
    profit_sum = 0
    mkt_sum = 0
    for cons in cons_list:
        reportpath = "../data/" + tradeDate + "/" + cons + "report.csv"
        reportdf = pd.read_csv(reportpath, index_col=0)
        reportdf.loc[:, ['TOTAL_SHARES', 'SHARE_TOTALA']] \
            = reportdf.loc[:, ['TOTAL_SHARES', 'SHARE_TOTALA']].fillna(method='bfill')
        reportdf['ASHARE_PCT'] = reportdf['SHARE_TOTALA'] / reportdf['TOTAL_SHARES']
        reportdf['ASHARE_NP'] = reportdf['NP_BELONGTO_PARCOMSH'] * reportdf['ASHARE_PCT']

        clspath = "../data/" + tradeDate + "/" +  cons + "cls.csv"
        clsdf = pd.read_csv(clspath, index_col=0)
        clsdf['ASHARE_MKT'] = clsdf['CLOSE'] * clsdf['SHARE_TOTALA']
        profit, mkt = read_pro_mkt(reportdf, clsdf, datatype)
        print(cons)
        print(mkt/profit)
        if profit <= 0:
            print("profit less zero")
        profit_sum += profit
        mkt_sum += mkt

    return profit_sum, mkt_sum




def load_cons(tradeDate, index_code):
    filepath = "../data/" + tradeDate + "/" + index_code + "cons.csv"
    # print(filepath)
    consdf = pd.read_csv(filepath, index_col=0)
    conslist = consdf['wind_code'].tolist()
    # print(consdf)
    return conslist

def cal_idx_valuation(tradeDate, index_code):
    '''
    计算指数估值数据
    根据不同的日期类型，得到的数据格式也有所不同，处理方式也有所不同
    :param tradeDate:
    :return:
    '''

    datatype = get_dataType(tradeDate)

    idx_cons = load_cons(tradeDate, index_code)
    print(idx_cons)
    profit_sum, mkt_sum = load_stk_data(tradeDate, idx_cons, datatype)
    print(mkt_sum/profit_sum)


if __name__ == '__main__':
    pd.set_option('display.max_columns', 999)
    tradeDate = "2019-09-02"
    index_code = '000016.SH'
    cal_idx_valuation(tradeDate, index_code)
