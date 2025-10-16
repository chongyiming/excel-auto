import streamlit as st
import pandas as pd
from io import StringIO

st.write("http://192.168.1.38:5568/ServerHealth/Auto_Server_Check")
free_memory_text = st.text_area("Free Memory")
free_memory = pd.read_csv(StringIO(free_memory_text), sep="\t")
free_memory_sorted=free_memory.sort_values(by='Total Counts', ascending=False)
st.dataframe(free_memory_sorted)

st.write("More than 100 total counts")
free_memory_sorted_100=free_memory_sorted[free_memory_sorted['Total Counts']>100]
st.dataframe(free_memory_sorted_100)

logins = free_memory_sorted_100['Login'].tolist()
print(logins)
for i in range(0, len(logins), 7):
    row = logins[i:i+7]
    st.code(", ".join(str(login) for login in row), language="text")

