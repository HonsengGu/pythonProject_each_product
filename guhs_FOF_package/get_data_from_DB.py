
from pymongo import MongoClient
import pandas as pd
import tushare as ts
pro = ts.pro_api("ab9bd05c38852f579af7c43978e914a93e242e19e760dedb310ed827")


def get():
    client = MongoClient('localhost', 27017)
    db = client['飒露紫子基金净值汇总']
    table = db['Df_Mongo']
    # 读取数据
    data_net_worth= pd.DataFrame(list(table.find()))[["产品名称","日期","累计单位净值",'单位净值']]
    try:
        data_net_worth["累计单位净值"] = pd.to_numeric(data_net_worth["累计单位净值"], errors='coerce')
        client.close()
    except:
        client.close()
    return data_net_worth



def get_FOF_eachday():
    # i = datetime.datetime.now()
    # diff_day = datetime.datetime.now().strftime("%p")
    # today = str("%s%s%s" % (i.year, i.month, i.day))
    client = MongoClient('localhost', 27017)
    db = client['Daily_show']
    # collection_list=db.list_collection_names()
    table = db["FOF"]
    # ["Df_Mongo" + "_" + today + "_" + diff_day]

    try:
        data = pd.DataFrame(list(table.find()))[["标签","产品名称","日期","当日累计净值","单位净值","日收益率","当日回撤","最大回撤","起始日期","年化收益","夏普比率","运作天数","初始资金（万元）","经纪商","所属项目"]]
        client.close()
    except:
        client.close()
    return data







