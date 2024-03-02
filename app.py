import streamlit as st
import pandas as pd

# Load the CSV data into a DataFrame
def load_data():
    data = pd.read_csv('jobs.csv')
    # Convert compensation columns to numeric, removing any non-numeric characters
    data['compensation_min'] = pd.to_numeric(data['compensation_min'].replace('[\$,]', '', regex=True), errors='coerce')
    data['compensation_max'] = pd.to_numeric(data['compensation_max'].replace('[\$,]', '', regex=True), errors='coerce')
    return data

data = load_data()

st.sidebar.header('Filter options')

# New "Remote only" checkbox
remote_only = st.sidebar.checkbox('Remote only', False)

include_no_comp = st.sidebar.checkbox('Include jobs without compensation details', True)

# Compensation range slider
compensation_range = st.sidebar.slider(
    'Compensation Range ($)',
    min_value=int(data['compensation_min'].min(skipna=True)),
    max_value=int(data['compensation_max'].max(skipna=True)),
    value=(75000, int(data['compensation_max'].max(skipna=True))),
    step=1000,
    format='%d'
)
min_compensation, max_compensation = compensation_range

# Keyword search for "Job Title"
job_title_keyword = st.sidebar.text_input('Job Title Keyword Search').lower()

# Apply the "Remote only" filter
if remote_only:
    data = data[data['remote'].isin(['yes', 'hybrid'])]

# Apply compensation filters
if not include_no_comp:
    data = data.dropna(subset=['compensation_min', 'compensation_max'])
    data = data[(data['compensation_min'] >= min_compensation) & (data['compensation_max'] <= max_compensation)]
else:
    mask = (data['compensation_min'] >= min_compensation) & (data['compensation_max'] <= max_compensation) | data['compensation_min'].isna() | data['compensation_max'].isna()
    data = data[mask]

# Apply job title keyword search filter
if job_title_keyword:
    data = data[data['job_title'].str.lower().str.contains(job_title_keyword)]

# Display the filtered DataFrame without the 'link to appy'
st.write(data.drop(columns=['link to appy']))

# New Section for Job Applications
st.header("Apply to Selected Jobs")
apply_data = data[['job_title', 'company', 'link to appy']].drop_duplicates()

if not apply_data.empty:
    for i, row in enumerate(apply_data.iterrows(), start=1):
        job_info = f"{i}. **{row[1]['job_title']}** at **{row[1]['company']}** - [Apply Here]({row[1]['link to appy']})"
        st.markdown(job_info)
else:
    st.write("No job listings match your filters.")
