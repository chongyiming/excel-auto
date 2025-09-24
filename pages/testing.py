import streamlit as st
import pandas as pd
from io import StringIO
import ast

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
        pasted_text = st.text_area("UM", height=300)

    with col2:
        um2pasted_text = st.text_area("UM2", height=300)



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

            if option =="UM" or option=="UM2":
                st.success(f'UM Count: {len(result_df)}')
                st.dataframe(result_df.iloc[:, [0, 1]])
            else:
                st.dataframe(result_df.iloc[:, 1])



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

            if option =="UM" or option=="UM2":
                st.success(f'UM2 Count: {len(result_df)}')

                st.dataframe(um2_result_df.iloc[:, [0, 1]])
            else:
                st.dataframe(um2_result_df.iloc[:, 1])


        except Exception as e:
            st.error(f"Error parsing table: {e}")



elif option=="ST":
    st.write("2) Paste Per seconds modified here:")

    col1, col2,col3 = st.columns(3)

    with col1:
        st_pasted_text = st.text_area("ST", height=300)

    with col2:
        st2_pasted_text = st.text_area("ST2", height=300)

    with col3:
        st4_pasted_text = st.text_area("ST4", height=300)



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
            st.dataframe(st_result_df.iloc[:, 1])



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
            st.dataframe(st2_result_df.iloc[:, 1])

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
            st.dataframe(st4_result_df.iloc[:, 1])

        except Exception as e:
            st.error(f"Error parsing ST4 table: {e}")


    
            

st.write("3) Go to http://192.168.1.39:8000/find_info")


st.write("4) Paste Advanced account info here:")

risk_tool_pasted_text = st.text_area(" ", height=200, key="risk_tool_text_area")
if risk_tool_pasted_text:
    try:
        risk_tool_df = pd.read_csv(StringIO(risk_tool_pasted_text), sep="\t", header=None)
        risk_tool_df = risk_tool_df.drop(index=0)


        st.success("✅ Table parsed successfully!")
        st.dataframe(risk_tool_df.iloc[:, [0,1,2,3,4,6]])
        st.write("Row count:", len(risk_tool_df))

    except Exception as e:
        st.error(f"Error parsing table: {e}")
