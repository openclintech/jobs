import streamlit as st
import pandas as pd

def load_data(filepath):
    data = pd.read_csv(filepath, delimiter='\t')
    data['compensation_min'] = pd.to_numeric(data['compensation_min'].replace('[\$,]', '', regex=True), errors='coerce')
    data['compensation_max'] = pd.to_numeric(data['compensation_max'].replace('[\$,]', '', regex=True), errors='coerce')
    return data

def filter_data(data, remote_only, include_no_comp, min_comp, max_comp, keywords, companies, cities, states):
    # Filter by remote status if selected
    if remote_only:
        data = data[(data['remote'] == 'yes') | (data['remote'] == 'hybrid')]
    
    # Apply keyword search for job title
    if keywords:
        data = data[data['job_title'].str.lower().str.contains(keywords.lower())]
    
    # Filter by company, city, and state if selections are made
    if companies:
        data = data[data['company'].isin(companies)]
    if cities:
        data = data[data['city'].isin(cities)]
    if states:
        data = data[data['state'].isin(states)]
    
    # Handle compensation filters
    if not include_no_comp:
        # Only include jobs with specified compensation details within the selected range
        data = data.dropna(subset=['compensation_min', 'compensation_max'])
        data = data[(data['compensation_min'] >= min_comp) & (data['compensation_max'] <= max_comp)]
    else:
        # Include all jobs, but still apply compensation range to those with available details
        condition = (data['compensation_min'] >= min_comp) & (data['compensation_max'] <= max_comp) | data['compensation_min'].isna() | data['compensation_max'].isna()
        data = data[condition]

    return data

def main():
    data = load_data('jobs.csv')
    remote_only = st.sidebar.checkbox('Remote only', False)
    include_no_comp = st.sidebar.checkbox('Include jobs without compensation details', True)
    compensation_range = st.sidebar.slider('Compensation Range ($)', int(data['compensation_min'].min(skipna=True, default=0)), int(data['compensation_max'].max(skipna=True)), (75000, int(data['compensation_max'].max(skipna=True))), 1000, '%d')
    job_title_keyword = st.sidebar.text_input('Job Title Keyword Search')
    selected_company = st.sidebar.multiselect('Company', data['company'].dropna().unique())
    selected_city = st.sidebar.multiselect('City', data['city'].dropna().unique())
    selected_state = st.sidebar.multiselect('State', data['state'].dropna().unique())

    filtered_data = filter_data(data, remote_only, include_no_comp, *compensation_range, job_title_keyword, selected_company, selected_city, selected_state)
    st.write(filtered_data)

if __name__ == "__main__":
    main()
