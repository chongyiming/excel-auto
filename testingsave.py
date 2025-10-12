import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="Sheet1", usecols=list(range(2)))
st.dataframe(data)
new_data=pd.DataFrame([{"Name":"yes",
"Age":"Test"}])
with st.form(key="form"):
    info=st.text_area(label="info")
    submit_button=st.form_submit_button(label="submit")

    if submit_button:
        conn.update(data=new_data)