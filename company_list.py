import streamlit as st
import pandas as pd
from datetime import datetime

# Load data
file_path = 'gaborone_companies_with_tracking.csv'
df = pd.read_csv(file_path)

st.title("📞 Company Contact Tracker")

# Editable table row-by-row
for i in df.index:
    with st.expander(f"{df['Company Name'][i]}"):
        st.write(f"**Address:** {df['Address'][i]}")
        st.write(f"**Phone:** {df['Phone Number'][i]}")
        st.markdown(f"**Website:** [{df['Website (Profile Link)'][i]}]({df['Website (Profile Link)'][i]})")
        st.write(f"**Description:** {df['Description'][i]}")
        
        # Editable fields
        df.at[i, 'Contacted'] = st.selectbox("Contacted?", ['No', 'Yes'], index=['No', 'Yes'].index(df['Contacted'][i]), key=f"contacted_{i}")
        df.at[i, 'Date Contacted'] = st.date_input("Date Contacted", 
                                                   value=pd.to_datetime(df['Date Contacted'][i]) if pd.notna(df['Date Contacted'][i]) and df['Date Contacted'][i] else datetime.today(), 
                                                   key=f"date_contacted_{i}") if df.at[i, 'Contacted'] == 'Yes' else ''
        df.at[i, 'Response Received'] = st.selectbox("Response Received?", ['No', 'Yes'], index=['No', 'Yes'].index(df['Response Received'][i]), key=f"response_{i}")
        df.at[i, 'Response Date'] = st.date_input("Response Date", 
                                                  value=pd.to_datetime(df['Response Date'][i]) if pd.notna(df['Response Date'][i]) and df['Response Date'][i] else datetime.today(), 
                                                  key=f"response_date_{i}") if df.at[i, 'Response Received'] == 'Yes' else ''
        df.at[i, 'Notes'] = st.text_area("Notes", value=df['Notes'][i], key=f"notes_{i}")

st.markdown("---")
if st.button("💾 Save Updates"):
    df.to_csv(file_path, index=False)
    st.success("Updates saved to CSV!")

