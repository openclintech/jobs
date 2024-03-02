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

# Checkbox to include jobs without compensation details
include_no_comp = st.sidebar.checkbox('Include jobs without compensation details', True)

# Compensation range input
min_compensation = st.sidebar.number_input('Minimum Compensation ($)', min_value=0, max_value=int(data['compensation_max'].max(skipna=True)), step=1000, format='%d')
max_compensation = st.sidebar.number_input('Maximum Compensation ($)', min_value=0, max_value=int(data['compensation_max'].max(skipna=True)), step=1000, format='%d', value=int(data['compensation_max'].max(skipna=True)))

# Remote filter
remote_options = ['All', 'Yes', 'No', 'Unknown']
selected_remote = st.sidebar.selectbox('Remote?', remote_options)

# Apply filters
if selected_remote != 'All':
    data = data[data['remote'].str.lower() == selected_remote.lower()]

if not include_no_comp:
    data = data.dropna(subset=['compensation_min', 'compensation_max'])
    data = data[(data['compensation_min'] >= min_compensation) & (data['compensation_max'] <= max_compensation)]
else:
    mask = (data['compensation_min'] >= min_compensation) & (data['compensation_max'] <= max_compensation) | data['compensation_min'].isna() | data['compensation_max'].isna()
    data = data[mask]

for column in data.columns.drop(['compensation_min', 'compensation_max', 'remote', 'link to appy']):
    unique_values = data[column].dropna().unique()
    selected_values = st.sidebar.multiselect(f'Filter by {column}', unique_values)
    if selected_values:
        data = data[data[column].isin(selected_values)]

# Display the filtered DataFrame without the 'link to appy'
st.write(data.drop(columns=['link to appy']))

# New Section for Job Applications
st.header("Apply to Selected Jobs")
apply_data = data[['job_title', 'company', 'link to appy']].drop_duplicates()
for _, row in apply_data.iterrows():
    st.markdown(f"**{row['job_title']}** at **{row['company']}**")
    st.markdown(f"[Apply Here]({row['link to appy']})")
