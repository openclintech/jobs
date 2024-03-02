import streamlit as st
import pandas as pd

@st.cache
def load_data(filepath):
    data = pd.read_csv(filepath)
    data['compensation_min'] = pd.to_numeric(data['compensation_min'].replace('[\$,]', '', regex=True), errors='coerce')
    data['compensation_max'] = pd.to_numeric(data['compensation_max'].replace('[\$,]', '', regex=True), errors='coerce')
    return data

def filter_data(data, remote_only, include_no_comp, min_comp, max_comp, keywords, companies, cities, states):
    filtered = data
    if remote_only:
        filtered = filtered[filtered['remote'].isin(['yes', 'hybrid'])]
    if not include_no_comp:
        filtered = filtered.dropna(subset=['compensation_min', 'compensation_max'])
    filtered = filtered[(filtered['compensation_min'] >= min_comp) & (filtered['compensation_max'] <= max_comp)]
    if keywords:
        filtered = filtered[filtered['job_title'].str.lower().str.contains(keywords.lower())]
    if companies:
        filtered = filtered[filtered['company'].isin(companies)]
    if cities:
        filtered = filtered[filtered['city'].isin(cities)]
    if states:
        filtered = filtered[filtered['state'].isin(states)]
    return filtered

def display_applications(filtered_data):
    st.header("Apply to Selected Jobs")
    if not filtered_data.empty:
        for i, row in filtered_data.iterrows():
            job_info = f"{i+1}. **{row['job_title']}** at **{row['company']}** - [Apply Here]({row['link to appy']})"
            st.markdown(job_info)
    else:
        st.write("No job listings match your filters.")

def main():
    data = load_data('jobs.csv')
    remote_only = st.sidebar.checkbox('Remote only', False)
    include_no_comp = st.sidebar.checkbox('Include jobs without compensation details', True)
    compensation_range = st.sidebar.slider('Compensation Range ($)', int(data['compensation_min'].min(skipna=True)), int(data['compensation_max'].max(skipna=True)), (75000, int(data['compensation_max'].max(skipna=True))), 1000, '%d')
    job_title_keyword = st.sidebar.text_input('Job Title Keyword Search')
    selected_company = st.sidebar.multiselect('Company', data['company'].unique())
    selected_city = st.sidebar.multiselect('City', data['city'].unique())
    selected_state = st.sidebar.multiselect('State', data['state'].unique())

    filtered_data = filter_data(data, remote_only, include_no_comp, *compensation_range, job_title_keyword, selected_company, selected_city, selected_state)
    # Display filtered DataFrame without 'link to appy' for the main data view
    st.write(filtered_data.drop(columns=['link to appy']))
    # Use the filtered data with 'link to appy' for application links
    display_applications(filtered_data)

if __name__ == "__main__":
    main()
