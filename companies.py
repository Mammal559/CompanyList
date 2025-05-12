
import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Company List", layout="wide")

# Load data
csv_file = "gaborone_companies_with_tracking.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=[
        "Company Name", "Address", "Phone Number", "Website (Profile Link)",
        "Description", "Contacted", "Date Contacted", "Response Received", 
        "Response Date", "Notes"
    ])

# Ensure proper date formats
df["Date Contacted"] = pd.to_datetime(df["Date Contacted"], errors='coerce')
df["Response Date"] = pd.to_datetime(df["Response Date"], errors='coerce')

# Sidebar filters
st.sidebar.header("🔍 Filters")
search_query = st.sidebar.text_input("Search by Company Name")
filter_contacted = st.sidebar.selectbox("Filter by Contacted", ["All", "Yes", "No"])
filter_response = st.sidebar.selectbox("Filter by Response Received", ["All", "Yes", "No"])

# Apply filters
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df["Company Name"].str.contains(search_query, case=False, na=False)]
if filter_contacted != "All":
    filtered_df = filtered_df[filtered_df["Contacted"] == filter_contacted]
if filter_response != "All":
    filtered_df = filtered_df[filtered_df["Response Received"] == filter_response]

# Title
st.title("📇 Company List Tracker")

# Editable table
edited_df = st.data_editor(
    filtered_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Date Contacted": st.column_config.DateColumn("Date Contacted", format="YYYY-MM-DD"),
        "Response Date": st.column_config.DateColumn("Response Date", format="YYYY-MM-DD"),
        "Contacted": st.column_config.SelectboxColumn("Contacted", options=["Yes", "No", ""]),
        "Response Received": st.column_config.SelectboxColumn("Response Received", options=["Yes", "No", ""]),
    },
    key="company_edit"
)

# Save button
if st.button("💾 Save Changes"):
    edited_df.to_csv(csv_file, index=False)
    st.success("Changes saved successfully!")

# Charts section
st.subheader("📊 Company Contact Analysis")

col1, col2 = st.columns(2)

# Pie chart: Contacted
with col1:
    contacted_counts = df["Contacted"].value_counts(dropna=True).reindex(["Yes", "No"], fill_value=0)
    fig1 = px.pie(values=contacted_counts.values, names=contacted_counts.index, title="Contacted Distribution")
    st.plotly_chart(fig1, use_container_width=True)

# Bar chart: Response Received by Date
with col2:
    if not df["Response Date"].isna().all():
        response_by_date = df.dropna(subset=["Response Date"])
        count_by_date = response_by_date.groupby(response_by_date["Response Date"].dt.date).size().reset_index(name="Responses")
        fig2 = px.bar(count_by_date, x="Response Date", y="Responses", title="Responses Over Time")
        st.plotly_chart(fig2, use_container_width=True)

# Line chart: Date Contacted over time
if not df["Date Contacted"].isna().all():
    contact_by_date = df.dropna(subset=["Date Contacted"])
    contact_counts = contact_by_date.groupby(contact_by_date["Date Contacted"].dt.date).size().reset_index(name="Contacts")
    fig3 = px.line(contact_counts, x="Date Contacted", y="Contacts", title="Contacts Over Time")
    st.plotly_chart(fig3, use_container_width=True)
