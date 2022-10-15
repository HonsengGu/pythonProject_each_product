import datetime
import pandas as pd
from numpy import *
import quantstats as qs
import numpy as np
from pyfolio.timeseries import perf_stats

def ratio(data_net_worth,benchmark_ret=None,drawdowns_out=False):
    trade_days = (data_net_worth.iloc[-1,1] - data_net_worth.iloc[0,1]).days
    data_net_worth.loc[:, "日收益率"] = data_net_worth.loc[:, "累计单位净值"].pct_change(1).fillna(0)
    # data_net_worth.loc[:, "日收益率"] = np.log(data_net_worth.loc[:, "累计单位净值"] / data_net_worth.loc[:, "累计单位净值"].shift(1))

    data_net_worth.loc[:, "历史最大净值"]=data_net_worth.loc[:, "累计单位净值"].cummax()
    data_net_worth.loc[:, "当日回撤（%）"]=round((1-(data_net_worth.loc[:, "累计单位净值"]/data_net_worth.loc[:, "历史最大净值"]))*100,2)
    data_net_worth.loc[:, "最大回撤（%）"]=round(data_net_worth.loc[:, "当日回撤（%）"].cummax(),2)
    data_net_worth_use=data_net_worth

    if benchmark_ret is not None:
        benchmark_ret.loc[:, "基准收益率"] = benchmark_ret.loc[:, "close"].pct_change().fillna(0)
        benchmark_data=benchmark_ret.iloc[-3000:,:]
        benchmark_data=benchmark_data.loc[:, ["trade_date","基准收益率"]]
        benchmark_data=benchmark_data.dropna()
        benchmark_data.loc[:, "trade_date"] = [datetime.datetime(int(str(i)[0:4]), int(str(i)[4:-2]),
                                                  int(str(i)[-2:])) for i in benchmark_data.loc[:, "trade_date"]]
        benchmark_data.columns = ["日期","基准收益率"]
        data_net_worth_use=data_net_worth_use.loc[:, ["净值日期", "日收益率"]]
        data_net_worth_use.columns=["日期", "日收益率"]

        data_net_worth_use = data_net_worth_use.astype({'日期': 'datetime64'})  # 设置类型
        data_merge=pd.merge(data_net_worth_use.loc[:, ["日期","日收益率"]],
                            benchmark_data.loc[:, ["日期","基准收益率"]],on="日期",how='left')

        data_merge=data_merge.set_index(["日期"])
        # data_merge=benchmark_data.loc[:, ["基准收益率"]].join(data_net_worth.loc[:, ["日收益率"]],  how='left')
        ratio_data = perf_stats(data_merge.loc[:, "日收益率"],data_merge.loc[:, "基准收益率"])
        # gen_drawdown=pf.timeseries.gen_drawdown_table(data_merge.loc[:, "日收益率"])
        data_anylyse = pd.DataFrame([{
            "最新净值": data_net_worth.loc[data_net_worth.index[-1], "累计单位净值"],
            "运作天数": str(trade_days),
            "年化收益": round(ratio_data["Annual return"] * 100, 2),
            "最大回撤": round(ratio_data["Max drawdown"] * 100, 2),
            "Sharpe": round(ratio_data["Sharpe ratio"], 2),
            "Calmar": round(ratio_data["Calmar ratio"], 2),
            "Sortino": round(ratio_data["Sortino ratio"], 2),
            "Var": round(ratio_data["Daily value at risk"] * 100, 2),
            "tail": round(ratio_data["Tail ratio"], 2),
            "Omega": round(ratio_data["Omega ratio"], 2),
            "Alpha": round(ratio_data["Alpha"], 2),
            "Beta": round(ratio_data["Beta"], 2),
        }])


    else:
        data_net_worth_use = data_net_worth_use.set_index(["净值日期"])
        ratio_data = perf_stats(data_net_worth_use.loc[:, "日收益率"])
        data_anylyse = pd.DataFrame([{
            "最新净值":  data_net_worth.loc[data_net_worth.index[-1],"累计单位净值"],
            "运作天数" : str(trade_days),
            "年化收益": round(ratio_data["Annual return"] * 100, 2),
            "最大回撤": round(ratio_data["Max drawdown"] * 100, 2),
            "Sharpe": round(ratio_data["Sharpe ratio"], 2),
            "Calmar": round(ratio_data["Calmar ratio"], 2),
            "Sortino": round(ratio_data["Sortino ratio"], 2),
            "Var": round(ratio_data["Daily value at risk"] * 100, 2),
            "tail": round(ratio_data["Tail ratio"], 2),
            "Omega": round(ratio_data["Omega ratio"], 2),
        }])


    top_drawdowns = None
    if drawdowns_out == True:
        try:
            # top_drawdowns = pf.timeseries.gen_drawdown_table(data_merge.loc[:, "日收益率"], top=5)
            # top_drawdowns.columns = ["回撤幅度（%）", "峰值日期", "谷值日期", "修复日期", "修复天数"]
            # top_drawdowns = top_drawdowns.iloc[::-1].reset_index(drop=True)
            # top_drawdowns.loc[:, "回撤幅度（%）"] = [round(x, 2) for x in top_drawdowns.loc[:, "回撤幅度（%）"]]  # 保留几位小叔
            # top_drawdowns.loc[:, "峰值日期"] = [x.strftime('%Y-%m-%d') for x in top_drawdowns.loc[:, "峰值日期"]]
            # top_drawdowns.loc[:, "谷值日期"] = [x.strftime('%Y-%m-%d') for x in top_drawdowns.loc[:, "谷值日期"]]
            # # top_drawdowns.loc[:, "修复日期"] =[x.strftime('%Y-%m-%d')  for x in top_drawdowns.loc[:, "谷值日期"]]

            top_drawdowns = qs.reports.full(data_merge.loc[:, "日收益率"])
            top_drawdowns = top_drawdowns.iloc[:, 0:5]
            top_drawdowns.columns = ["回撤开始日期", "谷底日期", "回撤修复日期", "修复天数", "回撤幅度"]
            top_drawdowns.loc[:, "回撤幅度"] = [round(x, 2) for x in top_drawdowns.loc[:, "回撤幅度"]]  # 保留几位小叔

        except:
            pass
        return data_net_worth, data_anylyse, top_drawdowns
    else:
        return data_net_worth, data_anylyse



