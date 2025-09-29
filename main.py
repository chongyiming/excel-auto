import streamlit as st
# import pandas as pd
# from io import StringIO
# import ast

# st.title("排查")

# st.write("1) Select server")

# option = st.selectbox(
#     "Select server",
#     ("UM","UM2","ST","ST2","ST4"),
# )

# st.write("You selected:", option)
# st.write("2) Paste Per seconds modified here:")
# pasted_text = st.text_area(" ",height=200,key="text_area")

# def clean_cell(cell):
#     """Convert string-list to single value if needed."""
#     if isinstance(cell, str):
#         try:
#             val = ast.literal_eval(cell)
#             if isinstance(val, list) and len(val) == 1:
#                 return val[0]
#             else:
#                 return val
#         except:
#             return cell
#     else:
#         return cell

# if pasted_text:
#     try:
#         # Read pasted text as tab-separated values with no header
#         df = pd.read_csv(StringIO(pasted_text), sep="\t", header=None)

#         # Drop the first 5 rows (indexes 0-4)
#         df = df.drop(index=[0, 1, 2, 3, 4])

#         # Create dictionary with keys 0-3 for grouping rows in fours
#         result_dict = {0: [], 1: [], 2: [], 3: []}
#         for i in range(len(df)):
#             key = i % 4
#             row_values = df.iloc[i]
#             result_dict[key].append(row_values)

#         # Convert to DataFrame
#         result_df = pd.DataFrame(result_dict)

#         # Overwrite first column's all values with "UM"
#         result_df.iloc[:, 0] = option

#         # Clean columns 1, 2, 3 to unpack any stringified lists
#         for col in result_df.columns[1:]:
#             result_df[col] = result_df[col].apply(clean_cell)

#         st.success("✅ Table parsed successfully!")
#         if option =="UM" or option=="UM2":
#             st.dataframe(result_df.iloc[:, [0, 1]])
#         else:
#             st.dataframe(result_df.iloc[:, 1])

#         st.write("Count: ",len(result_df))


#     except Exception as e:
#         st.error(f"Error parsing table: {e}")

# st.write("3) Go to http://192.168.1.39:8000/find_info")


# st.write("4) Paste Advanced account info here:")

# risk_tool_pasted_text = st.text_area(" ", height=200, key="risk_tool_text_area")
# if risk_tool_pasted_text:
#     try:
#         risk_tool_df = pd.read_csv(StringIO(risk_tool_pasted_text), sep="\t", header=None)
#         risk_tool_df = risk_tool_df.drop(index=0)


#         st.success("✅ Table parsed successfully!")
#         st.dataframe(risk_tool_df.iloc[:, [0,1,2,3,4,6]])
#         st.write("Row count:", len(risk_tool_df))

#     except Exception as e:
#         st.error(f"Error parsing table: {e}")
# st.image("cannot-do.png")


pages = {
    "Dashboard": [
        st.Page("main.py", title="Homepage"),
    ],
    "Request Timeout": [
        st.Page("Request_Timeout.py", title="Request Timeout"),
        st.Page("Request_Timeout进阶版.py", title="Request Timeout(进阶版)"),
    ],
    "负载排查": [
        st.Page("排查.py", title="排查"),
        st.Page("account_lists.py", title="Account")

    ]
}

pg = st.navigation(pages)
pg.run()