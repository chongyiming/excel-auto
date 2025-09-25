import streamlit as st
import pandas as pd
from io import StringIO
import ast
import re



completed_ids = set()
all_matches = []

log_text = st.text_area("Paste log file here", height=200, key="log_text")
if log_text:
    try:
        log_text_df = pd.read_csv(StringIO(log_text), sep="\t", header=None)

        for line in log_text_df[2].astype(str):  # ensure it's string
            # Find completed order IDs
            if re.search(r"\bcompleted\b", line, re.IGNORECASE):
                found = re.findall(r"#\d+", line)
                completed_ids.update(found)

        for line in log_text_df[2].astype(str):
            found = re.findall(r"#\d+", line)
            for order_id in found:
                if order_id not in completed_ids:
                    all_matches.append(order_id)

        unique_matches = sorted(set(all_matches), key=lambda x: int(x[1:]))
        if len(unique_matches)>0:
            st.write(", ".join(unique_matches))
        else:
            st.write("Could find incomplete order, randomly put a number")
            st.write(sorted(completed_ids)[-1])



    except:
        pass
