import streamlit as st
import pandas as pd

def load_data(filepath):
    data = pd.read_csv(filepath)
    data['compensation_min'] = pd.to_numeric(data['compensation_min'].replace('[\$,]', '', regex=True), errors='coerce')
    data['compensation_max'] = pd.to_numeric(data['compensation_max'].replace('[\$,]', '', regex=True), errors='coerce')
    return data

def main():
    data = load_data('jobs.csv')
    # Determine the range for the slider based on available data
    min_compensation_value = int(data['compensation_min'].min(skipna=True)) if not data['compensation_min'].isna().all() else 0
    max_compensation_value = int(data['compensation_max'].max(skipna=True)) if not data['compensation_max'].isna().all() else 100000  # Assuming a default max value if all are NaN
    
    remote_only = st.sidebar.checkbox('Remote only', False)
    include_no_comp = st.sidebar.checkbox('Include jobs without compensation details', True)
    compensation_range = st.sidebar.slider(
        'Compensation Range ($)',
        min_value=min_compensation_value,
        max_value=max_compensation_value,
        value=(75000, max_compensation_value),
        step=1000,
        format='%d'
    )
    job_title_keyword = st.sidebar.text_input('Job Title Keyword Search')
    selected_company = st.sidebar.multiselect('Company', data['company'].dropna().unique())
    selected_city = st.sidebar.multiselect('City', data['city'].dropna().unique())
    selected_state = st.sidebar.multiselect('State', data['state'].dropna().unique())

    # Assuming filter_data function handles the filtering based on the user input
    # and returns the filtered DataFrame.
    filtered_data = filter_data(data, remote_only, include_no_comp, *compensation_range, job_title_keyword, selected_company, selected_city, selected_state)
    st.write(filtered_data)

if __name__ == "__main__":
    main()
