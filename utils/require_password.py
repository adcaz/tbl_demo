import streamlit as st
import time, bcrypt

hash_user = st.secrets.auth.user.encode()
hash_admin = st.secrets.auth.admin.encode()
ttl = st.secrets.auth.ttl * 3600

def require_password(role: str = "user") -> bool:
    ss = st.session_state
    now = time.time()
    ss.setdefault("authed_until", 0.0)
    ss.setdefault("attempts", 0)
    ss.setdefault("lock_until", 0.0)
    ss.setdefault("role", role)

    # Already signed in?
    if now < ss["authed_until"] and (ss["role"] == "admin" or ss["role"] ==  role):
        with st.sidebar:
            if ss["role"] == "user":
                st.markdown("**Connecté en tant qu'utilisateur**")
            elif ss["role"] == "admin":
                st.markdown("**Connecté en tant qu'administrateur**")
            if st.button("Déconnexion"):
                ss.clear()
                st.rerun()
        return True

    # Throttle brute force
    if now < ss["lock_until"]:
        wait = int(ss["lock_until"] - now)
        st.error(f"Trop de tentatives. Essaye à nouveau dans {wait}s.")
        return False

    # Login form
    with st.form("login", clear_on_submit=True):
        pwd = st.text_input("Saisi le mot de passe", type="password")
        ok = st.form_submit_button("Connexion")

    if ok:
        hash = hash_user if role == "user" else hash_admin
        valid = pwd and bcrypt.checkpw(pwd.encode(), hash)
        if valid:
            ss["authed_until"] = now + ttl
            ss["attempts"] = 0
            ss["role"] = role
            st.rerun()
        else:
            ss["attempts"] += 1
            st.error("Mot de passe incorrect.")
            if ss["attempts"] >= 5:
                ss["lock_until"] = now + 60  # 60s lockout

    return False
