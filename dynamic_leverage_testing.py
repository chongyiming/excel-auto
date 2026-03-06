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
import time

def is_session_covered(news_start_dt, news_end_dt, def_from_day, def_to_day, def_from_h, def_to_h, def_from_m, def_to_m):
    """
    Checks if a news event (datetime) falls completely inside the Default Session window.
    Handles the weekend wrap (e.g., Fri -> Mon).
    """
    # 1. Convert everything to "Minutes from Sunday 00:00" (Sun=0, Mon=1... Sat=6)
    def to_mins(day, h, m):
        return (day * 1440) + (h * 60) + m

    # Get News Day/Time in API format (Sun=0...Sat=6)
    # We use the same get_api_day logic you already have
    news_start_day = get_api_day(news_start_dt)
    news_end_day = get_api_day(news_end_dt)
    
    n_start = to_mins(news_start_day, news_start_dt.hour, news_start_dt.minute)
    n_end = to_mins(news_end_day, news_end_dt.hour, news_end_dt.minute)

    # Get Default Start/End in minutes
    d_start = to_mins(def_from_day, def_from_h, def_from_m)
    d_end = to_mins(def_to_day, def_to_h, def_to_m)

    # 2. Check overlap
    if d_start < d_end:
        # Normal Week (e.g., Mon -> Wed)
        # News is covered if it starts >= Default Start AND ends <= Default End
        return n_start >= d_start and n_end <= d_end
    else:
        # Weekend Wrap (e.g., Fri -> Mon)
        # The session covers [d_start to End_of_Week] AND [0 to d_end]
        
        # Check if news is fully in the "end of week" part (Fri night)
        in_late_week = (n_start >= d_start) and (n_end > n_start) # Simple check
        
        # Check if news is fully in the "start of week" part (Mon morning)
        in_early_week = (n_end <= d_end) and (n_start < n_end)
        
        # Handle case where news might wrap (Sat -> Sun) - unlikely for short news but possible
        # For simplicity, if news is Mon 00:00 (1440) to Mon 00:20 (1460)
        # d_end is Mon 00:30 (1470). 1460 <= 1470. Returns True.
        
        return in_late_week or in_early_week

# --- Helper Function for Merging ---

def merge_intervals(rows):

    """

    Takes a list of dictionaries containing 'Start_Full', 'End_Full', and 'Event'.

    Returns a merged list where overlapping timeframes are combined.

    """

    if not rows:

        return []



    # Sort by start time

    rows.sort(key=lambda x: x['Start_Full'])



    merged = [rows[0]]



    for current in rows[1:]:

        previous = merged[-1]



        # Check for overlap: If current start is before (or equal to) previous end

        if current['Start_Full'] <= previous['End_Full']:

            # Overlap detected!

            # 1. Extend the end time to whichever ends later

            previous['End_Full'] = max(previous['End_Full'], current['End_Full'])

            # 2. Combine the titles so you know which events caused this session

            if current['Event'] not in previous['Event']:

                previous['Event'] += f" / {current['Event']}"

        else:

            # No overlap, add as new session

            merged.append(current)

   

    return merged

# -----------------------------------



class TLS12Adapter(HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):

        ctx = ssl.create_default_context()

        ctx.minimum_version = ssl.TLSVersion.TLSv1_2

        pool_kwargs["ssl_context"] = ctx

        return super().init_poolmanager(connections, maxsize, block, **pool_kwargs)



session = requests.Session()

session.mount("https://", TLS12Adapter())



st.title("Remove white cell colour rows before upload file")

uploaded_file = st.file_uploader("Upload dynamic leverage", key="compair")



rows = []

if uploaded_file is not None:

    xls = pd.ExcelFile(uploaded_file)

   

    sheet_names = xls.sheet_names

    selected_sheet = st.selectbox("Select a sheet to view:", sheet_names)

    serverOption = st.selectbox("Select Server", ("MT4", "MT5"))

   

    option = st.selectbox("Select Time", ("Time (GMT+2)", "Time (GMT+3)"))



    input_token = st.text_area("Paste token here")

   

    f1_dataframe = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

    f1_dataframe = f1_dataframe.iloc[:, 0:4]

       

    # FIX: Use the actual DATE from the row, not datetime.today()

    # This allows bridging Friday to Monday correctly

    f1_dataframe['Time_DT'] = f1_dataframe.apply(

        lambda row: datetime.combine(row['Date'], row[option]), axis=1

    )



    # Calculate full Start and End datetimes

    f1_dataframe['Start_Full'] = f1_dataframe['Time_DT'] - pd.Timedelta(minutes=15)

    f1_dataframe['End_Full'] = f1_dataframe['Time_DT'] + pd.Timedelta(minutes=5)



    # We keep the display columns for the UI, but we use Start_Full/End_Full for logic

    f1_dataframe['-15 分钟'] = f1_dataframe['Start_Full'].dt.time

    f1_dataframe['+5 分钟'] = f1_dataframe['End_Full'].dt.time



    # f1_dataframe.drop(columns=['Time_DT'], inplace=True) # Keep Time_DT for debugging if needed



    f1_dataframe['Day'] = f1_dataframe['Date'].dt.day_name().str[:3].str.upper()



    for idx, row in f1_dataframe.iterrows():

        if "Oil" in row['Event']:

            f1_dataframe.at[idx, 'Profile'] = "Oil"

        elif row['Currency/Country'].strip() == "USD":

            f1_dataframe.at[idx, 'Profile'] = "Forex,Gold,Indices"

        else:

            f1_dataframe.at[idx, 'Profile'] = "Forex"

           

    f1_dataframe["New_Event"] = f1_dataframe["Event"]        

    # Adjust dataframe view for user

    st.dataframe(f1_dataframe)



    if serverOption == "MT4":

        config_list = ["MT4_UM1.xlsx", "MT4_UM2.xlsx"]

        url = "https://prod03-actions-b001.api.yoonit.net/api/DynamicMargin/EditSessions"

        Oil_IndicesLeverage = "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"0.5\"}]"

    elif serverOption == "MT5":

        config_list = ["MT5_UM1.xlsx", "MT5_UM2.xlsx"]

        url = "https://prod03-actions-b001.api.yoonit.net/api/DynamicMargin/EditSessions"

        Oil_IndicesLeverage = "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"0.005\"}]"

   

    Forex = False

    Gold = False

    Indices = False

    Oil = False

   

    for i in f1_dataframe["Profile"]:

        if "Forex" in i: Forex = True

        if "Gold" in i: Gold = True

        if "Indices" in i: Indices = True

        if "Oil" in i: Oil = True

           

    st.write("Forex: ", Forex, "\n", "Gold: ", Gold, "\n", "Indices: ", Indices, "\n", "Oil: ", Oil)



    headers = {

        "Content-Type": "application/json",

        "Token": input_token

    }



    # API uses 0 for Sunday, 1 for Monday...

    # We need to map Python's weekday() (Mon=0, Sun=6) to this custom map if needed

    # Or strict string mapping.

    # Python .weekday(): Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6

    # Your MAP: Mon=1 ... Sun=0.

    DAY_MAP_STR = {

        "MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5, "SAT": 6, "SUN": 0

    }

   

    # Helper to get API day number from datetime object

    def get_api_day(dt_obj):

        # dt_obj.strftime("%a").upper() gives MON, TUE etc.

        day_str = dt_obj.strftime("%a").upper()

        return DAY_MAP_STR.get(day_str, 1)



    if input_token:

        # ================= FOREX =================


        for i in config_list:

            for j in ["Forex1", 'Forex2']:

                config_file = pd.read_excel(i, sheet_name=j)

                config_row = config_file.iloc[0]

                psessions = []



                # 1. Filter Rows

                # 1. Filter News Rows
                forex_rows = f1_dataframe[f1_dataframe["Profile"].str.contains("Forex", na=False)]

                # 2. Collect ALL raw intervals (Defaults + News)
                raw_intervals = []

                # Add News Intervals
                for _, row in forex_rows.iterrows():
                    raw_intervals.append({
                        'Start_Full': row['Start_Full'],
                        'End_Full': row['End_Full'],
                        'Event': str(row["New_Event"])
                    })

                # Add Default Intervals (Converting the day/hour/min to a comparable datetime)
                # Note: We use the first News date as a reference to create the "Default" datetime
                ref_date = forex_rows.iloc[0]['Date'] if not forex_rows.empty else datetime.today()

                for index, config_row in config_file.iterrows():
                    # Helper to calculate datetime for the default session based on the week's dates
                    d_start = datetime.combine(ref_date, datetime.min.time()) + timedelta(days=(int(config_row["FromDay"]) - get_api_day(ref_date)))
                    d_start = d_start.replace(hour=int(config_row["FromHour"]), minute=int(config_row["FromMinute"]))
                    
                    # Handle the "ToDay" logic
                    d_end = datetime.combine(ref_date, datetime.min.time()) + timedelta(days=(int(config_row["ToDay"]) - get_api_day(ref_date)))
                    d_end = d_end.replace(hour=int(config_row["ToHour"]), minute=int(config_row["ToMinute"]))

                    raw_intervals.append({
                        'Start_Full': d_start,
                        'End_Full': d_end,
                        'Event': str(config_row["SessionTitle"])
                    })

                # 3. Merge EVERYTHING together
                # This will combine General Forex + GDP into ONE interval if they overlap
                merged_intervals = merge_intervals(raw_intervals)

                # 4. Build psessions from the merged results
                psessions = []
                for item in merged_intervals:
                    psessions.append({
                        "ServerID": 0,
                        "SessionID": None,
                        "ProfileID": int(config_row["ProfileID"]),
                        "FromDay": get_api_day(item['Start_Full']),
                        "ToDay": get_api_day(item['End_Full']),
                        "FromHour": item['Start_Full'].hour,
                        "ToHour": item['End_Full'].hour,
                        "FromMinute": item['Start_Full'].minute,
                        "ToMinute": item['End_Full'].minute,
                        "Tiers": str(config_row["Tiers"]),
                        "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]",
                        "SessionTitle": item['Event'],
                        "TiersDisplay": str(config_row["TiersDisplay"]),
                    })



                payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }

                st.write(payload)



                response = session.post(url, headers=headers, json=payload, timeout=30)

                try:

                    st.write(f"Forex ({j}): Status {response.status_code}")

                except:

                    pass

                time.sleep(1)



        # ================= GOLD =================


        for i in config_list:

            for j in ["Gold1"]:

                config_file = pd.read_excel(i, sheet_name=j)

                config_row = config_file.iloc[0]

                psessions = []



                gold_rows = f1_dataframe[f1_dataframe["Profile"].str.contains("Gold", na=False)]

                
                # 2. Collect ALL raw intervals (Defaults + News)
                raw_intervals = []

                # Add News Intervals
                for _, row in gold_rows.iterrows():
                    raw_intervals.append({
                        'Start_Full': row['Start_Full'],
                        'End_Full': row['End_Full'],
                        'Event': str(row["New_Event"])
                    })

                # Add Default Intervals (Converting the day/hour/min to a comparable datetime)
                # Note: We use the first News date as a reference to create the "Default" datetime
                ref_date = gold_rows.iloc[0]['Date'] if not gold_rows.empty else datetime.today()

                for index, config_row in config_file.iterrows():
                    # Helper to calculate datetime for the default session based on the week's dates
                    d_start = datetime.combine(ref_date, datetime.min.time()) + timedelta(days=(int(config_row["FromDay"]) - get_api_day(ref_date)))
                    d_start = d_start.replace(hour=int(config_row["FromHour"]), minute=int(config_row["FromMinute"]))
                    
                    # Handle the "ToDay" logic
                    d_end = datetime.combine(ref_date, datetime.min.time()) + timedelta(days=(int(config_row["ToDay"]) - get_api_day(ref_date)))
                    d_end = d_end.replace(hour=int(config_row["ToHour"]), minute=int(config_row["ToMinute"]))

                    raw_intervals.append({
                        'Start_Full': d_start,
                        'End_Full': d_end,
                        'Event': str(config_row["SessionTitle"])
                    })

                # 3. Merge EVERYTHING together
                # This will combine General Forex + GDP into ONE interval if they overlap
                merged_intervals = merge_intervals(raw_intervals)

                # 4. Build psessions from the merged results
                psessions = []
                for item in merged_intervals:
                    psessions.append({
                        "ServerID": 0,
                        "SessionID": None,
                        "ProfileID": int(config_row["ProfileID"]),
                        "FromDay": get_api_day(item['Start_Full']),
                        "ToDay": get_api_day(item['End_Full']),
                        "FromHour": item['Start_Full'].hour,
                        "ToHour": item['End_Full'].hour,
                        "FromMinute": item['Start_Full'].minute,
                        "ToMinute": item['End_Full'].minute,
                        "Tiers": str(config_row["Tiers"]),
                        "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]",
                        "SessionTitle": item['Event'],
                        "TiersDisplay": str(config_row["TiersDisplay"]),
                    })



                payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }

                st.write(payload)



                response = session.post(url, headers=headers, json=payload, timeout=30)

                try:

                    st.write(f"Gold ({j}): Status {response.status_code}")

                except:

                    pass

                time.sleep(1)



        # # ================= OIL =================


        for i in config_list:

            for j in ["Oil1"]:

                config_file = pd.read_excel(i, sheet_name=j)

                config_row = config_file.iloc[0]

                psessions = []



                oil_rows = f1_dataframe[f1_dataframe["Profile"].str.contains("Oil", na=False)]

                

                # Merge Logic

                raw_intervals = []

                for _, row in oil_rows.iterrows():

                    raw_intervals.append({

                        'Start_Full': row['Start_Full'],

                        'End_Full': row['End_Full'],

                        'Event': str(row["New_Event"])

                    })

                                    # 3. Merge Overlapping Sessions
                merged_intervals = merge_intervals(raw_intervals)

                for index, config_row in config_file.iterrows():
                    # 1. Extract values for the current row
                    d_from_day = int(config_row["FromDay"])
                    d_to_day   = int(config_row["ToDay"])
                    d_from_h   = int(config_row["FromHour"])
                    d_to_h     = int(config_row["ToHour"])
                    d_from_m   = int(config_row["FromMinute"])
                    d_to_m     = int(config_row["ToMinute"])

                    # 2. Append the dictionary for the current row to your list
                    psessions.append({ 
                        "ServerID": 0, 
                        "SessionID": None, 
                        "ProfileID": int(config_row["ProfileID"]), 
                        "FromDay": d_from_day, 
                        "ToDay": d_to_day, 
                        "FromHour": d_from_h, 
                        "ToHour": d_to_h, 
                        "FromMinute": d_from_m, 
                        "ToMinute": d_to_m, 
                        "Tiers": str(config_row["Tiers"]), 
                        "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]", 
                        "SessionTitle": str(config_row["SessionTitle"]), 
                        "TiersDisplay": str(config_row["TiersDisplay"]), 
                    })

                # 4. Add News Sessions (ONLY if not covered by Default)
                for item in merged_intervals:
                    
                    # CHECK: Is this news event completely inside the default session?
                    covered = is_session_covered(
                        item['Start_Full'], item['End_Full'],
                        d_from_day, d_to_day, d_from_h, d_to_h, d_from_m, d_to_m
                    )
                    
                    if covered:
                        # Skip adding this session because the Default Session covers it
                        # You can optionally print a log here for debugging
                        # st.write(f"Skipping {item['Event']} - Covered by Default Session")
                        continue 

                    # If NOT covered, add it
                    psessions.append({
                        "ServerID": 0,
                        "SessionID": None,
                        "ProfileID": int(config_row["ProfileID"]),
                        "FromDay": get_api_day(item['Start_Full']),
                        "ToDay": get_api_day(item['End_Full']),
                        "FromHour": item['Start_Full'].hour,
                        "ToHour": item['End_Full'].hour,
                        "FromMinute": item['Start_Full'].minute,
                        "ToMinute": item['End_Full'].minute,
                        "Tiers": str(config_row["Tiers"]),
                        "TiersJson": Oil_IndicesLeverage,
                        "SessionTitle": item['Event'],
                        "TiersDisplay": str(config_row["TiersDisplay"]),
                    })




                payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }

                st.write(payload)

                response = session.post(url, headers=headers, json=payload, timeout=30)

                try:

                    st.write(f"Oil ({j}): Status {response.status_code}")

                except:

                    pass

                time.sleep(1)



        # # ================= INDICES =================


        for i in config_list:

            for j in ["Indices1","Indices2","Indices3","Indices4","Indices5","Indices6","Indices7"]:

                config_file = pd.read_excel(i, sheet_name=j)

                config_row = config_file.iloc[0]

                psessions = []



                indices_rows = f1_dataframe[f1_dataframe["Profile"].str.contains("Indices", na=False)]
                raw_intervals = []

                # Add News Intervals
                for _, row in indices_rows.iterrows():
                    raw_intervals.append({
                        'Start_Full': row['Start_Full'],
                        'End_Full': row['End_Full'],
                        'Event': str(row["New_Event"])
                    })

                # Add Default Intervals (Converting the day/hour/min to a comparable datetime)
                # Note: We use the first News date as a reference to create the "Default" datetime
                ref_date = indices_rows.iloc[0]['Date'] if not indices_rows.empty else datetime.today()

                for index, config_row in config_file.iterrows():
                    # Helper to calculate datetime for the default session based on the week's dates
                    d_start = datetime.combine(ref_date, datetime.min.time()) + timedelta(days=(int(config_row["FromDay"]) - get_api_day(ref_date)))
                    d_start = d_start.replace(hour=int(config_row["FromHour"]), minute=int(config_row["FromMinute"]))
                    
                    # Handle the "ToDay" logic
                    d_end = datetime.combine(ref_date, datetime.min.time()) + timedelta(days=(int(config_row["ToDay"]) - get_api_day(ref_date)))
                    d_end = d_end.replace(hour=int(config_row["ToHour"]), minute=int(config_row["ToMinute"]))

                    raw_intervals.append({
                        'Start_Full': d_start,
                        'End_Full': d_end,
                        'Event': str(config_row["SessionTitle"])
                    })

                # 3. Merge EVERYTHING together
                # This will combine General Forex + GDP into ONE interval if they overlap
                merged_intervals = merge_intervals(raw_intervals)

                # 4. Build psessions from the merged results
                psessions = []
                for item in merged_intervals:
                    psessions.append({
                        "ServerID": 0,
                        "SessionID": None,
                        "ProfileID": int(config_row["ProfileID"]),
                        "FromDay": get_api_day(item['Start_Full']),
                        "ToDay": get_api_day(item['End_Full']),
                        "FromHour": item['Start_Full'].hour,
                        "ToHour": item['End_Full'].hour,
                        "FromMinute": item['Start_Full'].minute,
                        "ToMinute": item['End_Full'].minute,
                        "Tiers": str(config_row["Tiers"]),
                        "TiersJson": "[{\"Level\":\"T1\",\"Trenches\":\"0\",\"Percentage\":\"200\"}]",
                        "SessionTitle": item['Event'],
                        "TiersDisplay": str(config_row["TiersDisplay"]),
                    })


                payload = { "CompanyName": str(config_row["CompanyName"]), "AUID": str(config_row["AUID"]), "ServerID": int(config_row["ServerID"]), "ServerName": str(config_row["ServerName"]), "ServerType": str(config_row["ServerType"]), "CompanyID": str(config_row["CompanyID"]), "BUID": "00000000-0000-0000-0000-000000000000", "ClientName": str(config_row["ClientName"]), "ProfileName": str(config_row["ProfileName"]), "UserName": str(config_row["UserName"]), "ObjData": { "ProfileID": int(config_row["ProfileID"]), "ProfileIsOverrideTiers": False, "PSessions": psessions, "ProfileIDs": "", "PDSessions": [], "ProfileSessionActivator": False, "SessionTypeID": 1 } }

                st.write(payload)

                response = session.post(url, headers=headers, json=payload, timeout=30)

                try:

                    st.write(f"Indices ({j}): Status {response.status_code}")

                except:

                    pass

                time.sleep(1)