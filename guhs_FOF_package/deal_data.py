import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import MultipleLocator
def set_tick(data):
    if len(data) >= 360:
        x_major_locator = MultipleLocator(16)
    else:
        if 270 <= len(data) < 360:
            x_major_locator = MultipleLocator(15)
        if 180 <= len(data) < 270:
            x_major_locator = MultipleLocator(13)
        if 120 <= len(data) < 180:
            x_major_locator = MultipleLocator(11)
        if 90 <= len(data) < 120:
            x_major_locator = MultipleLocator(8)
        if 30 <= len(data) < 90:
            x_major_locator = MultipleLocator(4)
        if len(data) < 30:
            x_major_locator = MultipleLocator(2)
    proper_tick = x_major_locator
    ax = plt.gca()
    ax.xaxis.set_major_locator(proper_tick)
    # plt.tick_params(labelsize=6)  # 坐标值字体大小
    plt.xticks(rotation=45)
    plt.tight_layout()

def deal_data(data_net_worth_tatal,useless_list,trade_days):
    useless_list_pro=['孚盈飒露紫一号私募证券投资基金']
    data_net_worth_part_total= data_net_worth_tatal.groupby(["产品名称"])  # 按照合约品种分裂并求和
    data_merge= pd.DataFrame(columns=[ '日期'])

    for group in data_net_worth_part_total:
        product_name=group[0]
        if product_name in useless_list:
            pass
        else:
            group_new = group[1]  # 提取数组中的列表
            group_new = pd.DataFrame(group_new)
            group_new = group_new.reset_index(drop=True)
            data_net_worth = group_new.sort_values(by='日期', ascending=True, inplace=True)
            data_net_worth = group_new.reset_index(drop=True)
            data_net_worth.rename(columns={"累计单位净值": product_name}, inplace=True)
            if  len(data_net_worth)>trade_days:
            # data_net_worth['日期'] = pd.to_datetime(data_net_worth['日期'])
                data_merge = pd.merge(data_merge, data_net_worth[["日期", product_name]], on='日期', how='outer')
                data_merge.sort_values(by='日期', ascending=True, inplace=True)

            else:
                useless_list_pro.append(product_name)
            # data_merge['日期'] = pd.to_datetime(data_merge['日期'])
        data_merge.to_csv("子基金净值数据汇总.csv")
    return  data_merge,useless_list_pro