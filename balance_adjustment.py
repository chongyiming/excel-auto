import streamlit as st
import pandas as pd
from io import StringIO
import pymysql
option = st.selectbox(
    "Select Type",
    ("ST1","ST2","ST4"),
)

login = st.text_input("Login")
ticket = st.text_input("Ticket")


if option=="ST2":
    server="startrader2report"
elif option=="ST4":
    server="startrader4report"
elif option=="ST3":
    server="startrader3report"
elif option=="ST1":
    server="ivreport"
elif option=="UM":
    server="oplreport"

if option == "ST2" or option == "ST4" or option == "ST3" or option == "UM":
    db=pymysql.connect(host = "live-mt4-reportdb-repl-sg-03.vi-data.net", port = 3306, user = "reader_MY", passwd = "GC+Pb#Fw6?X-", db = server)
elif option == "ST1":
    db=pymysql.connect(host = "live-mt4-reportdb-repl-sg-02.vi-data.net", port = 3306, user = "reader_MY", passwd = "GC+Pb#Fw6?X-", db = server)

cursor=db.cursor()
sql = f"""
SELECT 
    t.LOGIN,
    t.PROFIT,
    u.NAME,
    u.GROUP
FROM {server}.mt4_trades AS t
JOIN {server}.mt4_users AS u
    ON t.LOGIN = u.LOGIN
WHERE t.LOGIN = {login} AND LOWER(t.COMMENT) = 'star-deposit'
LIMIT 1;
"""
cursor.execute(sql)
data = cursor.fetchall()
row=pd.DataFrame(list(data),columns=['login','profit','name','group'])
st.dataframe(row)

if len(row)>0:
    if row['profit'].iloc[0]>0:
        st.write(f'操作的manager名稱：YM-MY-Admin 帳號：{login} 帳號名稱：{row['name'].iloc[0]} 組別：{row['group'].iloc[0]} 資金：{row['profit'].iloc[0]} 需求: {ticket} 描述:展示帳號入金')
    if row['profit'].iloc[0]<0:
        st.write(f'操作的manager名稱：YM-MY-Admin 帳號：{login} 帳號名稱：{row['name'].iloc[0]} 組別：{row['group'].iloc[0]} 資金：{row['profit'].iloc[0]} 需求: {ticket} 描述:展示帳號出金')