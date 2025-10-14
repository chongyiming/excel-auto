import streamlit as st
import pandas as pd
from io import StringIO
import ast
from pymongo import MongoClient
import pymongo
import clipboard
import pyperclip as clipboard
from st_copy import copy_button


import streamlit as st
from streamlit_gsheets import GSheetsConnection

def clean_cell(cell):
    """Convert string-list to single value if needed."""
    if isinstance(cell, str):
        try:
            val = ast.literal_eval(cell)
            if isinstance(val, list) and len(val) == 1:
                return val[0]
            else:
                return val
        except:
            return cell
    else:
        return cell
def on_copy_click(text):
    clipboard.copy(text)
    # st.success('Text copied successfully!')
# mongo_uri = "mongodb+srv://yimingchonghytech:Amaci123456789012!@cluster0.fwtqwlo.mongodb.net/"
# client = MongoClient(mongo_uri)

# db = client.test
# collection = db.datas


# @st.cache_resource
# def init_connection():
#     return pymongo.MongoClient(**st.secrets["mongo"])


# client = init_connection()
# db = client.test
st.cache_data.clear()

st.title("排查")

st.write("1) Select server")

option = st.selectbox(
    "Select server",
    ("UM","ST","PU"),
)



if option=="UM":
    st.write("2) Paste Per seconds modified here:")

    col1, col2 = st.columns(2)

    with col1:
        pasted_text = st.text_area("UM")

    with col2:
        um2pasted_text = st.text_area("UM2")



    if pasted_text:
        try:
            # Read pasted text as tab-separated values with no header
            df = pd.read_csv(StringIO(pasted_text), sep="\t", header=None)

            # Drop the first 5 rows (indexes 0-4)
            df = df.drop(index=[0, 1, 2, 3, 4])

            # Create dictionary with keys 0-3 for grouping rows in fours
            result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(df)):
                key = i % 4
                row_values = df.iloc[i]
                result_dict[key].append(row_values)

            # Convert to DataFrame
            result_df = pd.DataFrame(result_dict)

            # Overwrite first column's all values with "UM"
            result_df.iloc[:, 0] = "UM"

            # Clean columns 1, 2, 3 to unpack any stringified lists
            for col in result_df.columns[1:]:
                result_df[col] = result_df[col].apply(clean_cell)

            st.success(f'UM Count: {len(result_df)}')
            st.dataframe(result_df.iloc[:, [0, 1]])
            



        except Exception as e:
            st.error(f"Error parsing table: {e}")
    
    if um2pasted_text:
        try:
            # Read pasted text as tab-separated values with no header
            um2df = pd.read_csv(StringIO(um2pasted_text), sep="\t", header=None)

            # Drop the first 5 rows (indexes 0-4)
            um2df = um2df.drop(index=[0, 1, 2, 3, 4])

            # Create dictionary with keys 0-3 for grouping rows in fours
            um2_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(um2df)):
                key = i % 4
                row_values = um2df.iloc[i]
                um2_result_dict[key].append(row_values)

            # Convert to DataFrame
            um2_result_df = pd.DataFrame(um2_result_dict)

            # Overwrite first column's all values with "UM"
            um2_result_df.iloc[:, 0] = "UM2"

            # Clean columns 1, 2, 3 to unpack any stringified lists
            for col in um2_result_df.columns[1:]:
                um2_result_df[col] = um2_result_df[col].apply(clean_cell)
            st.success(f'UM2 Count: {len(um2_result_df)}')

            st.dataframe(um2_result_df.iloc[:, [0, 1]])
        
        except Exception as e:
            st.error(f"Error parsing table: {e}") 
            
                        
    st.write("3) Paste in http://192.168.1.39:8000/find_info and **click 複製表格**")

    st.write("4) Go to [Excel](https://hytechconsult-my.sharepoint.com/:x:/g/personal/yiming_chong_hytechc_com/Edarz2Kh_HBArpQvcfsx86cBRy2E-5hlkLsbjJ8y7a4OtA?e=O8FOqA&nav=MTVfe0JDQTcxMUJFLTBCNkUtNDVFRi1BRTE5LUU2QUIyOTQxQjEyRH0) & paste using **Ctrl+Shift+V**")
    # st.write("5) Paste Advanced account info here:")

    # rtcol1, rtcol2 = st.columns(2)

    # with rtcol1:
    #     risk_tool_pasted_text = st.text_area("UM",key="risk_tool_text_area")

    # with rtcol2:
    #     risk_tool_pasted_text_2 = st.text_area("UM2",key="risk_tool_text_area_2")
    # # risk_tool_pasted_text = st.text_area(" ", height=200, key="risk_tool_text_area")
    # if risk_tool_pasted_text:
    #     try:
    #         risk_tool_df = pd.read_csv(StringIO(risk_tool_pasted_text), sep="\t", header=None)
    #         risk_tool_df = risk_tool_df.drop(index=0)


    #         st.success(f'UM Count: {len(risk_tool_df)}')
    #         risk_tool_df = risk_tool_df.fillna('')
    #         st.dataframe(risk_tool_df.iloc[:, [0,1,2,3,4,6]])

    #     except Exception as e:
    #         st.error(f"Error parsing table: {e}")
    # if risk_tool_pasted_text_2:
    #     try:
    #         risk_tool_df_2 = pd.read_csv(StringIO(risk_tool_pasted_text_2), sep="\t", header=None)
    #         risk_tool_df_2 = risk_tool_df_2.drop(index=0)

    #         st.success(f'UM2 Count: {len(risk_tool_df_2)}')
    #         risk_tool_df_2 = risk_tool_df_2.fillna('')
    #         st.dataframe(risk_tool_df_2.iloc[:, [0,1,2,3,4,6]])

    #     except Exception as e:
    #         st.error(f"Error parsing table: {e}")
    


    st.write("5) Copy and paste this to outlook using **Ctrl+V**")

    # st.markdown("""
    # Hi Team,<br><br>

    # We are writing to inform you that client’s trading behavior causing excessive server load.<br><br>
    # Please inform clients to adjust EA configurations and trading behaviors to avoid causing server overloading.

    # """, unsafe_allow_html=True)

    # if risk_tool_pasted_text:
    #     st.markdown("""<u><strong>UM</strong></u>""",unsafe_allow_html=True)
    #     st.markdown(
    #         risk_tool_df.iloc[:, [0,1,2,3,4,6]].to_html(index=False, header=False),
    #         unsafe_allow_html=True
    #     )


    # if risk_tool_pasted_text_2:
    #     st.markdown("""<u><strong>UM2</strong></u>""",unsafe_allow_html=True)
    #     st.markdown(
    #     risk_tool_df_2.iloc[:, [0,1,2,3,4,6]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )
    # st.markdown("""
    # <br>What would CS Team need to know?<br>
    # Please kindly inform client to adjust EA configuration or trading behavior accordingly and help to assist clients if they need. The threshold value was listed as below if client would like to know. System Admin would also preserve the right to take execution regarding to other abnormal behaviors causing server excessive loading. For instance, consistently login and logout without actual operations/several times of request sending to server within a second/unknown network pumping, etc."<br><br>
    # More than 3 times within a second<br>
    # More than 600 times within 30 minutes.<br>

    # Best Regards,<br>
    # System Admin
    # """, unsafe_allow_html=True)

    email_body = 'Hi Team,\n\nWe are writing to inform you that client’s trading behavior causing excessive server load.\n\nPlease inform clients to adjust EA configurations and trading behaviors to avoid causing server overloading.\n\n\n\nWhat would CS Team need to do?\nPlease kindly inform client to adjust EA configuration or trading behavior accordingly and help to assist clients if they need. The threshold value was listed as below if client would like to know. System Admin would also preserve the right to take execution regarding to other abnormal behaviors causing server excessive loading. For instance, consistently login and logout without actual operations/several times of request sending to server within a second/unknown network pumping, etc."\n\nMore than 3 times within a second\nMore than 600 times within 30 minutes.\n\nBest Regards,\nSystem Admin'

    # st.button("Copy Email Format",on_click=on_copy_click, args=(email_body,))
    # st.text_area("Copy Email", email_body, height=300)
        
    # Show the text
    st.code(email_body, language="text")


elif option=="ST":

    conn = st.connection("gsheets", type=GSheetsConnection)

    with st.form(key="form"):
        submit_button=st.form_submit_button(label="Press this before proceed")
        if submit_button:
            conn.update(worksheet="Sheet1",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="Sheet2",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="Sheet3",data=pd.DataFrame(columns=["Name"]))


    
    usc_string = ""

    st.write("2) Paste Per seconds modified here:")

    col1, col2,col3 = st.columns(3)

    with col1:
        st_pasted_text = st.text_area("ST")

    with col2:
        st2_pasted_text = st.text_area("ST2")

    with col3:
        st4_pasted_text = st.text_area("ST4")



    if st_pasted_text:
        try:
            # Read pasted text as tab-separated values with no header
            st_df = pd.read_csv(StringIO(st_pasted_text), sep="\t", header=None)

            # Drop the first 5 rows (indexes 0-4)
            st_df = st_df.drop(index=[0, 1, 2, 3, 4])

            # Create dictionary with keys 0-3 for grouping rows in fours
            st_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(st_df)):
                key = i % 4
                row_values = st_df.iloc[i]
                st_result_dict[key].append(row_values)

            # Convert to DataFrame
            st_result_df = pd.DataFrame(st_result_dict)

            # Clean columns 1, 2, 3 to unpack any stringified lists
            for col in st_result_df.columns[1:]:
                st_result_df[col] = st_result_df[col].apply(clean_cell)

            st.success(f'ST Count: {len(st_result_df)}')

            
            # conn = st.connection("gsheets", type=GSheetsConnection)

            data = conn.read(worksheet="Sheet1", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = st_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="Sheet1",data=new_data)
            # st.dataframe(st_result_df.iloc[:, 1])



        except Exception as e:
            st.error(f"Error parsing table: {e}")
    if st2_pasted_text:
        try:
            # Read pasted text as tab-separated values with no header
            st2_df = pd.read_csv(StringIO(st2_pasted_text), sep="\t", header=None)

            # Drop the first 5 rows (indexes 0-4)
            st2_df = st2_df.drop(index=[0, 1, 2, 3, 4])

            # Create dictionary with keys 0-3 for grouping rows in fours
            st2_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(st2_df)):
                key = i % 4
                row_values = st2_df.iloc[i]
                st2_result_dict[key].append(row_values)

            # Convert to DataFrame
            st2_result_df = pd.DataFrame(st2_result_dict)

            # Clean columns 1, 2, 3 to unpack any stringified lists
            for col in st2_result_df.columns[1:]:
                st2_result_df[col] = st2_result_df[col].apply(clean_cell)

            st.success(f'ST2 Count: {len(st2_result_df)}')
            # st.dataframe(st2_result_df.iloc[:, 1])
            st.write("Accounts")
            # url = "https://docs.google.com/spreadsheets/d/1ImBMnjPD8xsXnqrejd7W2Y2vtREP6tvwox-XJf3mkXA/edit?usp=sharing"

            # conn = st.connection("gsheets", type=GSheetsConnection)

            data = conn.read(worksheet="Accounts", usecols=list(range(2)))
            st.dataframe(data)
            # account_list = pd.read_csv("account.csv", sep="\t", header=None)
            # account_list = account_list.iloc[1:, :]  # skip header

            # account_list[0] = account_list[0].astype(str).str.strip()
            # account_list[1] = account_list[1].astype(str).str.strip()
            # st2_result_df.iloc[:, 1] = st2_result_df.iloc[:, 1].astype(str).str.strip()

            # for i in st2_result_df.iloc[:, 1]:
            #     for acc_num, label in zip(account_list[0], account_list[1]):
            #         if i == acc_num and label == "USC":
            #             usc_string += i + ","

            # if usc_string:
            #     usc_string = usc_string.rstrip(",")  # Remove trailing comma, if any
            #     usc_accounts = usc_string.split(",")

            
            account_list_ID = data['ID'].astype(str).str.strip()
            account_list_Currency = data['Currency'].astype(str).str.strip()
            st2_result_df.iloc[:, 1] = st2_result_df.iloc[:, 1].astype(str).str.strip()

            ban_list=[]
            for i, j in zip(st2_result_df.iloc[:, 1], st2_result_df.iloc[:, 3]):
                for acc_num, label in zip(account_list_ID, account_list_Currency):
                    if i == acc_num and label == "USC" and int(j)>400:
                        usc_string += i + ","
                        ban_list.append(i)
                        # st.write(st2_result_df[st2_result_df.iloc[:, 1]==acc_num])

            if usc_string:
                usc_string = usc_string.rstrip(",")  # Remove trailing comma, if any
                usc_accounts = usc_string.split(",")

            st2_result_df[0] = st2_result_df[0].apply(lambda x: pd.to_datetime(x.values[0]) if isinstance(x, pd.Series) else pd.to_datetime(x))
            # st.dataframe(st2_result_df)

            filtered_rows = []
            for i, row in st2_result_df.iterrows():
                if row[1] in ban_list:
                    filtered_rows.append(row)

            # Convert list of Series back to DataFrame
            filtered_df = pd.DataFrame(filtered_rows)

            # Display in Streamlit
            st.dataframe(filtered_df)
            data = conn.read(worksheet="Sheet2", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = st2_result_df[1]
            conn.update(worksheet="Sheet2",data=new_data)
            

            # st.write(new_data)



        except Exception as e:
            st.error(f"Error parsing ST2 table: {e}")
    if st4_pasted_text:
        try:
            # Read pasted text as tab-separated values with no header
            st4_df = pd.read_csv(StringIO(st4_pasted_text), sep="\t", header=None)

            # Drop the first 5 rows (indexes 0-4)
            st4_df = st4_df.drop(index=[0, 1, 2, 3, 4])

            # Create dictionary with keys 0-3 for grouping rows in fours
            st4_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(st4_df)):
                key = i % 4
                row_values = st4_df.iloc[i]
                st4_result_dict[key].append(row_values)

            # Convert to DataFrame
            st4_result_df = pd.DataFrame(st4_result_dict)

            # Clean columns 1, 2, 3 to unpack any stringified lists
            for col in st4_result_df.columns[1:]:
                st4_result_df[col] = st4_result_df[col].apply(clean_cell)

            st.success(f'ST4 Count: {len(st4_result_df)}')
            # st.dataframe(st4_result_df.iloc[:, 1])

            # conn = st.connection("gsheets", type=GSheetsConnection)

            data = conn.read(worksheet="Sheet3", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = st4_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="Sheet3",data=new_data)

        except Exception as e:
            st.error(f"Error parsing ST4 table: {e}")

    st.write("3) USC Users (Filter using Total > 400) and can add accounts [here](https://docs.google.com/spreadsheets/d/1R1bndk9Pb8N3oXP_8TB0xmHpigP7OMer4qtOmL58yks/edit?usp=sharing)")
    st.write(usc_string)
    

    st.write("4) Copy and paste this to outlook")

    # st.markdown("""
    # Hi Team,<br><br>

    # We are writing to inform you that client’s trading behavior causing excessive server load.<br>
    # Please inform clients to adjust EA configurations and trading behaviors to avoid causing server overloading.<br><br>

    # <u><strong>ST</strong></u>
    # """, unsafe_allow_html=True)

    # st.markdown(
    # st_result_df.iloc[:, [1]].to_html(index=False, header=False),
    # unsafe_allow_html=True
    # )

    # st.markdown("""
    # <br>

    # <u><strong>ST2</strong></u>
    # """, unsafe_allow_html=True)
    # st.markdown(
    # st2_result_df.iloc[:, [1]].to_html(index=False, header=False),
    # unsafe_allow_html=True
    # )

    # st.markdown("""
    # <br>

    # <u><strong>ST4</strong></u>
    # """, unsafe_allow_html=True)
    # st.markdown(
    # st4_result_df.iloc[:, [1]].to_html(index=False, header=False),
    # unsafe_allow_html=True
    # )
    # st.markdown("""
    # <br>

    # What would CS Team need to do?<br><br><br>

    # Please kindly inform client to adjust EA configuration or trading behavior accordingly and help to assist clients if they need. The threshold value was listed as below if client would like to know. System Admin would also preserve the right to take execution regarding to other abnormal behaviors causing server excessive loading. For instance, consistently login and logout without actual operations/several times of request sending to server within a second/unknown network pumping, etc."<br><br>

    # More than 3 times within a second<br>
    # More than 600 times within 30 minutes.<br><br><br>

    # Best Regards,<br>
    # System Admin
    # """, unsafe_allow_html=True)

    
    email_body = 'Hi Team,\n\nWe are writing to inform you that client’s trading behavior causing excessive server load.\nPlease inform clients to adjust EA configurations and trading behaviors to avoid causing server overloading.\n\n\n\nWhat would CS Team need to do?\n\n\nPlease kindly inform client to adjust EA configuration or trading behavior accordingly and help to assist clients if they need. The threshold value was listed as below if client would like to know. System Admin would also preserve the right to take execution regarding to other abnormal behaviors causing server excessive loading. For instance, consistently login and logout without actual operations/several times of request sending to server within a second/unknown network pumping, etc."\n\nMore than 3 times within a second\nMore than 600 times within 30 minutes.\n\n\nBest Regards,\nSystem Admin'

    # st.button("Copy Email Format",on_click=on_copy_click, args=(email_body,))
    # st.text_area("Copy Email Format", email_body, height=300)


    # st.write("5) Copy and paste table using **Ctrl+V**")

    # st1_string="ST\n"
    # for i in st_result_df[1]:
    #     st1_string+=i+"\n"
    # st.button("Copy ST",on_click=on_copy_click, args=(st1_string[:-1],))

    # st2_string="ST2\n"
    # for i in st2_result_df[1]:
    #     st2_string+=i+"\n"
    # st.button("Copy ST2",on_click=on_copy_click, args=(st2_string[:-1],))


    # st4_string="ST4\n"
    # for i in st4_result_df[1]:
    #     st4_string+=i+"\n"
    # st.button("Copy ST4",on_click=on_copy_click, args=(st4_string[:-1],))
    st_string = ""

    if st_pasted_text:
        st_string += "ST\n"
        for i in st_result_df[1]:
            st_string += i + "\n"

    if st2_pasted_text:
        if st_string:  # Add newline only if something already exists
            st_string += "\n"
        st_string += "ST2\n"
        for i in st2_result_df[1]:
            st_string += i + "\n"

    if st4_pasted_text:
        if st_string:
            st_string += "\n"
        st_string += "ST4\n"
        for i in st4_result_df[1]:
            st_string += i + "\n"

    # st.button("Copy ST Table",on_click=on_copy_click, args=(st_string[:-1],))

    final_email_body = email_body.replace(
    "causing server overloading.\n\n\n\n",
    "causing server overloading.\n\n" + st_string + "\n"
    )

    # st.text_area("Copy ST Table", st_string[:-1], height=300)
    st.code(final_email_body, language="text")



    
            

elif option=="PU":
    conn = st.connection("gsheets", type=GSheetsConnection)

    with st.form(key="form"):
        submit_button=st.form_submit_button(label="Press this before proceed")
        if submit_button:
            conn.update(worksheet="PU1",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="PU2",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="PU3",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="PU4",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="PU5",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="PU6",data=pd.DataFrame(columns=["Name"]))
            conn.update(worksheet="PU7",data=pd.DataFrame(columns=["Name"]))

    st.write("2) Paste Per seconds modified here:")

    pu_col1, pu_col2, pu_col3, pu_col4, pu_col5, pu_col6, pu_col7 = st.columns(7)

    with pu_col1:
        pu_pasted_text = st.text_area("PU")

    with pu_col2:
        pu2_pasted_text = st.text_area("PU2")

    with pu_col3:
        pu3_pasted_text = st.text_area("PU3")

    with pu_col4:
        pu4_pasted_text = st.text_area("PU4")

    with pu_col5:
        pu5_pasted_text = st.text_area("PU5")

    with pu_col6:
        pu6_pasted_text = st.text_area("PU6")

    with pu_col7:
        pu7_pasted_text = st.text_area("PU7")
    

    if pu_pasted_text:
        try:
            pu_df = pd.read_csv(StringIO(pu_pasted_text), sep="\t", header=None)
            pu_df = pu_df.drop(index=[0, 1, 2, 3, 4])

            pu_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(pu_df)):
                key = i % 4
                row_values = pu_df.iloc[i]
                pu_result_dict[key].append(row_values)

            pu_result_df = pd.DataFrame(pu_result_dict)
            for col in pu_result_df.columns[1:]:
                pu_result_df[col] = pu_result_df[col].apply(clean_cell)

            st.success(f'PU Count: {len(pu_result_df)}')
            # st.dataframe(pu_result_df.iloc[:, 1])


            data = conn.read(worksheet="PU1", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = pu_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="PU1",data=new_data)
        except Exception as e:
            st.error(f"Error parsing PU2: {e}")
    if pu2_pasted_text:
        try:
            pu2_df = pd.read_csv(StringIO(pu2_pasted_text), sep="\t", header=None)
            pu2_df = pu2_df.drop(index=[0, 1, 2, 3, 4])

            pu2_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(pu2_df)):
                key = i % 4
                row_values = pu2_df.iloc[i]
                pu2_result_dict[key].append(row_values)

            pu2_result_df = pd.DataFrame(pu2_result_dict)
            for col in pu2_result_df.columns[1:]:
                pu2_result_df[col] = pu2_result_df[col].apply(clean_cell)

            st.success(f'PU2 Count: {len(pu2_result_df)}')

            data = conn.read(worksheet="PU2", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = pu2_result_df[1]
            conn.update(worksheet="PU2",data=new_data)

            # st.write(new_data)

            
            # st.dataframe(pu2_result_df.iloc[:, 1])
        except Exception as e:
            st.error(f"Error parsing PU2: {e}")

    if pu3_pasted_text:
        try:
            pu3_df = pd.read_csv(StringIO(pu3_pasted_text), sep="\t", header=None)
            pu3_df = pu3_df.drop(index=[0, 1, 2, 3, 4])

            pu3_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(pu3_df)):
                key = i % 4
                row_values = pu3_df.iloc[i]
                pu3_result_dict[key].append(row_values)

            pu3_result_df = pd.DataFrame(pu3_result_dict)
            for col in pu3_result_df.columns[1:]:
                pu3_result_df[col] = pu3_result_df[col].apply(clean_cell)

            st.success(f'PU3 Count: {len(pu3_result_df)}')
            # st.dataframe(pu3_result_df.iloc[:, 1])

            data = conn.read(worksheet="PU3", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = pu3_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="PU3",data=new_data)
        except Exception as e:
            st.error(f"Error parsing PU3: {e}")

    # PU4
    if pu4_pasted_text:
        try:
            pu4_df = pd.read_csv(StringIO(pu4_pasted_text), sep="\t", header=None)
            pu4_df = pu4_df.drop(index=[0, 1, 2, 3, 4])

            pu4_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(pu4_df)):
                key = i % 4
                row_values = pu4_df.iloc[i]
                pu4_result_dict[key].append(row_values)

            pu4_result_df = pd.DataFrame(pu4_result_dict)
            for col in pu4_result_df.columns[1:]:
                pu4_result_df[col] = pu4_result_df[col].apply(clean_cell)

            st.success(f'PU4 Count: {len(pu4_result_df)}')
            # st.dataframe(pu4_result_df.iloc[:, 1])

            data = conn.read(worksheet="PU4", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = pu4_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="PU4",data=new_data)
        except Exception as e:
            st.error(f"Error parsing PU4: {e}")

    # PU5
    if pu5_pasted_text:
        try:
            pu5_df = pd.read_csv(StringIO(pu5_pasted_text), sep="\t", header=None)
            pu5_df = pu5_df.drop(index=[0, 1, 2, 3, 4])

            pu5_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(pu5_df)):
                key = i % 4
                row_values = pu5_df.iloc[i]
                pu5_result_dict[key].append(row_values)

            pu5_result_df = pd.DataFrame(pu5_result_dict)
            for col in pu5_result_df.columns[1:]:
                pu5_result_df[col] = pu5_result_df[col].apply(clean_cell)

            st.success(f'PU5 Count: {len(pu5_result_df)}')
            # st.dataframe(pu5_result_df.iloc[:, 1])

            data = conn.read(worksheet="PU5", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = pu5_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="PU5",data=new_data)
        except Exception as e:
            st.error(f"Error parsing PU5: {e}")

    # PU6
    if pu6_pasted_text:
        try:
            pu6_df = pd.read_csv(StringIO(pu6_pasted_text), sep="\t", header=None)
            pu6_df = pu6_df.drop(index=[0, 1, 2, 3, 4])

            pu6_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(pu6_df)):
                key = i % 4
                row_values = pu6_df.iloc[i]
                pu6_result_dict[key].append(row_values)

            pu6_result_df = pd.DataFrame(pu6_result_dict)
            for col in pu6_result_df.columns[1:]:
                pu6_result_df[col] = pu6_result_df[col].apply(clean_cell)

            st.success(f'PU6 Count: {len(pu6_result_df)}')
            # st.dataframe(pu6_result_df.iloc[:, 1])
            data = conn.read(worksheet="PU6", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = pu6_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="PU6",data=new_data)
        except Exception as e:
            st.error(f"Error parsing PU6: {e}")

    # PU7
    if pu7_pasted_text:
        try:
            pu7_df = pd.read_csv(StringIO(pu7_pasted_text), sep="\t", header=None)
            pu7_df = pu7_df.drop(index=[0, 1, 2, 3, 4])

            pu7_result_dict = {0: [], 1: [], 2: [], 3: []}
            for i in range(len(pu7_df)):
                key = i % 4
                row_values = pu7_df.iloc[i]
                pu7_result_dict[key].append(row_values)

            pu7_result_df = pd.DataFrame(pu7_result_dict)
            for col in pu7_result_df.columns[1:]:
                pu7_result_df[col] = pu7_result_df[col].apply(clean_cell)

            st.success(f'PU7 Count: {len(pu7_result_df)}')
            # st.dataframe(pu7_result_df.iloc[:, 1])
            data = conn.read(worksheet="PU7", usecols=list(range(1)))
            new_data=pd.DataFrame()
            new_data['Name'] = pu7_result_df[1]


            # st.write(new_data)

            conn.update(worksheet="PU7",data=new_data)
        except Exception as e:
            st.error(f"Error parsing PU7: {e}")
    # st.write("5) Copy this to outlook:")

    # st.markdown("""
    # Hi Team,<br><br>

    # We are writing to let you know that clients listed are trading excessively with over 20,000 orders per week with order modification. Please inform clients to adjust EA configurations and trading behaviors to avoid causing server overloading.<br>

    # """, unsafe_allow_html=True)
    # if pu_pasted_text:
    #     st.markdown("<br><u><strong>PU</strong></u>", unsafe_allow_html=True)
    #     st.markdown(
    #     pu_result_df.iloc[:, [1]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )
    
    # if pu2_pasted_text:
    #     st.markdown("""
    #     <br>

    #     <u><strong>PU2</strong></u>
    #     """, unsafe_allow_html=True)
    #     st.markdown(
    #     pu2_result_df.iloc[:, [1]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )

    # if pu3_pasted_text:

    #     st.markdown("""
    #     <br>

    #     <u><strong>PU3</strong></u>
    #     """, unsafe_allow_html=True)
    #     st.markdown(
    #     pu3_result_df.iloc[:, [1]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )

    # if pu4_pasted_text:

    #     st.markdown("""
    #     <br>

    #     <u><strong>PU4</strong></u>
    #     """, unsafe_allow_html=True)
    #     st.markdown(
    #     pu4_result_df.iloc[:, [1]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )

    # if pu5_pasted_text:

    #     st.markdown("""
    #     <br>

    #     <u><strong>PU5</strong></u>
    #     """, unsafe_allow_html=True)
    #     st.markdown(
    #     pu5_result_df.iloc[:, [1]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )

    # if pu6_pasted_text:

    #     st.markdown("""
    #     <br>

    #     <u><strong>PU6</strong></u>
    #     """, unsafe_allow_html=True)
    #     st.markdown(
    #     pu6_result_df.iloc[:, [1]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )

    # if pu7_pasted_text:

    #     st.markdown("""
    #     <br>

    #     <u><strong>PU7</strong></u>
    #     """, unsafe_allow_html=True)
    #     st.markdown(
    #     pu7_result_df.iloc[:, [1]].to_html(index=False, header=False),
    #     unsafe_allow_html=True
    #     )
    # st.markdown("""
    # <br>

    # What would CS Team need to know?<br><br>

    # The clients were informed because of Hyperactive EA Trading might cause server excessive loading. This notification letter is a reminder to inform clients applying adjustments to avoid further influence. At the moment, System Admin would not apply any execution against clients. System Admin will inform again if clients refuse to make adjustment or apply inappropriate adjustment might cause server overloading.<br><br>

    # What would CS Team need to do?<br><br>

    # Please kindly inform client to adjust EA configuration or trading behavior accordingly and help to assist clients if they need. The threshold value was listed as below if client would like to know. System Admin would also preserve the right to take execution regarding to other abnormal behaviors causing server excessive loading. For instance, consistently login and logout without actual operations/several times of request sending to server within a second/unknown network pumping, etc."<br><br>

    # More than 3 times within a second<br>
    # More than 600 times within 30 minutes.<br><br><br>

    # Best Regards,<br>
    # System Admin
    # """, unsafe_allow_html=True)
    
    email_body = 'Hi Team,\n\nWe are writing to let you know that clients listed are trading excessively with over 20,000 orders per week with order modification. Please inform clients to adjust EA configurations and trading behaviors to avoid causing server overloading.\n\n\n\nWhat would CS Team need to know?\n\nThe clients were informed because of Hyperactive EA Trading might cause server excessive loading. This notification letter is a reminder to inform clients applying adjustments to avoid further influence. At the moment, System Admin would not apply any execution against clients. System Admin will inform again if clients refuse to make adjustment or apply inappropriate adjustment might cause server overloading.\n\nWhat would CS Team need to do?\n\nPlease kindly inform client to adjust EA configuration or trading behavior accordingly and help to assist clients if they need. The threshold value was listed as below if client would like to know. System Admin would also preserve the right to take execution regarding to other abnormal behaviors causing server excessive loading. For instance, consistently login and logout without actual operations/several times of request sending to server within a second/unknown network pumping, etc."\n\nMore than 3 times within a second\nMore than 600 times within 30 minutes.\n\n\nBest Regards,\nSystem Admin'

    # st.button("Copy Email Format",on_click=on_copy_click, args=(email_body,))
    # st.text_area("Copy Email Format", email_body, height=300)



    st.write("3) Copy and paste into outlook")

    pu_string = ""

    if pu_pasted_text:
        pu_string += "PU\n"
        for i in pu_result_df[1]:
            pu_string += i + "\n"

    if pu2_pasted_text:
        if pu_string:
            pu_string += "\n"
        pu_string += "PU2\n"
        for i in pu2_result_df[1]:
            pu_string += i + "\n"

    if pu3_pasted_text:
        if pu_string:
            pu_string += "\n"
        pu_string += "PU3\n"
        for i in pu3_result_df[1]:
            pu_string += i + "\n"

    if pu4_pasted_text:
        if pu_string:
            pu_string += "\n"
        pu_string += "PU4\n"
        for i in pu4_result_df[1]:
            pu_string += i + "\n"

    if pu5_pasted_text:
        if pu_string:
            pu_string += "\n"
        pu_string += "PU5\n"
        for i in pu5_result_df[1]:
            pu_string += i + "\n"

    if pu6_pasted_text:
        if pu_string:
            pu_string += "\n"
        pu_string += "PU6\n"
        for i in pu6_result_df[1]:
            pu_string += i + "\n"

    if pu7_pasted_text:
        if pu_string:
            pu_string += "\n"
        pu_string += "PU7\n"
        for i in pu7_result_df[1]:
            pu_string += i + "\n"

    # st.button("Copy PU Table", on_click=on_copy_click, args=(pu_string[:-1],))
    # st.text_area("Copy Email Format", pu_string[:-1], height=300)


    # st.button("Copy ST Table",on_click=on_copy_click, args=(st_string[:-1],))

    final_email_body = email_body.replace(
    "avoid causing server overloading.\n\n\n\n",
    "avoid causing server overloading.\n\n" + pu_string + "\n"
    )

    # st.text_area("Copy ST Table", st_string[:-1], height=300)
    st.code(final_email_body, language="text")

