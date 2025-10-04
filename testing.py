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




st.title("Copy Button Example")

# Example text
text_to_copy = "Hello, this is some text you can copy!"

# Show the text
st.code(text_to_copy, language="text")

# # Add a copy button
# copy_button(
#     text_to_copy,
#     icon='material_symbols',          # optional: Streamlit-style icon
#     tooltip='Click to copy text',     # optional: hover tooltip
#     copied_label='Copied!',           # optional: text shown after click
#     key='copy_text_to_clipboard'      # required: must be unique per button
# )
