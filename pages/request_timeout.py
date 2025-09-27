# import streamlit as st
# import pandas as pd
# from io import StringIO
# from collections import defaultdict
# from datetime import datetime, timedelta


# rt_pasted_text = st.text_area("Request Timeout (Get all accounts)")

# result_dict = defaultdict(list)
# if rt_pasted_text:
#     try:
#         rt_df = pd.read_csv(StringIO(rt_pasted_text), sep="\t", header=None)

#         # Loop through each row
#         for i in range(len(rt_df)):
#             key = str(rt_df.iloc[i, 0])
#             full_string = str(rt_df.iloc[i, 3])
#             value = full_string.split(':')[0]  # Get part before the colon
#             result_dict[key].append((str(rt_df.iloc[i, 1]), value[1:-1]))

#         for i in result_dict:
#             st.write(i, ":")
#             output_string = ""
#             for _, value in result_dict[i]:
#                 output_string += "'"+value+"'" + "|"
#             st.write(output_string[0:-1])
#         print(result_dict)
#         st.write("2) Paste journal:")

#         columns = st.columns(len(result_dict))
#         text_inputs = {}

#         for i, (key, _) in enumerate(result_dict.items()):
#             with columns[i]:
#                 text_inputs[key] = st.text_area(f"Journal for {key}")

#         df_dict=defaultdict(list)
#         if all(len(text_inputs[key].strip()) > 0 for key in result_dict):
#             for key in text_inputs:
#                 for i, value_list in result_dict.items():
#                     if i == key:
#                         journal_df = pd.read_csv(StringIO(text_inputs[key]), sep="\t", header=None)
#                         for i in value_list:
#                             matching_rows = journal_df[journal_df[2].str.match(fr"'{i[1]}':")]
#                             st.write(matching_rows)





#         else:
#             st.warning("Please fill in all input fields before proceeding.")
#     except:
#         pass


import re

import streamlit as st
import pandas as pd
from io import StringIO
from collections import defaultdict
from datetime import datetime, timedelta


rt_pasted_text = st.text_area("1) Paste Request Timeout Log (Get all accounts)", height=200)

result_dict = defaultdict(list)

completed_ids = defaultdict(lambda: defaultdict(list))
all_matches = defaultdict(lambda: defaultdict(list))

if rt_pasted_text:
    try:
        rt_df = pd.read_csv(StringIO(rt_pasted_text), sep="\t", header=None)

        # Build result_dict
        for i in range(len(rt_df)):
            key = str(rt_df.iloc[i, 0])  # e.g. account
            full_string = str(rt_df.iloc[i, 3])
            value = full_string.split(':')[0]  # Get part before the colon
            result_dict[key].append((str(rt_df.iloc[i, 1]), value[1:-1]))

        # Display extracted order IDs
        for account in result_dict:
            # st.write(**account**, ":")
            st.markdown(f"**{account}**:")
            login_ids = "|".join("'" + val + "'" for _, val in result_dict[account])
            st.write(login_ids)

        st.markdown("""<br>""", unsafe_allow_html=True)

        st.write("2) Paste Journal Logs:")

        # Create dynamic journal input fields
        columns = st.columns(len(result_dict))
        text_inputs = {}

        for i, (key, _) in enumerate(result_dict.items()):
            with columns[i]:
                text_inputs[key] = st.text_area(f"Journal for {key}", height=200)

        # Only process if all journal inputs are filled
        df_dict = defaultdict(list)
        st.markdown("""<br>""", unsafe_allow_html=True)

        st.write("3) Journals before request time out for each login (3-4 minutes range)")

        if all(len(text_inputs[key].strip()) > 0 for key in result_dict):
            for key in text_inputs:
                journal_df = pd.read_csv(StringIO(text_inputs[key]), sep="\t", header=None)

                if journal_df.shape[1] < 3:
                    st.error(f"Journal data for {key} has fewer than 3 columns.")
                    continue

                journal_df[0] = journal_df[0].astype(str)
                journal_df[2] = journal_df[2].astype(str)

                def parse_ts(ts):
                    for fmt in ("%Y.%m.%d %H:%M:%S.%f", "%Y.%m.%d"):
                        try:
                            return datetime.strptime(ts, fmt)
                        except:
                            continue
                    return None

                journal_df["parsed_time"] = journal_df[0].apply(parse_ts)

                for entry_time_str, login_id in result_dict[key]:

                    st.markdown(f"**{key}**:")

                    try:
                        entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
                    except:
                        st.warning(f"Invalid datetime: {entry_time_str}")
                        continue

                    start_time = entry_time - timedelta(minutes=4)
                    end_time = entry_time - timedelta(minutes=3)

                    if "parsed_time" not in journal_df.columns:
                        journal_df["parsed_time"] = journal_df[0].astype(str).apply(parse_ts)

                    time_mask = journal_df["parsed_time"].between(start_time, end_time)

                    id_mask = journal_df[2].astype(str).str.contains(fr"'{login_id}'", na=False)

                    final_mask = time_mask & id_mask

                    filtered_logs = journal_df[final_mask].iloc[:, [0,1,2]]

                    if not filtered_logs.empty:
                        st.write(f"`{login_id}`")
                        st.write(filtered_logs)
                        for line in filtered_logs[2].astype(str):
                            if re.search(r"\bcompleted\b", line, re.IGNORECASE):
                                found = re.findall(r"#\d+", line)
                                for order_id in found:
                                    if order_id not in completed_ids[key][login_id]:
                                        completed_ids[key][login_id].append(order_id)

                        for line in filtered_logs[2].astype(str):
                            found = re.findall(r"#\d+", line)
                            for order_id in found:
                                if order_id not in completed_ids[key][login_id] and order_id not in all_matches[key][login_id]:
                                    all_matches[key][login_id].append(order_id)
                        
                    else:
                        st.write(f"No logs for `{login_id}`")


            st.markdown("""<br>""", unsafe_allow_html=True)

                

            for key in all_matches:

                all_orders_flat = []

                for login_id in all_matches[key]:
                    order_ids = all_matches[key][login_id]
                    unique_matches = sorted(set(order_ids), key=lambda x: int(x[1:]))

                    all_orders_flat.extend(unique_matches)

                        
                st.markdown("""<br>""", unsafe_allow_html=True)

                

                summary_matches = sorted(set(all_orders_flat), key=lambda x: int(x[1:]))
                if summary_matches:
                    st.subheader(f"All orders for `{key}`:")
                    st.write(",".join(summary_matches))
                else:
                    st.subheader(f"All orders for `{key}`:")
                    st.write("No incomplete orders found for this account.")



        else:
            st.warning("Please fill in all journal text areas before proceeding.")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
