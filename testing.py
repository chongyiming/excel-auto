import streamlit as st
import pandas as pd


data = [
    ['Chloe Ngu'],
    ['Ting Hee'],
    ['Ivan Wong']
]
df = pd.DataFrame(data, columns=['Name'])


st.dataframe(df)