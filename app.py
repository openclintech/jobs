import streamlit as st
import pandas as pd

# Load the CSV data into a DataFrame
@st.cache
def load_data():
    data = pd.read_csv('jobs.csv')
    # Convert compensation columns to numeric, removing any non-numeric characters
    data['compensation_min'] = pd.to_numeric(data['compensation_min'].replace('[\$,]', '', regex=True), errors='coerce')
    data['compensation_max'] = pd.to_numeric(data['compensation_max'].replace('[\$,]', '', regex=True), errors='coerce')
    return data

data = load_data()

# Sidebar filters
st.sidebar.header('Filter options')

# Compensation range input
min_compensation = st.sidebar.number_input('Minimum Compensation ($)', min_value=0, max_value=int(data['compensation_max'].max()), step=1000, format='%d')
max_compensation = st.sidebar.number_input('Maximum Compensation ($)', min_value=0, max_value=int(data['compensation_max'].max()), step=1000, format='%d', value=int(data['compensation_max'].max()))

# Filter data based on compensation
if min_compensation or max_compensation:
    data = data[(data['compensation_min'] >= min_compensation) & (data['compensation_max'] <= max_compensation)]

# Dynamically create filters for other fields
for column in data.columns.drop(['compensation_min', 'compensation_max']):
    unique_values = data[column].dropna().unique()
    selected_values = st.sidebar.multiselect(f'Filter by {column}', unique_values)
    if selected_values:
        data = data[data[column].isin(selected_values)]

# Display the filtered DataFrame
st.write(data)
