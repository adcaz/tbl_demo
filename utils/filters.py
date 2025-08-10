import streamlit as st
import pandas as pd

class Filters:
    def __init__(self, dataset: pd.DataFrame, filter_columns: list):
        """
        Initialize the Filters class.

        :param dataset: The dataset to filter.
        :param filter_columns: List of column names for which filters should be created.
        """
        self.dataset = dataset
        self.filter_columns = filter_columns
        self.session_keys = {col: f"filter_{col}_key" for col in filter_columns}

        # Initialize session state for each filter column
        for col in self.filter_columns:
            if self.session_keys[col] not in st.session_state:
                st.session_state[self.session_keys[col]] = col

    def display_filters(self, columns_per_row: int = 3):
        """
        Render the selectboxes in a grid pattern and a reset button.

        :param columns_per_row: Number of columns in the grid layout.
        """
        cols = st.columns(columns_per_row)

        for idx, col_name in enumerate(self.filter_columns):
            with cols[idx % columns_per_row]:
                options = [col_name] + sorted(self.get_filtered_data(ignore_filter=col_name)[col_name].unique().tolist())
                st.selectbox(
                    f"Filter {col_name}",
                    options=options,
                    index=options.index(st.session_state[self.session_keys[col_name]]),
                    key=self.session_keys[col_name],
                    label_visibility="collapsed"
                )

        # Add reset button in the last column
        with cols[-1]:
            if st.button("Réinitialiser les filtres"):
                for key in self.session_keys.values():
                    del st.session_state[key]
                st.rerun()

    def get_filtered_data(self, ignore_filter: str = None):
        """
        Return the filtered dataset based on the selected filters.

        :return: Filtered dataset.
        """
        filtered_data = self.dataset.copy()
        for col_name in self.filter_columns:
            if ignore_filter and col_name == ignore_filter:
                continue
            filter_value = st.session_state[self.session_keys[col_name]]
            if filter_value != col_name:
                filtered_data = filtered_data[filtered_data[col_name] == filter_value]
        return filtered_data
