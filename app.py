import streamlit as st
import pandas as pd

# Load the CSV data into a DataFrame
@st.cache
def load_data():
    data = pd.read_csv('jobs.csv')  # Comma is the default, so no need to specify
    return data

data = load_data()

# Sidebar filters
st.sidebar.header('Filter options')

# Dynamically create filters for each field
for column in data.columns:
    unique_values = data[column].dropna().unique()
    selected_values = st.sidebar.multiselect(f'Filter by {column}', unique_values)
    if selected_values:
        data = data[data[column].isin(selected_values)]

# Display the filtered DataFrame
st.write(data)
