import streamlit as st
import pandas as pd
import gspread
from utils.filters import Filters
from utils.require_password import require_password

st.set_page_config(page_title="Protected User Page", layout="wide")

if not require_password(role="admin"):
    st.stop()

# Load data from Google Sheets
@st.cache_data(ttl=300, show_time=True)
def load_gsheet():
    gc = gspread.service_account_from_dict(st.secrets["gspread_creds"])
    sh = gc.open("gsheet_lorem_data")
    data = sh.sheet1.get_all_records()
    filters = sh.worksheet("filtres").get_all_records()
    return pd.DataFrame(data), pd.DataFrame(filters)

def update_gsheet(data_df, filters_df):
    gc = gspread.service_account_from_dict(st.secrets["gspread_creds"])
    sh = gc.open("gsheet_lorem_data")
    sh.sheet1.clear()
    sh.sheet1.update([data_df.columns.values.tolist()] + data_df.values.tolist())
    sh.worksheet("filtres").clear()
    sh.worksheet("filtres").update([filters_df.columns.values.tolist()] + filters_df.values.tolist())

data, filters = load_gsheet()

# Add or remove filters
filter_columns = st.multiselect(
    "Sélectionner les colonnes qui pourront être filtrées",
    options=data.columns.tolist(),
    default=filters
)

# Initialize Filters class with dataset and columns to filter
filters = Filters(dataset=data, filter_columns=filter_columns)

# Display filters
filters.display_filters(columns_per_row=5)

# Get filtered data
filtered_data = filters.get_filtered_data()
# Display filtered data
updated_data = st.data_editor(filtered_data, hide_index=True, use_container_width=True, num_rows="dynamic", key="filtered_data_editor")

# Save changes to Google Sheets
if st.button("Enregistrer les modifications"):
    with st.spinner("Enregistrement des modifications...", show_time=True):
        update_gsheet(updated_data, pd.DataFrame(filter_columns, columns=["Filtres"]))
        st.cache_data.clear()  # Clear cache to ensure fresh data is loaded next time
    st.success("Modifications enregistrées avec succès.")