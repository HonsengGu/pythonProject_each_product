import tushare as ts
import pandas as pd
pro = ts.pro_api("ab9bd05c38852f579af7c43978e914a93e242e19e760dedb310ed827")

pd.set_option('display.max_columns', None)
# #显示所有行
pd.set_option('display.max_rows', None)
def relation(type,data_net_worth):
    beginday=str(data_net_worth.iloc[0,1] )#净值日期
    endday=str(data_net_worth.iloc[-1,1])

    df_nh = pro.index_daily(ts_code='NHCI.NH', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_300 = pro.index_daily(ts_code='399300.SZ', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_500 = pro.index_daily(ts_code='399905.SZ', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_farming_future = pro.index_daily(ts_code='NHAI.NH', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_energe_future = pro.index_daily(ts_code='NHECI.NH', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_black_future = pro.index_daily(ts_code='NHFI.NH', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_industory_future = pro.index_daily(ts_code='NHII.NH', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_colour_future = pro.index_daily(ts_code='NHNFI.NH', start_date=beginday, end_date=endday)[["trade_date", "close"]]

    df_expensive_future = pro.index_daily(ts_code='NHPMI.NH', start_date=beginday, end_date=endday)[["trade_date", "close"]]


    df_nh.columns = ['净值日期', '南华指数']
    df_300.columns = ['净值日期', '沪深300指数']
    df_500.columns = ['净值日期', '中证500']
    df_farming_future.columns = ['净值日期', '南华农产品指数']
    df_energe_future.columns = ['净值日期', '南华能化指数']
    df_black_future.columns = ['净值日期', '南华黑色指数']
    df_industory_future.columns = ['净值日期', '南华工业指数']
    df_colour_future.columns = ['净值日期', '南华有色金属指数']
    df_expensive_future.columns = ['净值日期', '南华贵金属指数']

    df_nh = df_nh.sort_values(by='净值日期', ascending=True, inplace=False)
    df_300 = df_300.sort_values(by='净值日期', ascending=True, inplace=False)
    df_500 = df_500.sort_values(by='净值日期', ascending=True, inplace=False)
    df_farming_future = df_farming_future.sort_values(by='净值日期', ascending=True, inplace=False)
    df_energe_future = df_energe_future.sort_values(by='净值日期', ascending=True, inplace=False)
    df_black_future = df_black_future.sort_values(by='净值日期', ascending=True, inplace=False)
    df_industory_future = df_industory_future.sort_values(by='净值日期', ascending=True, inplace=False)
    df_colour_future = df_colour_future.sort_values(by='净值日期', ascending=True, inplace=False)
    df_expensive_future = df_expensive_future.sort_values(by='净值日期', ascending=True, inplace=False)

    df_nh = df_nh.reset_index(drop=True)
    df_300 = df_300.reset_index(drop=True)
    df_500 = df_500.reset_index(drop=True)
    df_farming_future = df_farming_future.reset_index(drop=True)
    df_energe_future = df_energe_future.reset_index(drop=True)
    df_black_future = df_black_future.reset_index(drop=True)
    df_industory_future = df_industory_future.reset_index(drop=True)
    df_colour_future = df_colour_future.reset_index(drop=True)
    df_expensive_future = df_expensive_future.reset_index(drop=True)

    df_nh.loc[:,"南华指数_日收益"] = df_nh.loc[:, "南华指数"].pct_change(1)

    df_300.loc[:,"沪深300指数_日收益"] = df_300.loc[:, "沪深300指数"].pct_change(1)

    df_500.loc[:,"中证500_日收益"] =df_500.loc[:, "中证500"].pct_change(1)

    df_farming_future.loc[:,"南华农产品指数_日收益"] = df_farming_future.loc[:,"南华农产品指数"] .pct_change(1)

    df_energe_future.loc[:,"南华能化指数_日收益"] = df_energe_future.loc[:,"南华能化指数"].pct_change(1)

    df_black_future.loc[:,"南华黑色指数_日收益"] = df_black_future.loc[:,"南华黑色指数"] .pct_change(1)

    df_industory_future.loc[:,"南华工业指数_日收益"] = df_industory_future.loc[:,"南华工业指数"] .pct_change(1)

    df_colour_future.loc[:,"南华有色金属指数_日收益"] =df_colour_future.loc[:,"南华有色金属指数"] .pct_change(1)

    df_expensive_future.loc[:,"南华贵金属指数_日收益"] =df_expensive_future.loc[:,"南华贵金属指数"] .pct_change(1)

    data_net_worth.loc[:,'净值日期'] = [str(i) for i in data_net_worth.loc[:,'净值日期']]


    product_data_index = data_net_worth
    data_net_worth.loc[:,"日收益率"] =data_net_worth.loc[:,"累计单位净值"] .pct_change(1)

    product_data_index=pd.merge(product_data_index, df_nh[['净值日期', '南华指数']], on='净值日期', how='left')
    product_data_index=pd.merge(product_data_index, df_300[['净值日期', '沪深300指数']], on='净值日期', how='left')
    product_data_index = pd.merge(product_data_index, df_500[['净值日期', '中证500']], on='净值日期', how='left')
    product_data_index = pd.merge(product_data_index,  df_farming_future[['净值日期', '南华农产品指数']], on='净值日期', how='left')
    product_data_index = pd.merge(product_data_index,  df_energe_future[['净值日期', '南华能化指数']], on='净值日期', how='left')
    product_data_index = pd.merge(product_data_index,  df_black_future[['净值日期', '南华黑色指数']], on='净值日期', how='left')
    product_data_index = pd.merge(product_data_index, df_industory_future[['净值日期', '南华工业指数']], on='净值日期', how='left')
    product_data_index = pd.merge(product_data_index, df_colour_future[['净值日期', '南华有色金属指数']], on='净值日期', how='left')
    product_data_index = pd.merge(product_data_index, df_expensive_future[['净值日期', '南华贵金属指数']], on='净值日期', how='left')




    product_data_index=product_data_index.reset_index(drop=True)

    data_temp = data_net_worth[['净值日期', '日收益率']]
    # data_temp.loc[:,'净值日期'] = [str(i) for i in data_temp.loc[:,'净值日期']]
    data_temp = pd.DataFrame(data_temp)

    df_merge = pd.merge(data_temp, df_nh, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_300, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_500, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_farming_future, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_energe_future, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_black_future, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_industory_future, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_colour_future, on='净值日期', how='left')
    df_merge = pd.merge(df_merge, df_expensive_future, on='净值日期', how='left')
    df_merge = df_merge[['日收益率', "南华指数_日收益", "沪深300指数_日收益", 
                         '中证500_日收益', "南华农产品指数_日收益", "南华能化指数_日收益",
                         "南华黑色指数_日收益", "南华工业指数_日收益",
                        "南华有色金属指数_日收益", "南华贵金属指数_日收益"]]

    df_merge.columns = [type, "南华指数", "沪深300指数", '中证500', "南华农产品指数", "南华能化指数", "南华黑色指数", "南华工业指数",
                        "南华有色金属指数", "南华贵金属指数"]

    corr = df_merge.corr('pearson')
    corr = corr.fillna(0)
    corr=round(corr,2)

    return corr,product_data_index


def profio_relation(found_profilo):

    found_profilo_temp=found_profilo.iloc[:,1:]
    found_profilo_temp=found_profilo_temp.pct_change(1)
    found_profilo_cor = found_profilo_temp.corr('pearson')
    found_profilo_cor = round(found_profilo_cor, 2)

    return found_profilo_cor

