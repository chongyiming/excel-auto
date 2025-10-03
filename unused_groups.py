import pandas as pd
import streamlit as st
import pandas as pd
from io import StringIO

# Text input from user
sheet1 = st.text_area("Account", height=200, key="Account")
sheet2 = st.text_area("Group", height=200, key="Group")

sheet1_df = pd.read_csv(StringIO(sheet1), sep="\t", header=None)
# st.write(sheet1_df)

# Extract unique values from column 2 (index 2)
groups_in_sheet1 = sheet1_df.iloc[:, 2].dropna().unique()
# st.write("Groups in Sheet1:", groups_in_sheet1)


sheet2_df = pd.read_csv(StringIO(sheet2), sep="\t", header=None)
# st.write(sheet2_df)

# Extract unique values from column 0 (index 0)
groups_in_sheet2 = sheet2_df.iloc[:, 0].dropna().unique()
# st.write("Groups in Sheet2:", groups_in_sheet2)

exclude_list = ["datacenter", "coverage", "demoforex", "preliminary", "manager", "LIVE_instiview"]
groups_in_sheet2 = [
    g for g in groups_in_sheet2 
    if not str(g).startswith("T") and g not in exclude_list
]

unused_groups = [g for g in groups_in_sheet2 if g not in groups_in_sheet1]
st.dataframe(unused_groups)
# output_file = "unused_groups.xlsx"
# pd.DataFrame(unused_groups, columns=["Unused Groups"]).to_excel(output_file, index=False)

# print("Done", output_file)
