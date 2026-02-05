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

uploaded_file = st.file_uploader("Upload CSV File", key="excel")

if uploaded_file is not None:
    sheet2_df = pd.read_csv(uploaded_file, sep=",")
    st.dataframe(sheet2_df)
    output_login_list=[]
    output_status_list=[]
    manager = MT5Manager.ManagerAPI()
    if manager.Connect(st.secrets["accounts"]["ip"], int(st.secrets["accounts"]["login"]), st.secrets["accounts"]["password"], 
                        MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL, 12000):

        
        user = MT5Manager.MTUser(manager)
        
        for index, row in sheet2_df.iterrows():
            if row['SERVER_NAME'] == 'MT5 Live 1':
                login_id = int(row['LOGIN'])
                
                user = manager.UserRequest(login_id)
                if user==False:
                    st.warning(f"Login {login_id} not found")
                    output_login_list.append(login_id)
                    output_status_list.append("User Not Found")
                    output_data=pd.DataFrame({"Login": output_login_list, "Status": output_status_list})
                    # output_data.to_excel('output.xlsx', index=False)
                    time.sleep(1)
                    continue 
                
                positions = manager.PositionGetByLogins([user.Login])
                st.write(f"Found user {user.Login}: {len(positions)} Positions")
                if len(positions)==0:
                    user.Leverage = 500
                    if not manager.UserUpdate(user):
                        output_login_list.append(user.Login)
                        output_status_list.append("Error")
                    else:
                        output_login_list.append(user.Login)
                        output_status_list.append("Leverage changed")

                else:
                    output_login_list.append(user.Login)
                    output_status_list.append("Position exist")
                output_data=pd.DataFrame({"Login": output_login_list, "Status": output_status_list})
                time.sleep(1)

        manager.Disconnect()
        excel_data = to_excel(output_data)
        st.download_button(
        label="📥 Download Results as Excel",
        data=excel_data,
        file_name="leverage_change_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    else:
        # failed to connect to the server
        st.warning(f"Failed to connect to server: {MT5Manager.LastError()}")