import streamlit as st
import pandas as pd

@st.cache
def load_data(filepath):
    data = pd.read_csv(filepath)
    data['compensation_min'] = pd.to_numeric(data['compensation_min'].replace('[\$,]', '', regex=True), errors='coerce')
    data['compensation_max'] = pd.to_numeric(data['compensation_max'].replace('[\$,]', '', regex=True), errors='coerce')
    return data.drop(columns=['link to appy'])  # Drop once if not needed for filtering

def filter_data(data, remote_only, include_no_comp, min_comp, max_comp, keywords, companies, cities, states):
    if remote_only:
        data = data[data['remote'].isin(['yes', 'hybrid'])]
    if not include_no_comp:
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
    include_no_comp = st.sidebar.checkbox('Include jobs without compensation details', True)
    compensation_range = st.sidebar.slider('Compensation Range ($)', 0, int(data['compensation_max'].max()), (75000, int(data['compensation_max'].max())), 1000, '%d')
    job_title_keyword = st.sidebar.text_input('Job Title Keyword Search')
    selected_company = st.sidebar.multiselect('Company', data['company'].unique())
    selected_city = st.sidebar.multiselect('City', data['city'].unique())
    selected_state = st.sidebar.multiselect('State', data['state'].unique())

    filtered_data = filter_data(data, remote_only, include_no_comp, *compensation_range, job_title_keyword, selected_company, selected_city, selected_state)
    st.write(filtered_data)
     display_applications(filtered_data)  # Uncomment and adjust if links are to be displayed

if __name__ == "__main__":
    main()
