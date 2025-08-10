import streamlit as st
import pandas as pd
import gspread
from utils.filters import Filters
from utils.require_password import require_password

st.set_page_config(page_title="Protected User Page", layout="wide")

if not require_password(role="user"):
    st.stop()

# Load data from Google Sheets
@st.cache_data(ttl=300, show_time=True)
def load_gsheet():
    gc = gspread.service_account_from_dict(st.secrets["gspread_creds"])
    sh = gc.open("gsheet_lorem_data")
    data = sh.sheet1.get_all_records()
    filters = sh.worksheet("filtres").get_all_records()
    return pd.DataFrame(data), pd.DataFrame(filters)

data, filters = load_gsheet()

# Initialize Filters class with dataset and columns to filter
filters = Filters(dataset=data, filter_columns=filters["Filtres"].tolist())

# Display filters
filters.display_filters(columns_per_row=5)

# Get filtered data
filtered_data = filters.get_filtered_data()

# Display filtered data
st.dataframe(filtered_data, hide_index=True)