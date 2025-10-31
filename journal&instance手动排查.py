import pandas as pd
import streamlit as st
from io import StringIO
import pymysql
option1 = st.selectbox(
    "Select Type",
    ("Journal","Instance"),
)
server_option = st.selectbox(
    "Select Server",
    ("ST1","ST2","ST4","UM","UM2"),
)

if server_option=="ST2":
    server="startrader2report"
elif server_option=="ST4":
    server="startrader4report"
elif server_option=="ST1":
    server="ivreport"
elif server_option=="UM":
    server="oplreport"

uploaded_file = st.file_uploader("Upload Excel File", key="excel")

if uploaded_file:
    uploaded_file=pd.read_excel(uploaded_file,header=None)
    if option1=="Journal":
        filtered_df = uploaded_file[uploaded_file[2].astype(str).str.contains("modify", case=False, na=False)]
        split_df = filtered_df[2].astype(str).str.split(":", expand=True)
        count_series = split_df[0].value_counts().reset_index()
        count_series.columns = ["Value", "Count"]
        st.subheader("Modified")
        st.dataframe(count_series)

        filtered_df1 = uploaded_file[uploaded_file[2].astype(str).str.contains("no money", case=False, na=False)]
        split_df1 = filtered_df1[2].astype(str).str.split(":", expand=True)
        count_series1 = split_df1[0].value_counts().reset_index()
        count_series1.columns = ["Value", "Count"]
        st.subheader("No Money")
        st.dataframe(count_series1)

        filtered_df2 = uploaded_file[uploaded_file[2].astype(str).str.contains("invalid password", case=False, na=False)]
        split_df2 = filtered_df2[2].astype(str).str.split(":", expand=True)
        count_series2 = split_df2[0].value_counts().reset_index()
        count_series2.columns = ["Value", "Count"]
        st.subheader("Invalid Password")
        st.dataframe(count_series2)
    if option1=="Instance":
        filtered_df = uploaded_file[uploaded_file[3].astype(str).str.contains("modify", case=False, na=False)]
        split_df = filtered_df[3].astype(str).str.split(":", expand=True)
        count_series = split_df[0].value_counts().reset_index()
        count_series.columns = ["Value", "Count"]
        st.subheader("Modified")
        st.dataframe(count_series)

        filtered_df1 = uploaded_file[uploaded_file[3].astype(str).str.contains("no money", case=False, na=False)]
        split_df1 = filtered_df1[3].astype(str).str.split(":", expand=True)
        count_series1 = split_df1[0].value_counts().reset_index()
        count_series1.columns = ["Value", "Count"]
        st.subheader("No Money")
        st.dataframe(count_series1)

        filtered_df2 = uploaded_file[uploaded_file[3].astype(str).str.contains("invalid password", case=False, na=False)]
        split_df2 = filtered_df2[3].astype(str).str.split(":", expand=True)
        count_series2 = split_df2[0].value_counts().reset_index()
        count_series2.columns = ["Value", "Count"]
        st.subheader("Invalid Password")
        st.dataframe(count_series2)

    number = st.number_input("Filter count more than:")
    if number:
        filtered_count_series = count_series[count_series["Count"] > number]
        filtered_count_series1 = count_series1[count_series1["Count"] > number]
        filtered_count_series2 = count_series2[count_series2["Count"] > number]
        if server_option == "ST2" or server_option == "ST4" or server_option == "UM":
            db=pymysql.connect(host = "live-mt4-reportdb-repl-sg-03.vi-data.net", port = 3306, user = "reader_MY", passwd = "GC+Pb#Fw6?X-", db = server)
        elif server_option == "ST1":
            db=pymysql.connect(host = "live-mt4-reportdb-repl-sg-02.vi-data.net", port = 3306, user = "reader_MY", passwd = "GC+Pb#Fw6?X-", db = server)

        cursor=db.cursor()
        
        if len(filtered_count_series)>0:
            result = ",".join(f"{i}" for i in filtered_count_series["Value"])
            sql = f"""
            SELECT `login`,`name`, `group`, `balance`
            FROM mt4_users
            WHERE login IN ({result})
            """
            cursor.execute(sql)
            data = cursor.fetchall()
            row=pd.DataFrame(list(data),columns=['login','name','group','balance'])
            st.subheader("Modified Order Details")
            st.dataframe(row)

        if len(filtered_count_series1)>0:

            result1 = ",".join(f"{i}" for i in filtered_count_series1["Value"])
            sql1 = f"""
            SELECT `login`,`name`, `group`, `balance`
            FROM mt4_users
            WHERE login IN ({result1})
            """
            cursor.execute(sql1)
            data1 = cursor.fetchall()
            row1=pd.DataFrame(list(data1),columns=['login','name','group','balance'])
            st.subheader("Modified Order Details")
            st.dataframe(row)

        if len(filtered_count_series2)>0:

            result2 = ",".join(f"{i}" for i in filtered_count_series2["Value"])
            sql2 = f"""
            SELECT `login`,`name`, `group`, `balance`
            FROM mt4_users
            WHERE login IN ({result2})
            """
            cursor.execute(sql2)
            data2 = cursor.fetchall()
            row2=pd.DataFrame(list(data2),columns=['login','name','group','balance'])
            st.subheader("Invalid Password Details")
            st.dataframe(row2)