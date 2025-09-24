# import re

# completed_ids = set()
# all_matches = []

# # Step 1: 读取日志文件
# with open("logfile.txt", "r", encoding="utf-8") as file:
#     lines = file.readlines()
#     print(lines[0])

# # Step 2: 找出所有 completed 的 orderid
# for line in lines:
#     if re.search(r"\bcompleted\b", line, re.IGNORECASE):
#         found = re.findall(r"#\d+", line)
#         completed_ids.update(found)

# # Step 3: 找出所有非 completed 的 orderid
# for line in lines:
#     found = re.findall(r"#\d+", line)
#     for order_id in found:
#         if order_id not in completed_ids:
#             all_matches.append(order_id)

# # Step 4: 去重并按数字排序
# unique_matches = sorted(set(all_matches), key=lambda x: int(x[1:]))

# # Step 5: 写入文件
# with open("unique_hash_numbers.txt", "w", encoding="utf-8") as output:
#     output.write(",".join(unique_matches))

# print("✅ Done! Saved to 'unique_hash_numbers.txt'")

import streamlit as st
import pandas as pd
from io import StringIO
import ast
import re

completed_ids = set()
all_matches = []

log_text = st.text_area(" ", height=200, key="log_text")
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

        st.write(", ".join(unique_matches))


    except:
        pass
