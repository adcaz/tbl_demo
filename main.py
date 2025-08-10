import streamlit as st


pg = st.navigation([
    st.Page("pages/public_source.py", title="Données publiques & statiques", icon=":material/public:"),
    st.Page("pages/protected_user.py", title="Lecture seulement", icon=":material/lock:"),
    st.Page("pages/protected_admin.py", title="Lecture et écriture", icon=":material/lock_open:"),
])

pg.run()