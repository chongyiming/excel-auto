import pandas as pd
import streamlit as st

uploaded_file = st.file_uploader("Upload CSV File", key="excel")

if uploaded_file is not None:
    sheet2_df = pd.read_csv(uploaded_file, sep=",")
    st.dataframe(sheet2_df)

    chunk_results = []

    unique_servers = sheet2_df['Server_Name'].unique()

    for server in unique_servers:
        server_rows = sheet2_df[sheet2_df['Server_Name'] == server]
        logins = server_rows['login'].astype(str).tolist()
        if server == 'inf_mt5':
            end=14
        else:
            end=7
        for i in range(0, len(logins), end):
            chunk = logins[i:i+end]
            concatenated = ",".join(chunk)
            chunk_number = (i // end) + 1
            chunk_results.append({
                'Server_Name': server,
                'Chunk_Number': chunk_number,
                'Login_Chunk': concatenated
            })

    chunk_df = pd.DataFrame(chunk_results)

    for _, row in chunk_df.iterrows():
        st.markdown(f"**Server:** {row['Server_Name']}")
        st.code(row['Login_Chunk'], language="text")
        st.markdown("---")  # Divider line

