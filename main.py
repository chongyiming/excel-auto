import streamlit as st
import pandas as pd
from io import StringIO


st.title("📋 Paste Table Input App")


st.write("Paste your table from Excel/Sheets here:")


# Text area for input
pasted_text = st.text_area("Paste table here:", height=200)


if pasted_text:
    # Try parsing as CSV-like text (tabs or commas)
    try:
        df = pd.read_csv(StringIO(pasted_text), sep="\t",header=None)
        print(df)
        print(df[0])
        df[0]="UM"
        st.success("✅ Table parsed successfully!")
        st.dataframe(df)  # Show table

        
    except Exception as e:
        st.error(f"⚠️ Could not parse the table: {e}")