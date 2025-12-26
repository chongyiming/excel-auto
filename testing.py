import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
import csv
import re
import os, glob
from typing import List, Tuple, Dict, Set, Optional
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta

uploaded_file = st.file_uploader("Upload阶梯式杠杆Symbol筛选模板",key="compair")
rows=[]
if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file)
    
    # Get all sheet names
    sheet_names = xls.sheet_names
    selected_sheet = st.selectbox("Select a sheet to view:", sheet_names)

    option = st.selectbox(
    "Select Time",
    ("Time (GMT+2)","Time (GMT+3)"),
    )
    f1_dataframe = pd.read_excel(uploaded_file,sheet_name=selected_sheet)
    # f1_dataframe=f1_dataframe.iloc[:, 5:9]
    # f1_dataframe.rename(columns={f1_dataframe.columns[2]: 'Day'}, inplace=True)
    # st.dataframe(f1_dataframe)
    f1_dataframe=f1_dataframe.iloc[:, 0:4]
        
    f1_dataframe['Time_DT'] = f1_dataframe[option].apply(
    lambda t: datetime.combine(datetime.today(), t)
    )

    # Now perform the timedelta operations
    f1_dataframe['-15 分钟'] = f1_dataframe['Time_DT'] - pd.Timedelta(minutes=15)
    f1_dataframe['+5 分钟'] = f1_dataframe['Time_DT'] + pd.Timedelta(minutes=5)

    # # (Optional) If you only want the time part back:
    f1_dataframe['-15 分钟'] = f1_dataframe['-15 分钟'].dt.time
    f1_dataframe['+5 分钟'] = f1_dataframe['+5 分钟'].dt.time

    # (Optional) Drop the temporary datetime column
    f1_dataframe.drop(columns=['Time_DT'], inplace=True)

    f1_dataframe['Day'] = f1_dataframe['Date'].dt.day_name().str[:3].str.upper()
    # f1_dataframe.rename(columns={f1_dataframe.columns[2]: 'Day'}, inplace=True)

    for idx, row in f1_dataframe.iterrows():
        if "Oil" in row['Event']:
            f1_dataframe.at[idx, 'Profile'] = "Oil"
        elif row['Currency/Country'].strip() == "USD":
            f1_dataframe.at[idx, 'Profile'] = "Forex,Gold,Indices"
        else:
            f1_dataframe.at[idx, 'Profile'] = "Forex"
    f1_dataframe["New_Event"]=f1_dataframe["Event"]        
    f1_dataframe=f1_dataframe.iloc[:, 4:10]
    st.dataframe(f1_dataframe)

    # for i in f1_dataframe["Profile"]:
    #     if "Forex" in i:
    #         print("yes")
    config_list=["MT4_UM1.xlsx"]
    for i in f1_dataframe["Profile"]:
        if i == "Forex":
            config_file = pd.read_excel(config_list[0],sheet_name="Forex1")
            print(config_file)


