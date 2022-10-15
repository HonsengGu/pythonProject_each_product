
from pyfinance import TSeries
import numpy as np


def roll_return_values(data_net_worth,return_value,group_name,select_day):
    data_net_worth.loc[:, "日收益率"]=data_net_worth.loc[:,"累计单位净值"].pct_change().fillna(0)
    data_net_worth=data_net_worth[data_net_worth.index<=select_day]

    tss = TSeries(data_net_worth.loc[:, "日收益率"], freq="D")
    tss_year = TSeries(data_net_worth.loc[:, "日收益率"], freq="D")

    d_ret = round(tss.rollup(freq='D') * 100, 2)
    w_ret = round(tss.rollup(freq='W')*100,2)
    m_ret = round(tss.rollup(freq='M')*100,2)
    Q_ret = round(tss.rollup(freq='Q')*100,2)
    A_ret = round(tss_year.rollup(freq='A')*100,2)
    d_ret.index=[x.strftime('%y-%m-%d') for x in d_ret.index]
    w_ret.index=[x.strftime('%y-%m-%d') for x in w_ret.index]
    m_ret.index = [x.strftime('%y-%m-%d') for x in m_ret.index]
    Q_ret.index = [x.strftime('%y-%m-%d') for x in Q_ret.index]
    A_ret.index = [x.strftime('%y-%m-%d') for x in A_ret.index]
    try:
        d_net_worth = data_net_worth.loc[data_net_worth.index[-1], "累计单位净值"]
        latest_day = data_net_worth.index[-1].strftime('%y-%m-%d')
        return_value=return_value.append([[group_name,latest_day,d_net_worth,w_ret[-1],w_ret.index[-1],m_ret[-1],m_ret.index[-1],Q_ret[-1],Q_ret.index[-1],A_ret[-1],A_ret.index[-1]]], ignore_index=True)
    except:
        d_net_worth=np.nan
        latest_day=np.nan
        return_value = return_value.append([[group_name,"暂无数据","暂无数据", "暂无数据", "暂无数据", "暂无数据", "暂无数据",
                                             "暂无数据", "暂无数据", "暂无数据", "暂无数据"]],
                                           ignore_index=True)

    new_data=return_value

    return new_data,w_ret,m_ret,Q_ret,A_ret,d_ret,latest_day,d_net_worth







