import pandas as pd
import streamlit as st
import pandas as pd
from io import StringIO

option1 = st.selectbox(
    "Select Type",
    ("Journal","Instance"),
)


uploaded_file = st.file_uploader("Upload Excel File", key="excel")

if uploaded_file:
    uploaded_file=pd.read_excel(uploaded_file,header=None)
    if option1=="Journal":
        filtered_df = uploaded_file[uploaded_file[2].astype(str).str.contains("modify", case=False, na=False)]
        split_df = filtered_df[2].astype(str).str.split(":", expand=True)
        count_series = split_df[0].value_counts().reset_index()
        count_series.columns = ["Value", "Count"]
        st.subheader("Modify")
        st.dataframe(count_series)

        filtered_df1 = uploaded_file[uploaded_file[2].astype(str).str.contains("no money", case=False, na=False)]
        split_df1 = filtered_df1[2].astype(str).str.split(":", expand=True)
        count_series1 = split_df1[0].value_counts().reset_index()
        count_series1.columns = ["Value", "Count"]
        st.subheader("No Money")
        st.dataframe(count_series1)

        filtered_df2 = uploaded_file[uploaded_file[2].astype(str).str.contains("invalid password", case=False, na=False)]
        split_df2 = filtered_df2[2].astype(str).str.split(":", expand=True)
        count_series2 = split_df2[0].value_counts().reset_index()
        count_series2.columns = ["Value", "Count"]
        st.subheader("Invalid Password")
        st.dataframe(count_series2)
    if option1=="Instance":
        filtered_df = uploaded_file[uploaded_file[3].astype(str).str.contains("modify", case=False, na=False)]
        split_df = filtered_df[3].astype(str).str.split(":", expand=True)
        count_series = split_df[0].value_counts().reset_index()
        count_series.columns = ["Value", "Count"]
        st.subheader("Modify")
        st.dataframe(count_series)

        filtered_df1 = uploaded_file[uploaded_file[3].astype(str).str.contains("no money", case=False, na=False)]
        split_df1 = filtered_df1[3].astype(str).str.split(":", expand=True)
        count_series1 = split_df1[0].value_counts().reset_index()
        count_series1.columns = ["Value", "Count"]
        st.subheader("No Money")
        st.dataframe(count_series1)

        filtered_df2 = uploaded_file[uploaded_file[3].astype(str).str.contains("invalid password", case=False, na=False)]
        split_df2 = filtered_df2[3].astype(str).str.split(":", expand=True)
        count_series2 = split_df2[0].value_counts().reset_index()
        count_series2.columns = ["Value", "Count"]
        st.subheader("Invalid Password")
        st.dataframe(count_series2)