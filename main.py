import streamlit as st
import pandas as pd


# load csv (;) into df
# @st.cache_data
def load_data():
    df = pd.read_csv("lorem_data.csv", sep=';')
    return df

data = load_data()


st.dataframe(data, hide_index=True, use_container_width=True)