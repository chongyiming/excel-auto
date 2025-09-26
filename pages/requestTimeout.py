import streamlit as st
import pandas as pd
from io import StringIO
import ast
import re
from collections import defaultdict


rt_pasted_text = st.text_area("1) Paste Request Timeout (Get all accounts for each server)", height=200)

result_dict = defaultdict(list)

if rt_pasted_text:
    try:
        rt_df = pd.read_csv(StringIO(rt_pasted_text), sep="\t", header=None)

        # Build result_dict
        for i in range(len(rt_df)):
            key = str(rt_df.iloc[i, 0])  # e.g. account
            full_string = str(rt_df.iloc[i, 3])
            value = full_string.split(':')[0]  # Get part before the colon
            result_dict[key].append((str(rt_df.iloc[i, 1]), value[1:-1]))  # (timestamp, order_id)

        # Display extracted order IDs
        for account in result_dict:
            st.write(account, ":")
            order_ids = "|".join("'" + val + "'" for _, val in result_dict[account])
            st.write(order_ids)
    
    except Exception as e:
        st.error(f"Something went wrong: {e}")
completed_ids = set()
all_matches = []


st.markdown("""
<br>
""", unsafe_allow_html=True)
log_text = st.text_area("Paste log file here **(NOW ONLY SUPPORT INDIVIDUAL LOG)**", height=200, key="log_text")
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
