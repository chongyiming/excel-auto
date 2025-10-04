import streamlit as st
import pandas as pd
from st_copy import copy_button

data = [
    ['Chloe Ngu'],
    ['Ting Hee'],
    ['Ivan Wong']
]
df = pd.DataFrame(data, columns=['Name'])


st.dataframe(df)


