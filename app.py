import streamlit as st
import pandas as pd

def load_data(filepath):
    data = pd.read_csv(filepath)
    data['compensation_min'] = pd.to_numeric(data['compensation_min'].replace('[\$,]', '', regex=True), errors='coerce')
    data['compensation_max'] = pd.to_numeric(data['compensation_max'].replace('[\$,]', '', regex=True), errors='coerce')
    return data

def get_compensation_range(data, comp_details_only):
    if comp_details_only:
        min_value = int(data['compensation_min'].min(skipna=True))
        max_value = int(data['compensation_max'].max(skipna=True))
        min_compensation, max_compensation = st.sidebar.slider(
            'Compensation Range ($)', 
            min_value=min_value, 
            max_value=max_value, 
            value=(75000, max_value), 
            step=1000, 
            format='%d'
        )
    else:
        min_compensation, max_compensation = 0, int(data['compensation_max'].max(skipna=True))
    return min_compensation, max_compensation

def filter_data(data, remote_only, comp_details_only, min_comp, max_comp, keywords, companies, cities, states):
    if remote_only:
        data = data[(data['remote'] == 'yes') | (data['remote'] == 'hybrid')]
    if comp_details_only:
        data = data.dropna(subset=['compensation_min', 'compensation_max'])
        data = data[(data['compensation_min'] >= min_comp) & (data['compensation_max'] <= max_comp)]
    
    if keywords:
        data = data[data['job_title'].str.lower().str.contains(keywords.lower())]
    if companies:
        data = data[data['company'].isin(companies)]
    if cities:
        data = data[data['city'].isin(cities)]
    if states:
        data = data[data['state'].isin(states)]

    return data

def display_applications(data):
    st.header("Apply to Selected Jobs")
    if not data.empty:
        for i, row in data.iterrows():
            job_info = f"{i+1}. **{row['job_title']}** at **{row['company']}** - [Apply Here]({row['link to appy']})"
            st.markdown(job_info)
    else:
        st.write("No job listings match your filters.")

def main():
    data = load_data('jobs.csv')
    remote_only = st.sidebar.checkbox('Remote only', False)
    comp_details_only = st.sidebar.checkbox('Only jobs with compensation details', True)
    min_compensation, max_compensation = get_compensation_range(data, comp_details_only)
    
    job_title_keyword = st.sidebar.text_input('Job Title Keyword Search')
    selected_company = st.sidebar.multiselect('Company', data['company'].dropna().unique())
    selected_city = st.sidebar.multiselect('City', data['city'].dropna().unique())
    selected_state = st.sidebar.multiselect('State', data['state'].dropna().unique())

    filtered_data = filter_data(data, remote_only, comp_details_only, min_compensation, max_compensation, job_title_keyword, selected_company, selected_city, selected_state)
    st.write(filtered_data)

    display_applications(filtered_data)

if __name__ == "__main__":
    main()
