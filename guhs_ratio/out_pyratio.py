import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import datetime
import quantstats as qs
import numpy as np
from pyfolio.timeseries import perf_stats
import pyfolio
import empyrical  as  em
plt.rcParams['font.sans-serif']=['SimHei']


def pyratio(data_net_worth,drawdowns_out=False):
    data_net_worth.index=[datetime.datetime(int(str(i)[0:4]), int(str(i)[4:-2]), int(str(i)[-2:]))  for i in data_net_worth.index.values.tolist()]

    trade_days=(data_net_worth.index[-1]-data_net_worth.index[0]).days
    data_net_worth.loc[:, "日收益率"]=data_net_worth.loc[:,"累计单位净值"].pct_change().fillna(0)
    ratio_data=perf_stats(data_net_worth.loc[:, "日收益率"])
    data_anylyse = pd.DataFrame([{
                                "最新净值": data_net_worth.loc[data_net_worth.index[-1],"累计单位净值"],
                                "天数": str(trade_days),
                                  "年化收益":round(ratio_data["Annual return"]*100, 2),
                                  "最大回撤": round(ratio_data["Max drawdown"]*100, 2),
                                  "Sharpe": round(ratio_data["Sharpe ratio"], 2),
                                  "Calmar": round(ratio_data["Calmar ratio"], 2),
                                  "Sortino": round(ratio_data["Sortino ratio"], 2),
                                    "Var":round(ratio_data["Daily value at risk"]*100, 2),
                                    "tail":round(ratio_data["Tail ratio"], 2),
                                    "Omega":round(ratio_data["Omega ratio"], 2),
                                  }])

    top_drawdowns = None
    if drawdowns_out == True:
        try:
            top_drawdowns=qs.reports.full(data_net_worth.loc[:, "日收益率"])
            top_drawdowns=top_drawdowns.iloc[:,0:5]
            top_drawdowns.columns = ["回撤开始日期", "谷底日期", "回撤修复日期", "修复天数", "回撤幅度"]
            top_drawdowns.loc[:, "回撤幅度"] = [round(x, 2) for x in top_drawdowns.loc[:, "回撤幅度"]]  # 保留几位小叔
        except:
            pass
        return data_net_worth, data_anylyse,top_drawdowns
    else:
        return data_net_worth, data_anylyse

def out_pic(pct_serise,each_file_path,top_drawdowns):
    pnl = pd.Series(pct_serise)
    cumulative=em.cum_returns(pnl,starting_value=1)

    max_return = cumulative.cummax()
    drawdown = (cumulative - max_return) / max_return
    perf_stats_year = (pnl).groupby(pnl.index.to_period('y')).apply(lambda data: pyfolio.timeseries.perf_stats(data)).unstack()
    perf_stats_all = pyfolio.timeseries.perf_stats((pnl)).to_frame(name='all')
    perf_stats = pd.concat([perf_stats_year, perf_stats_all.T], axis=0)
    perf_stats_ = round(perf_stats,4).reset_index()

    if  top_drawdowns.empty:
        fig, (ax0, ax1) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[1.5, 4]}, figsize=(20,8))
        fig.suptitle("净值情况", fontsize=20)
        cols_names = ['日期', '年化\n收益', '累计\n收益', '年化\n波动',
               '夏普\n比率', '卡马\n比率', 'Stability', '最大\n回撤',
               'Omega\nratio', '索提诺\n比率', '偏度', '峰度', 'Tail\nratio',
               'Daily value\nat risk']
        # 绘制表格
        ax0.set_axis_off() # 除去坐标轴
        table = ax0.table(cellText = perf_stats_.values,
                        bbox=(0,0,1,1), # 设置表格位置， (x0, y0, width, height)
                        rowLoc = 'right', # 行标题居中
                        cellLoc='right' ,
                        colLabels = cols_names, # 设置列标题
                        colLoc = 'right', # 列标题居中
                        edges = 'open' # 不显示表格边框
                        )
        table.set_fontsize(18)
        # 绘制累计收益曲线
        ax2 = ax1.twinx()
        ax1.yaxis.set_ticks_position('right') # 将回撤曲线的 y 轴移至右侧
        ax2.yaxis.set_ticks_position('left') # 将累计收益曲线的 y 轴移至左侧
        # 绘制回撤曲线
        drawdown.plot.area(ax=ax1, label='drawdown (right)', rot=0, alpha=0.3, fontsize=13, grid=False)
        # 绘制累计收益曲线
        (cumulative).plot(ax=ax2, color='#F1C40F' , lw=3.0, label='cumret (left)', rot=0, fontsize=13, grid=False)
        # 不然 x 轴留有空白
        ax2.set_xbound(lower=cumulative.index.min(), upper=cumulative.index.max())
        # 主轴定位器：每 5 个月显示一个日期：根据具体天数来做排版
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(int(len(cumulative)/5)))
        # 同时绘制双轴的图例
        h1,l1 = ax1.get_legend_handles_labels()
        h2,l2 = ax2.get_legend_handles_labels()
        plt.legend(h1+h2,l1+l2, fontsize=12, loc='upper left', ncol=1)
        fig.tight_layout() # 规整排版
        #保存图片
        plt.savefig(each_file_path+'\\净值图和风险指标.png')
    else:
        fig, (ax0, ax1, ax0_pro) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [2, 4,2]}, figsize=(20, 8))
        fig.suptitle("净值情况", fontsize=20)
        cols_names = ['日期', '年化\n收益', '累计\n收益', '年化\n波动',
                      '夏普\n比率', '卡马\n比率', 'Stability', '最大\n回撤',
                      'Omega\nratio', '索提诺\n比率', '偏度', '峰度', 'Tail\nratio',
                      'Daily value\nat risk']
        # 绘制表格
        ax0.set_axis_off()  # 除去坐标轴
        table = ax0.table(cellText=perf_stats_.values,
                          bbox=(0, 0, 1, 1),  # 设置表格位置， (x0, y0, width, height)
                          rowLoc='right',  # 行标题居中
                          cellLoc='right',
                          colLabels=cols_names,  # 设置列标题
                          colLoc='right',  # 列标题居中
                          edges='open'  # 不显示表格边框
                          )
        table.set_fontsize(14)
        ax2 = ax1.twinx()
        ax1.yaxis.set_ticks_position('right')  # 将回撤曲线的 y 轴移至右侧
        ax2.yaxis.set_ticks_position('left')  # 将累计收益曲线的 y 轴移至左侧
        # 绘制回撤曲线
        drawdown.plot.area(ax=ax1, label='drawdown (right)', rot=0, alpha=0.3, fontsize=13, grid=False)
        # 绘制累计收益曲线
        (cumulative).plot(ax=ax2, color='#F1C40F', lw=3.0, label='cumret (left)', rot=0, fontsize=13, grid=False)
        # 不然 x 轴留有空白
        ax2.set_xbound(lower=cumulative.index.min(), upper=cumulative.index.max())
        # 主轴定位器：每 5 个月显示一个日期：根据具体天数来做排版
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(int(len(cumulative) / 5)))
        # 同时绘制双轴的图例
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()


        cols_names_pro = ["回撤开始日期", "谷底日期", "回撤修复日期", "修复天数", "回撤幅度"]
        # 绘制表格
        ax0_pro.set_axis_off()  # 除去坐标轴
        table_pro = ax0_pro.table(cellText=top_drawdowns.values,
                                  bbox=(0, 0, 1, 1),  # 设置表格位置， (x0, y0, width, height)
                                  rowLoc='right',  # 行标题居中
                                  cellLoc='right',
                                  colLabels=cols_names_pro,  # 设置列标题
                                  colLoc='right',  # 列标题居中
                                  edges='open'  # 不显示表格边框
                                  )
        table_pro.set_fontsize(18)

        plt.legend(h1 + h2, l1 + l2, fontsize=12, loc='upper left', ncol=1)
        fig.tight_layout()  # 规整排版
        # 保存图片
        plt.savefig(each_file_path + '\\净值图和风险指标.png')


def out_special_pic(pct_serise,each_file_path,k):
    pnl = pd.Series(pct_serise)
    cumulative=em.cum_returns(pnl,starting_value=1)
    max_return = cumulative.cummax()
    drawdown = (cumulative - max_return) / max_return
    perf_stats_all = pyfolio.timeseries.perf_stats((pnl)).to_frame(name='all')
    perf_stats = perf_stats_all.T
    perf_stats_ = round(perf_stats,4).reset_index()
    fig, (ax0, ax1) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[1.5, 4]}, figsize=(20,8))
    #增加标题
    fig.suptitle(k+"净值情况", fontsize=20)
    cols_names = [ '年化\n收益', '累计\n收益', '年化\n波动',
           '夏普\n比率', '卡马\n比率', 'Stability', '最大\n回撤',
           'Omega\nratio', '索提诺\n比率', '偏度', '峰度', 'Tail\nratio',
           'Daily value\nat risk']
    # 绘制表格
    # print(perf_stats_.values[0].drop('all'))
    #numpy.ndarray去掉某个元素

    ax0.set_axis_off() # 除去坐标轴
    table = ax0.table(cellText =[np.delete(perf_stats_.values[0],0)],
                    bbox=(0,0,1,1), # 设置表格位置， (x0, y0, width, height)
                    rowLoc = 'right', # 行标题居中
                    cellLoc='right' ,
                    colLabels = cols_names, # 设置列标题
                    colLoc = 'right', # 列标题居中
                    edges = 'open' # 不显示表格边框
                    )
    table.set_fontsize(18)
    # 绘制累计收益曲线
    ax2 = ax1.twinx()
    ax1.yaxis.set_ticks_position('right') # 将回撤曲线的 y 轴移至右侧
    ax2.yaxis.set_ticks_position('left') # 将累计收益曲线的 y 轴移至左侧
    # 绘制回撤曲线
    drawdown.plot.area(ax=ax1, label='drawdown (right)', rot=0, alpha=0.3, fontsize=13, grid=False)
    # 绘制累计收益曲线
    (cumulative).plot(ax=ax2, color='#F1C40F' , lw=3.0, label='cumret (left)', rot=0, fontsize=13, grid=False)
    # 不然 x 轴留有空白
    ax2.set_xbound(lower=cumulative.index.min(), upper=cumulative.index.max())
    # 主轴定位器：每 5 个月显示一个日期：根据具体天数来做排版
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(int(len(cumulative)/5)))
    # 同时绘制双轴的图例
    h1,l1 = ax1.get_legend_handles_labels()
    h2,l2 = ax2.get_legend_handles_labels()
    plt.legend(h1+h2,l1+l2, fontsize=12, loc='upper left', ncol=1)
    fig.tight_layout() # 规整排版
    #保存图片
    plt.savefig(each_file_path+'\\'+k+'净值情况.png')