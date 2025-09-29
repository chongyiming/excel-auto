import streamlit as st
import pandas as pd
from pymongo import MongoClient
from io import StringIO

# MongoDB connection
mongo_uri = "mongodb+srv://yimingchonghytech:Amaci123456789012!@cluster0.fwtqwlo.mongodb.net/"
client = MongoClient(mongo_uri)
db = client.test
collection = db.datas

al_input_text = st.text_area("Paste your Excel data (without 'ID' & 'Currency' header) and save to database", height=200)

if al_input_text:
    try:
        df = pd.read_csv(StringIO(al_input_text), sep="\t", header=None)

        if df.shape[1] != 2:
            st.error("Please make sure the pasted data has exactly 2 columns.")
        else:
            df.columns = ['ID', 'Currency']
            st.subheader("Parsed Data:")
            st.dataframe(df)

            if st.button("Save to Database"):
                docs = df.to_dict(orient='records')
                result = collection.insert_many(docs)
                st.success(f"Successfully inserted {len(result.inserted_ids)} records.")
    except Exception as e:
        st.error(f"Error reading pasted data: {e}")

documents = list(collection.find())

if documents:
    db_df = pd.DataFrame(documents)
    if '_id' in db_df.columns:
        db_df.drop(columns=['_id'], inplace=True)

    st.subheader("Current Accounts in Database:")
    st.dataframe(db_df)
else:
    st.info("No documents found in the collection.")
