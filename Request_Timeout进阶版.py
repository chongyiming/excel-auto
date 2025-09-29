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
                        # st.write(entry_time)
                    except:
                        st.warning(f"Invalid datetime: {entry_time_str}")
                        continue

                    start_time = entry_time - timedelta(minutes=4)
                    # st.write("start",start_time)
                    end_time = entry_time - timedelta(minutes=2, seconds=59)
                    # st.write("end",end_time)


                    if "parsed_time" not in journal_df.columns:
                        journal_df["parsed_time"] = journal_df[0].astype(str).apply(parse_ts)

                    time_mask = journal_df["parsed_time"].between(start_time, end_time)

                    id_mask = journal_df[2].astype(str).str.contains(fr"'{login_id}'", na=False)

                    final_mask = time_mask & id_mask

                    filtered_logs = journal_df[final_mask].iloc[:, [0,1,2]]
                    # filtered_logs = journal_df[final_mask]


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

                

            st.markdown("""<br>""", unsafe_allow_html=True)
            st.subheader("All Orders Per Server (including fallback)")

            for key in result_dict:
                all_orders_flat = []
                login_ids_checked = set()

                for _, login_id in result_dict[key]:  # Use all login IDs, not just those in all_matches
                    login_ids_checked.add(login_id)
                    orders = all_matches[key].get(login_id, [])

                    if orders:
                        unique_orders = sorted(set(orders), key=lambda x: int(x[1:]))
                        all_orders_flat.extend(unique_orders)
                    else:
                        # Fallback: use latest completed_id for this login_id
                        completed_list = completed_ids[key].get(login_id, [])
                        if completed_list:
                            latest_completed = sorted(completed_list, key=lambda x: int(x[1:]))[-1]
                            all_orders_flat.append(latest_completed)

                summary_matches = sorted(set(all_orders_flat), key=lambda x: int(x[1:]))

                st.markdown(f"### Server: `{key}`")
                if summary_matches:
                    st.write(",".join(summary_matches))
                else:
                    st.write("No orders found (no incomplete or completed orders).")




        else:
            st.warning("Please fill in all journal text areas before proceeding.")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
