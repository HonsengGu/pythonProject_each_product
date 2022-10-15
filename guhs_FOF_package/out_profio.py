
import  pandas as pd

def profilo(data_fof,found_list):
    data_temp=data_fof[data_fof.loc[:,"产品名称"].str.contains(found_list[0])]
    data_temp.rename(columns={"累计单位净值": "example"}, inplace=True)
    data_temp=data_temp[["日期","example"]]
    for name in found_list:
        data_each = data_fof[data_fof.loc[:,"产品名称"].str.contains(name)]
        data_each.rename(columns={"累计单位净值": name}, inplace=True)
        data_temp = pd.merge(data_temp, data_each[["日期",name]], on='日期', how='outer')
    df_merge = data_temp.sort_values(by='日期', ascending=True)
    df_merge=df_merge.drop("example",axis=1)
    df_merge=df_merge.reset_index(drop=True)
    return  df_merge


