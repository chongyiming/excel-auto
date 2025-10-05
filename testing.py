import streamlit as st
import pandas as pd
from st_copy import copy_button

data = [
    ['Ting Hee'],
    ['Ivan Wong'],
    ['Wei Ming'],
    ['Chloe Ngu'],
    ['Amber Tai'],

]
df = pd.DataFrame(data, columns=['Name'])


st.dataframe(df)


