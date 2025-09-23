import streamlit as st
import pandas as pd
from io import StringIO
import ast

st.title("排查")

st.write("1) Paste table here:")
pasted_text = st.text_area("Table",height=200,key="text_area")

def clean_cell(cell):
    """Convert string-list to single value if needed."""
    if isinstance(cell, str):
        try:
            val = ast.literal_eval(cell)
            if isinstance(val, list) and len(val) == 1:
                return val[0]
            else:
                return val
        except:
            return cell
    else:
        return cell

if pasted_text:
    try:
        # Read pasted text as tab-separated values with no header
        df = pd.read_csv(StringIO(pasted_text), sep="\t", header=None)

        # Drop the first 5 rows (indexes 0-4)
        df = df.drop(index=[0, 1, 2, 3, 4])

        for col in df.columns:
            df[col] = df[col].apply(clean_cell)

        st.success("✅ Table parsed successfully!")
        st.dataframe(df)
        st.write("Row count:", len(df))


    except Exception as e:
        st.error(f"Error parsing table: {e}")


risk_tool_pasted_text = st.text_area("Table", height=200, key="risk_tool_text_area")
if risk_tool_pasted_text:
    try:
        risk_tool_df = pd.read_csv(StringIO(risk_tool_pasted_text), sep="\t", header=None)

        # Optional: clean cells
        for col in risk_tool_df.columns:
            risk_tool_df[col] = risk_tool_df[col].apply(clean_cell)

        st.success("✅ Table parsed successfully!")
        st.dataframe(risk_tool_df)
        st.write("Row count:", len(risk_tool_df))

    except Exception as e:
        st.error(f"Error parsing table: {e}")
