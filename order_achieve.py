import streamlit as st
import pandas as pd
import pymysql
import requests
import json
import datetime

d = st.date_input("Select Archive Date")
st.write("Date:", d)
if st.button("Get File"):
    db=pymysql.connect(host = "live-mt4-reportdb-repl-sg-03.vi-data.net", port = 3306, user = "reader_MY", passwd = "GC+Pb#Fw6?X-", db = "pui7report")
    cursor=db.cursor()
    sql = f"""
    select 'pui7report' as 'Server',t.login,u.`group`,count(t.ticket),u.COUNTRY, sum(t.PROFIT+t.COMMISSION+t.`SWAPS`) as "balance"
    from pui7report.mt4_trades t 
    left join 
    pui7report.mt4_users u 
    on t.login = u.login
    where 1=1
    and u.Currency = 'USC'
    and u.GROUP not regexp '^TES|BK|BR|^T_|TEST'
    and t.close_time <= '{d} 23:59:59' 
    and t.close_time != '1970-01-01 00:00:00' 
    and cmd not in (2,3,4,5,6,7)
    group by t.login
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    data=pd.DataFrame(list(data),columns=['Server','Login','group','PreCount','COUNTRY','balance'])
    data=data.loc[:, ['Login','PreCount']]
    data['Archive Date']=d.strftime('%Y-%m-%d')
    data=data.loc[:,['Login','Archive Date','PreCount']]
    st.write("PU7")
    st.dataframe(data)
    data.to_csv(f"{d}_archive_order_PU7.csv", index=False)


    db1=pymysql.connect(host = "live-mt4-reportdb-repl-sg-03.vi-data.net", port = 3306, user = "reader_MY", passwd = "GC+Pb#Fw6?X-", db = "pui6report")
    cursor1=db1.cursor()
    sql1 = f"""
    select 'pui6report' as 'Server',t.login,u.`group`,count(t.ticket),u.COUNTRY, sum(t.PROFIT+t.COMMISSION+t.`SWAPS`) as "balance"
    from pui6report.mt4_trades t 
    left join 
    pui6report.mt4_users u 
    on t.login = u.login
    where 1=1
    and u.Currency = 'USC'
    and u.GROUP not regexp '^TES|BK|BR|^T_|TEST'
    and t.close_time <= '{d} 23:59:59' 
    and t.close_time != '1970-01-01 00:00:00' 
    and cmd not in (2,3,4,5,6,7)
    group by t.login
    """
    cursor1.execute(sql1)
    data1 = cursor1.fetchall()
    data1=pd.DataFrame(list(data1),columns=['Server','Login','group','PreCount','COUNTRY','balance'])
    data1=data1.loc[:, ['Login','PreCount']]
    data1['Archive Date']=d.strftime('%Y-%m-%d')
    data1=data1.loc[:,['Login','Archive Date','PreCount']]
    st.write("PU6")
    st.dataframe(data1)
    data1.to_csv(f"{d}_archive_order_PU6.csv", index=False)

