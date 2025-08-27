import streamlit as st
import requests
import json
import pandas as pd

# Base URL dari API Flask Anda
BASE_URL = "http://127.0.0.1:5000/api"

st.set_page_config(layout="wide")
st.title("🧪 Dashboard Pengujian API HealthLinkr (Flask) untuk tugasnya Uqi")

# --- Sidebar untuk Navigasi ---
st.sidebar.header("Pilih Endpoint")
menu = st.sidebar.selectbox(
    "Pilih API yang ingin diuji:",
    ["Authentication & User", "Service Management", "Appointment Management"]
)

# BRIEF 1: AUTHENTICATION & USER
if menu == "Authentication & User":
    st.header("Authentication & Authorization")

    # --- SIGNUP ---
    with st.expander("🚀 POST /api/signup/"):
        st.subheader("Registrasi User Baru")
        with st.form("signup_form"):
            signup_username = st.text_input("Username")
            signup_email = st.text_input("Email")
            signup_password = st.text_input("Password", type="password")
            signup_role = st.selectbox("Role", ["patient", "doctor", "administrator"])
            submitted = st.form_submit_button("Daftar")

            if submitted:
                payload = {
                    "username": signup_username,
                    "email": signup_email,
                    "password": signup_password,
                    "role": signup_role
                }
                try:
                    response = requests.post(f"{BASE_URL}/signup/", json=payload)
                    st.write("Status Code:", response.status_code)
                    st.json(response.json())
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Koneksi Gagal: Pastikan API Flask (app.py) sudah berjalan. Detail: {e}")


    # --- LOGIN ---
    with st.expander("🔑 GET /api/login/"):
        st.subheader("Login User")
        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            login_submitted = st.form_submit_button("Login")

            if login_submitted:
                params = {"username": login_username, "password": login_password}
                try:
                    response = requests.get(f"{BASE_URL}/login/", params=params)
                    st.write("Status Code:", response.status_code)
                    st.json(response.json())
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Koneksi Gagal: Pastikan API Flask (app.py) sudah berjalan. Detail: {e}")

    # --- GET USER DETAIL ---
    with st.expander("👤 GET /api/user/{user_id}/"):
        st.subheader("Lihat Detail User")
        user_id_to_get = st.number_input("Masukkan ID User", min_value=1, step=1)
        if st.button("Cari User"):
            try:
                response = requests.get(f"{BASE_URL}/user/{user_id_to_get}/")
                st.write("Status Code:", response.status_code)
                st.json(response.json())
            except requests.exceptions.ConnectionError as e:
                st.error(f"Koneksi Gagal: Pastikan API Flask (app.py) sudah berjalan. Detail: {e}")


# BRIEF 2: SERVICE MANAGEMENT

elif menu == "Service Management":
    st.header("Service Management")
    with st.expander("🩺 GET /api/services/"):
        st.subheader("Tampilkan Semua Layanan Medis")
        if st.button("Ambil Data Layanan"):
            try:
                response = requests.get(f"{BASE_URL}/services/")
                st.write("Status Code:", response.status_code)
                # Tampilkan dalam bentuk tabel yang lebih rapi
                df = pd.DataFrame(response.json())
                st.dataframe(df)
            except requests.exceptions.ConnectionError as e:
                st.error(f"Koneksi Gagal: Pastikan API Flask (app.py) sudah berjalan. Detail: {e}")
            except json.JSONDecodeError:
                 st.warning("Gagal mem-parsing JSON. Mungkin endpoint belum diimplementasikan di app.py?")



# BRIEF 3: APPOINTMENT MANAGEMENT

elif menu == "Appointment Management":
    st.header("Appointment Management")
    
    # --- GET ALL APPOINTMENTS ---
    with st.expander("🗓️ GET /api/appointments/"):
        st.subheader("Tampilkan Semua Appointments")
        if st.button("Ambil Data Appointment"):
            try:
                response = requests.get(f"{BASE_URL}/appointments/")
                st.write("Status Code:", response.status_code)
                df = pd.DataFrame(response.json())
                st.dataframe(df)
            except requests.exceptions.ConnectionError as e:
                st.error(f"Koneksi Gagal: Pastikan API Flask (app.py) sudah berjalan. Detail: {e}")

    # --- CANCEL APPOINTMENT ---
    with st.expander("❌ POST /api/appointments/{id}/cancel/"):
        st.subheader("Batalkan Appointment")
        appointment_id_to_cancel = st.number_input("Masukkan ID Appointment", min_value=1, step=1, key="cancel_id")
        if st.button("Batalkan Appointment"):
            try:
                response = requests.post(f"{BASE_URL}/appointments/{appointment_id_to_cancel}/cancel/")
                st.write("Status Code:", response.status_code)
                st.json(response.json())
            except requests.exceptions.ConnectionError as e:
                st.error(f"Koneksi Gagal: Pastikan API Flask (app.py) sudah berjalan. Detail: {e}")