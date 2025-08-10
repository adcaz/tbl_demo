import streamlit as st
import pandas as pd
from utils.filters import Filters

st.set_page_config(page_title="Public Source Page", layout="wide")


@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv("sample_data.csv", sep=';')
    return df


# Initialize Filters class with dataset and columns to filter
filter_columns = ["Category", "Subcategory", "Supplier", "Region"]
filters = Filters(dataset=load_data(), filter_columns=filter_columns)

# Display filters
filters.display_filters(columns_per_row=5)

# Get filtered data
filtered_data = filters.get_filtered_data()

# Display filtered data
st.dataframe(filtered_data, hide_index=True)