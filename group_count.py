import streamlit as st
import pandas as pd
from io import BytesIO, StringIO

sheet2 = st.text_area("Group", height=200, key="Group")

sheet2_df = pd.read_csv(StringIO(sheet2), sep="\t", header=None)
st.write("Group count",len(sheet2_df[0]))