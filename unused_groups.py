import pandas as pd
import streamlit as st
import pandas as pd
from io import StringIO


sheet1 = st.text_area("Account", height=200, key="Account")
sheet2 = st.text_area("Group", height=200, key="Group")

sheet1_df = pd.read_csv(StringIO(sheet1), sep="\t", header=None)

groups_in_sheet1 = sheet1_df.iloc[:, 2].dropna().unique()


sheet2_df = pd.read_csv(StringIO(sheet2), sep="\t", header=None)

groups_in_sheet2 = sheet2_df.iloc[:, 0].dropna().unique()

exclude_list = ["datacenter", "coverage", "demoforex", "preliminary", "manager", "LIVE_instiview"]
groups_in_sheet2 = [
    g for g in groups_in_sheet2 
    if not str(g).startswith("T") and g not in exclude_list
]

unused_groups = [g for g in groups_in_sheet2 if g not in groups_in_sheet1]
st.dataframe(unused_groups)

# # Convert the list into a DataFrame
# unused_groups_df = pd.DataFrame(unused_groups, columns=["Unused Groups"])

# # Show interactive table
# interactive_table(unused_groups_df,
#                   caption='testing',
#                   buttons=['copyHtml5', 'colvis'])
