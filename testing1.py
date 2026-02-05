import pandas as pd
import streamlit as st
import MT5Manager
import time
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

uploaded_file = st.file_uploader("Upload XLSX File", key="excel")

if uploaded_file is not None:
    sheet2_df = pd.read_excel(uploaded_file)
    st.dataframe(sheet2_df)
    output_login_list=[]
    output_status_list=[]
    manager = MT5Manager.ManagerAPI()
    # if manager.Connect(st.secrets["accounts"]["ip"], int(st.secrets["accounts"]["login"]), st.secrets["accounts"]["password"], 
    #                     MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL, 12000):
    if manager.Connect(st.secrets["test_accounts"]["ip"], int(st.secrets["test_accounts"]["login"]), st.secrets["test_accounts"]["password"], 
                    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL, 120000):
        
        user = MT5Manager.MTUser(manager)
        
        
    else:
        # failed to connect to the server
        st.warning(f"Failed to connect to server: {MT5Manager.LastError()}")