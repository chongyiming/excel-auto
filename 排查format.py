import streamlit as st
import pandas as pd
from io import StringIO

# Define columns correctly
col1, col2, col3, col4, col5 = st.columns(5)

# Text areas
with col1:
    st_pasted_text = st.text_area("ST")
with col2:
    st2_pasted_text = st.text_area("ST2")
with col3:
    st4_pasted_text = st.text_area("ST4")
with col4:
    pu6_pasted_text = st.text_area("PU6")
with col5:
    pu7_pasted_text = st.text_area("PU7")

# Function to process pasted text
def process_text(pasted_text):
    if not pasted_text:
        return None

    # Split lines and clean
    lines = [line.strip() for line in pasted_text.splitlines() if line.strip()]

    # Remove header or irrelevant lines
    header_keywords = ["Login", "Time", "Request/sec", "Total"]
    lines = [line for line in lines if line not in header_keywords and not line.startswith("(")]

    # Group every 4 lines
    data = [lines[i:i+4] for i in range(0, len(lines), 4)]

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Login", "Time", "Request/sec", "Total"])

    # Convert data types
    df["Login"] = pd.to_numeric(df["Login"], errors="coerce")
    df["Request/sec"] = pd.to_numeric(df["Request/sec"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

    # Add header row
    new_row = pd.DataFrame({'Login': ["Login"], 'Time': ["Time"], 'Request/sec': ["Request/sec"], 'Total': ["Total"]})
    df = pd.concat([new_row, df], ignore_index=True)

    # Swap columns (if needed)
    df[["Login", "Time"]] = df[["Time", "Login"]].values
    df.columns = ['Time', 'Login', 'Request/sec', 'Total']

    return df


# Process each pasted text dynamically
datasets = {
    "ST": process_text(st_pasted_text),
    "ST2": process_text(st2_pasted_text),
    "ST4": process_text(st4_pasted_text),
    "PU6": process_text(pu6_pasted_text),
    "PU7": process_text(pu7_pasted_text),
}

# Display available DataFrames
for name, df in datasets.items():
    if df is not None:
        st.subheader(f"{name} Data")
        st.dataframe(df)


