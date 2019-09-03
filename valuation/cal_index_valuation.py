# -*- coding: UTF-8 -*-
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

def load_data(tradeDate, index_code, datatype):
    '''
    根据数据类型和交易日得到数据
    :param tradeDate:
    :param datatype:
    :return:
    '''

    #如果数据类型是3，表示交易日期在<= 09-01 <11-01之间
    if datatype == 3:


def cal_idx_valuation(tradeDate, index_code):
    '''
    计算指数估值数据
    根据不同的日期类型，得到的数据格式也有所不同，处理方式也有所不同
    :param tradeDate:
    :return:
    '''

    datatype = get_dataType(tradeDate)
    print(datatype)

    load_data(tradeDate, index_code, datatype)


if __name__ == '__main__':
    tradeDate = "2019-09-02"
    index_code = '000016.SH'
    cal_idx_valuation(tradeDate, index_code)
