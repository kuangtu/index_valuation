# -*- coding: UTF-8 -*-
import pandas as pd

def read_test_data(report_file, cls_file, datatype):

    report_df = pd.read_csv(report_file, index_col=0)
    print(report_df)
    print(report_df.isnull().sum())

    # 填充
    # report_df.loc[:, ['TOTAL_SHARES', 'SHARE_TOTALA']] = report_df.loc[:, ['TOTAL_SHARES', 'SHARE_TOTALA']].bfill()
    # report_df.fillna(method='bfill', inplace=True)
    # report_df.ffill(inplace=True)
    # print(report_df)

    report_df['ASHARE_PCT'] = report_df['SHARE_TOTALA'] / report_df['TOTAL_SHARES']
    report_df['ASHARE_NP'] = report_df['NP_BELONGTO_PARCOMSH'] * report_df['ASHARE_PCT']
    print(report_df)

    cls_df = pd.read_csv(cls_file, index_col=0)
    cls_df['ashare_mkt'] = cls_df['CLOSE'] * cls_df['SHARE_TOTALA']
    print(cls_df)

    if datatype == 2:
        t_1_q2_q4 = report_df.iloc[3, 4] - report_df.iloc[0, 4]
        t_q1 = report_df.iloc[4, 4]
        ashare_np_sum = t_1_q2_q4 + t_q1
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print(syl)

    if datatype == 1:
        t_1_q1_q3 = report_df.iloc[4, 4]
        t_2_q4 = report_df.iloc[1,4] - report_df.iloc[0,4]
        ashare_np_sum = t_1_q1_q3 + t_2_q4
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print (syl)

    if datatype == 3:
        t_1_q3_q4 = report_df.iloc[2, 4] - report_df.iloc[0, 4]
        t_q1_q2 = report_df.iloc[4,4]
        ashare_np_sum = t_1_q3_q4 + t_q1_q2
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print (syl)

    if datatype == 4:
        t_1_q4 = report_df.iloc[1, 4] - report_df.iloc[0, 4]
        t_2_q1_q2_q3 = report_df.iloc[4, 4]
        ashare_np_sum = t_1_q4 + t_2_q1_q2_q3
        ashare_mkt = cls_df.iloc[0, 2]
        syl = ashare_mkt / ashare_np_sum
        print (syl)


if __name__ == '__main__':
    # report_file = "../data/600519.csv"
    # cls_file = "../data/600519_cls.csv"
    # report_file = "../data/600000.csv"
    # cls_file = "../data/600000_cls.csv"
    # report_file = "../data/300750.csv"
    # cls_file = "../data/300750_cls.csv"
    # report_file = "../data/600519_5_1.csv"
    # cls_file = "../data/600519_5_1_cls.csv"
    report_file = "../data/600519_12_12.csv"
    cls_file = "../data/600519_12_12_cls.csv"
    datatype = 4
    read_test_data(report_file, cls_file, datatype)