import pandas as pd
import os
import matplotlib.ticker as ticker
from pyfolio.tears import create_full_tear_sheet,create_interesting_times_tear_sheet,create_interesting_times_tear_df
from  guhs_FOF_package.roll_returuns import *
from guhs_ratio.out_pyratio import pyratio,out_pic,out_special_pic
import empyrical as ep
import matplotlib.pyplot as plt
import time
plt.rcParams['font.sans-serif']=['SimHei']
path = os.getcwd()
file_list = os.listdir(path)
file_list = [file for file in file_list if file.endswith('.xlsx') or file.endswith('.xls') or   file.endswith('.csv') ]
try:

    for file in file_list:
        print("正在处理文件,请等待：",file)
        time.sleep(1)
        name=file.split('.')[0]
        each_file_path = path   + '\\' + name
        #新建一个文件夹，用于存放每个基金的结果
        if not os.path.exists(each_file_path):
            os.makedirs(each_file_path)
        data_input = pd.read_excel(file)
        data_input.columns = ["日期", "累计单位净值"]
        data_input.sort_values(by='日期', ascending=True, inplace=True)
        try:
            data_input.loc[:, "日期"] = [(''.join(filter(str.isalnum, str(x))))[0:8] for x in data_input.loc[:, "日期"]]
        except:
            data_input.loc[:, "日期"] = [x.strftime('%Y-%m-%d') for x in data_input.loc[:, "日期"]]
            data_input.loc[:, "日期"] = [''.join(filter(str.isalnum, x)) for x in data_input.loc[:, "日期"]]

        data_input_new = data_input.set_index(["日期"])

        data_net_worth, data_anylyse, top_drawdowns = pyratio(data_input_new, drawdowns_out=True)

        return_value = pd.DataFrame()
        select_day = data_net_worth.index[-1]

        return_value, w_ret, m_ret, Q_ret, A_ret, d_ret, latest_day, d_net_worth = roll_return_values(data_net_worth, return_value, str(file), select_day)

        out_pic(data_net_worth.loc[:, "日收益率"],each_file_path,top_drawdowns)

        d_data = pd.DataFrame(round(d_ret, 3)).dropna()
        A_data = pd.DataFrame(round(A_ret, 3)).dropna()
        w_data = pd.DataFrame(round(w_ret, 3)).dropna()
        m_data = pd.DataFrame(round(m_ret, 3)).dropna()
        q_data = pd.DataFrame(round(Q_ret, 3)).dropna()

        fig_period, (ax0, ax1,  ax2) = plt.subplots(3, 1, figsize=(20, 8))
        fig_period.suptitle('周期收益率', fontsize=20)
        (w_data.loc[:, "日收益率"]).plot.bar(ax=ax0, color='#3299CC', lw=3.0, label='周度收益（%）', rot=0, fontsize=13,grid=False)
        (m_data.loc[:, "日收益率"]).plot.bar(ax=ax1, color='#E47833', lw=3.0, label='月度收益（%）', rot=0, fontsize=13,grid=False)
        (q_data.loc[:, "日收益率"]).plot.bar(ax=ax2, color='#C0C0C0', lw=3.0, label='季度收益（%）', rot=0, fontsize=13,grid=False)
        # 设定标签位置

        ax0.xaxis.set_major_locator(ticker.MultipleLocator(int(len(w_data) / 5)))
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(int(len(m_data) / 5)))
        ax2.xaxis.set_major_locator(ticker.MultipleLocator(int(len(q_data) / 5)))
        # 同时绘制双轴的图例
        h1, l1 = ax0.get_legend_handles_labels()
        h2, l2 = ax1.get_legend_handles_labels()
        h3, l3 = ax2.get_legend_handles_labels()

        plt.legend(h1+h2+h3 , l1+l2+l3 , fontsize=12, loc='upper left', ncol=1)
        fig_period.tight_layout()  # 规整排版
        plt.savefig(each_file_path+'//定期收益图.png')


        data_input_new.index = pd.to_datetime(data_input_new.index)
        data_input_new.loc[:, "日收益率"] = data_input_new.loc[:, "累计单位净值"].pct_change().fillna(0)

        create_interesting_times_tuple = create_interesting_times_tear_df(data_net_worth.loc[:, "日收益率"])
        interesting_time_describe = create_interesting_times_tuple[0].reset_index()

        interesting_time_describe.rename(columns={"index": "特殊时期净值分析"}, inplace=True)

        count = 0

        for k, v in create_interesting_times_tuple[1].items():
            count = count + 1
            interesting_show = pd.DataFrame(ep.cum_returns(v, starting_value=1)).round(3)
            interesting_show.index = interesting_show.index.strftime('%Y-%m-%d')
            interesting_show.rename(columns={0: "归一净值"}, inplace=True)
            out_special_pic(v,each_file_path,k)

    print("处理完成,您可以退出")
    time.sleep(30)
except:

    print("代码出现错误,您可以退出")
    time.sleep(30)