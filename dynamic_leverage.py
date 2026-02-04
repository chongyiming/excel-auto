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
import requests
import json
import ssl
from requests.adapters import HTTPAdapter
import re
import time

class TLS12Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        ctx = ssl.create_default_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        pool_kwargs["ssl_context"] = ctx
        return super().init_poolmanager(connections, maxsize, block, **pool_kwargs)

session = requests.Session()
session.mount("https://", TLS12Adapter())
st.title("Remove white cell colour news before auto set")
uploaded_file = st.file_uploader("Upload dynamic leverage",key="compair")
rows=[]
if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file)
    
    # Get all sheet names
    sheet_names = xls.sheet_names
    selected_sheet = st.selectbox("Select a sheet to view:", sheet_names)
    serverOption = st.selectbox(
    "Select Server",
    ("MT4","MT5"),
    )
    
    option = st.selectbox(
    "Select Time",
    ("Time (GMT+2)","Time (GMT+3)"),
    )

    input_token = st.text_area("Paste token here")

    
    f1_dataframe = pd.read_excel(uploaded_file,sheet_name=selected_sheet)
    # f1_dataframe=f1_dataframe.iloc[:, 5:9]
    # f1_dataframe.rename(columns={f1_dataframe.columns[2]: 'Day'}, inplace=True)
    # st.dataframe(f1_dataframe)
    f1_dataframe=f1_dataframe.iloc[:, 0:4]
        
    f1_dataframe['Time_DT'] = f1_dataframe[option].apply(
    lambda t: datetime.combine(datetime.today(), t)
    )

    f1_dataframe['-15 分钟'] = f1_dataframe['Time_DT'] - pd.Timedelta(minutes=15)
    f1_dataframe['+5 分钟'] = f1_dataframe['Time_DT'] + pd.Timedelta(minutes=5)

    f1_dataframe['-15 分钟'] = f1_dataframe['-15 分钟'].dt.time
    f1_dataframe['+5 分钟'] = f1_dataframe['+5 分钟'].dt.time

    f1_dataframe.drop(columns=['Time_DT'], inplace=True)

    f1_dataframe['Day'] = f1_dataframe['Date'].dt.day_name().str[:3].str.upper()

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
    if serverOption=="MT4":
        config_list=["MT4_UM1.xlsx","MT4_UM2.xlsx"]
        url="https://prod03-actions-b001.api.yoonit.net/api/DynamicMargin/EditSessions"
        Oil_IndicesLeverage="[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"0.5\"}]"
    elif serverOption=="MT5":
        config_list=["MT5_UM1.xlsx","MT5_UM2.xlsx"]
        url="https://prod03-actions-b001.api.yoonit.net/api/DynamicMargin/EditSessions"
        Oil_IndicesLeverage="[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"0.005\"}]"
    Forex=False
    Gold=False
    Indices=False
    Oil=False
    for i in f1_dataframe["Profile"]:
        print(i)
        if "Forex" in i:
            Forex=True
        if "Gold" in i:
            Gold=True
        if "Indices" in i:
            Indices=True
        if "Oil" in i:
            Oil=True
    st.write("Forex: ",Forex,"\n","Gold: ",Gold,"\n","Indices: ",Indices,"\n","Oil: ",Oil)


    headers = {
        "Content-Type": "application/json",
        "Token": input_token
    }

    DAY_MAP = {
                "MON": 1,
                "TUE": 2,
                "WED": 3,
                "THU": 4,
                "FRI": 5,
                "SAT": 6,
                "SUN": 0
            }
    Forex=True
    Gold=True
    Indices=True
    Oil=True
    if input_token:
        if Forex==True:
            for i in config_list:
                for j in ["Forex1",'Forex2']:
                    config_file = pd.read_excel(i,sheet_name=j)
                    
                    config_row = config_file.iloc[0]
                    

                    psessions = []

                    forex_rows = f1_dataframe[
                        f1_dataframe["Profile"].str.contains("Forex", na=False)
                    ]
                    
                    psessions.append({ "ServerID": '0', "SessionID": None, "ProfileID": int(config_row["ProfileID"]), "FromDay": int(config_row["FromDay"]), "ToDay": int(config_row["ToDay"]), "FromHour": int(config_row["FromHour"]), "ToHour": int(config_row["ToHour"]), "FromMinute": int(config_row["FromMinute"]), "ToMinute": int(config_row["ToMinute"]), "Tiers": str(config_row["Tiers"]), "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]", "SessionTitle": str(config_row["SessionTitle"]), "TiersDisplay": str(config_row["TiersDisplay"]), } )
                    for _, row in forex_rows.iterrows():
                        from_time = row["-15 分钟"]
                        to_time = row["+5 分钟"]
                        day_code = DAY_MAP[row["Day"]]

                        psessions.append({
                            "ServerID": int(config_row["ServerID"]),
                            "SessionID": None,
                            "ProfileID": int(config_row["ProfileID"]),
                            "FromDay": day_code,
                            "ToDay": day_code,
                            "FromHour": from_time.hour,
                            "ToHour": to_time.hour,
                            "FromMinute": from_time.minute,
                            "ToMinute": to_time.minute,
                            "Tiers": str(config_row["Tiers"]),
                            "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]",
                            "SessionTitle": str(row["New_Event"]),
                            "TiersDisplay": str(config_row["TiersDisplay"]),
                        })
                    payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }
                    print(payload)

                    response = session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )


                    try:
                        st.write("Status Code:", response.status_code,j)
                        st.write("Response JSON:", response.json())
                    except ValueError:
                        st.write("Response Text:", response.text)
                    time.sleep(1)
        if Gold==True:
            for i in config_list:

                for j in ["Gold1"]:
                    config_file = pd.read_excel(i,sheet_name=j)
                    

                    

                    config_row = config_file.iloc[0]
                    
                    psessions = []

                    forex_rows = f1_dataframe[
                        f1_dataframe["Profile"].str.contains("Gold", na=False)
                    ]
                    
                    psessions.append({ "ServerID": '0', "SessionID": None, "ProfileID": int(config_row["ProfileID"]), "FromDay": int(config_row["FromDay"]), "ToDay": int(config_row["ToDay"]), "FromHour": int(config_row["FromHour"]), "ToHour": int(config_row["ToHour"]), "FromMinute": int(config_row["FromMinute"]), "ToMinute": int(config_row["ToMinute"]), "Tiers": str(config_row["Tiers"]), "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]", "SessionTitle": str(config_row["SessionTitle"]), "TiersDisplay": str(config_row["TiersDisplay"]), } )
                    for _, row in forex_rows.iterrows():
                        from_time = row["-15 分钟"]
                        to_time = row["+5 分钟"]
                        day_code = DAY_MAP[row["Day"]]

                        psessions.append({
                            "ServerID": int(config_row["ServerID"]),
                            "SessionID": None,
                            "ProfileID": int(config_row["ProfileID"]),
                            "FromDay": day_code,
                            "ToDay": day_code,
                            "FromHour": from_time.hour,
                            "ToHour": to_time.hour,
                            "FromMinute": from_time.minute,
                            "ToMinute": to_time.minute,
                            "Tiers": str(config_row["Tiers"]),
                            "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]",
                            "SessionTitle": str(row["New_Event"]),
                            "TiersDisplay": str(config_row["TiersDisplay"]),
                        })
                    payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }
                    print(payload)

                    response = session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )


                    try:
                        st.write("Status Code:", response.status_code,j)
                        st.write("Response JSON:", response.json())
                    except ValueError:
                        st.write("Response Text:", response.text)
                    time.sleep(1)

        if Oil==True:
            for i in config_list:

                for j in ["Oil1"]:
                    config_file = pd.read_excel(i,sheet_name=j)
                    

                    

                    config_row = config_file.iloc[0]
                    
                    psessions = []

                    forex_rows = f1_dataframe[
                        f1_dataframe["Profile"].str.contains("Oil", na=False)
                    ]
                    
                    psessions.append({ "ServerID": '0', "SessionID": None, "ProfileID": int(config_row["ProfileID"]), "FromDay": int(config_row["FromDay"]), "ToDay": int(config_row["ToDay"]), "FromHour": int(config_row["FromHour"]), "ToHour": int(config_row["ToHour"]), "FromMinute": int(config_row["FromMinute"]), "ToMinute": int(config_row["ToMinute"]), "Tiers": str(config_row["Tiers"]), "TiersJson": Oil_IndicesLeverage, "SessionTitle": str(config_row["SessionTitle"]), "TiersDisplay": str(config_row["TiersDisplay"]), } )
                    for _, row in forex_rows.iterrows():
                        from_time = row["-15 分钟"]
                        to_time = row["+5 分钟"]
                        day_code = DAY_MAP[row["Day"]]

                        psessions.append({
                            "ServerID": int(config_row["ServerID"]),
                            "SessionID": None,
                            "ProfileID": int(config_row["ProfileID"]),
                            "FromDay": day_code,
                            "ToDay": day_code,
                            "FromHour": from_time.hour,
                            "ToHour": to_time.hour,
                            "FromMinute": from_time.minute,
                            "ToMinute": to_time.minute,
                            "Tiers": str(config_row["Tiers"]),
                            "TiersJson": Oil_IndicesLeverage,
                            "SessionTitle": str(row["New_Event"]),
                            "TiersDisplay": str(config_row["TiersDisplay"]),
                        })
                    payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }
                    print(payload)

                    response = session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )


                    try:
                        st.write("Status Code:", response.status_code,j)
                        st.write("Response JSON:", response.json())
                    except ValueError:
                        st.write("Response Text:", response.text)
                    time.sleep(1)

        if Indices==True:
            for i in config_list:

                for j in ["Indices1","Indices2","Indices3","Indices4","Indices5","Indices6","Indices7"]:
                    config_file = pd.read_excel(i,sheet_name=j)
                    

                    

                    config_row = config_file.iloc[0]
                    
                    psessions = []

                    forex_rows = f1_dataframe[
                        f1_dataframe["Profile"].str.contains("Indices", na=False)
                    ]
                    
                    psessions.append({ "ServerID": '0', "SessionID": None, "ProfileID": int(config_row["ProfileID"]), "FromDay": int(config_row["FromDay"]), "ToDay": int(config_row["ToDay"]), "FromHour": int(config_row["FromHour"]), "ToHour": int(config_row["ToHour"]), "FromMinute": int(config_row["FromMinute"]), "ToMinute": int(config_row["ToMinute"]), "Tiers": str(config_row["Tiers"]), "TiersJson": Oil_IndicesLeverage, "SessionTitle": str(config_row["SessionTitle"]), "TiersDisplay": str(config_row["TiersDisplay"]), } )
                    for _, row in forex_rows.iterrows():
                        from_time = row["-15 分钟"]
                        to_time = row["+5 分钟"]
                        day_code = DAY_MAP[row["Day"]]

                        psessions.append({
                            "ServerID": int(config_row["ServerID"]),
                            "SessionID": None,
                            "ProfileID": int(config_row["ProfileID"]),
                            "FromDay": day_code,
                            "ToDay": day_code,
                            "FromHour": from_time.hour,
                            "ToHour": to_time.hour,
                            "FromMinute": from_time.minute,
                            "ToMinute": to_time.minute,
                            "Tiers": str(config_row["Tiers"]),
                            "TiersJson": Oil_IndicesLeverage,
                            "SessionTitle": str(row["New_Event"]),
                            "TiersDisplay": str(config_row["TiersDisplay"]),
                        })
                    payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }
                    print(payload)

                    response = session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )


                    try:
                        st.write("Status Code:", response.status_code,j)
                        st.write("Response JSON:", response.json())
                    except ValueError:
                        st.write("Response Text:", response.text)
                    time.sleep(1)
