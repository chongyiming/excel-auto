import streamlit as st
import pandas as pd
from io import StringIO

rt_pasted_text = st.text_area("Request Timeout")
con_strings = []
if rt_pasted_text:
    try:
        rt_df = pd.read_csv(StringIO(rt_pasted_text), sep="\t", header=None)

        for line in rt_df[3].astype(str):  # Ensure it's string
            prefix = line.split(':')[0]
            con_strings.append(prefix)

        if con_strings:
            final_string = "|".join(con_strings) + "|"
            st.write(final_string[0:-1])
    except:
        pass