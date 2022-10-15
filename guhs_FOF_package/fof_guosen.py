import pandas as pd
from streamlit_apex_charts import  bar_chart, pie_chart
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
import streamlit as st
import openpyxl
def guosen_fof(uploaded_file):
    for excel_name in uploaded_file:
        wb = openpyxl.load_workbook(excel_name)
        # 获取正在活跃的表单worksheet
        ws = wb.active
        ws.delete_rows(0)  # 删除index为2后面的bai2行
        ws.delete_rows(0)  # 删除index为2后面的bai2行
        wb.save("temp.xlsx")
        product_data = pd.read_excel("temp.xlsx")
        # product_data=product_data.set_index(["科目代码"],drop=True)
        product_data=product_data.dropna()
        product_data = product_data[product_data.loc[:, "科目代码"].str.contains('11090601') ].reset_index()
        product_data.loc[:, "科目名称"]=product_data.loc[:, "科目名称"].map(lambda x:x[:-8])#修改为日期格式
        label = pd.read_excel(r"C:\Users\Administrator\Desktop\python过程涉及\FOF\飒露紫子基金策略分类\飒露紫子基金策略分类.xlsx")[
            ["产品名称", "标签"]]
        label.loc[:, "标签"] = label.loc[:, "标签"].fillna("待补充")
        label=label.rename(columns={"产品名称": "科目名称"})
        product_data_new=pd.merge(product_data, label, on='科目名称', how='left')
        product_data_new.loc[:, "科目名称"]=product_data_new.loc[:, "科目名称"].map(lambda x: x.strip())
        product_data_new.loc[:, "增值/本金"] = product_data_new.loc[:, "估值增值"]/product_data_new.loc[:, "成本"]

    s0, s1 = st.columns(2)
    with s0:
        data_show_0=product_data_new.loc[:, ["科目名称","成本"]].set_index(["科目名称"]).T
        pie_chart("单个产品本金/投资子层产品全部本金(%)", data_show_0)
    with s1:
        data_show_1=product_data_new.loc[:, ["标签","成本"]].set_index(["标签"])
        data_show_1=data_show_1.groupby(["标签"]).sum().T
        pie_chart("策略本金/投资子层产品全部本金(%)", data_show_1)


    s2, s3= st.columns(2)
    with s2:
        data_show_2 = product_data_new.loc[:, ["科目名称", "增值/本金"]].set_index(["科目名称"]).sort_values(by='增值/本金')

        data_show_2.loc[:, "增值/本金"] = data_show_2.loc[:, "增值/本金"].map(lambda x:round(100*x,2))
        bar_chart("估值增值/本金(%)", data_show_2)
    with s3:
        data_show_3 = product_data_new.loc[:, ["标签", "估值增值","成本"]]
        data_show_3 = data_show_3.groupby(["标签"]).sum()
        data_show_3.loc[:, "增值/本金"] = (data_show_3.loc[:, "估值增值"]/ data_show_3.loc[:, "成本"]).map(lambda x:round(100*x,2))
        bar_chart("不同策略增值/本金(%)", data_show_3.loc[:, ["增值/本金"]].sort_values(by='增值/本金'))

    s4, s5 = st.columns(2)
    with s4:
        data_show_4 = product_data_new.loc[:, ["科目名称", "估值增值"]].set_index(["科目名称"]).sort_values(by='估值增值')
        data_show_4.loc[:, "估值增值"] = data_show_4.loc[:, "估值增值"].map(lambda x: round( x/10000, 2))
        bar_chart("估值增值(万)", data_show_4)
    with s5:
        data_show_5 = product_data_new.loc[:, ["标签", "估值增值"]].set_index(["标签"])
        data_show_5 = data_show_5.groupby(["标签"]).sum().sort_values(by='估值增值')
        data_show_5.loc[:, "估值增值"] = data_show_5.loc[:, "估值增值"].map(lambda x: round( x/10000, 2))
        bar_chart("不同策略增值(万)", data_show_5)




