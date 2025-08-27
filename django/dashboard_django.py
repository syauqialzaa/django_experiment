import streamlit as st
import requests
import json
import pandas as pd

BASE_URL = "http://127.0.0.1:8000/api"

st.set_page_config(layout="wide")
st.title("🧪 Dashboard API HealthLinkr (Django) untuk tugasnya Uqi")

# --- Sidebar untuk Navigasi ---
st.sidebar.header("Pilih Endpoint")
menu = st.sidebar.selectbox(
    "Pilih API yang ingin diuji:",
    ["Authentication & User", "Service Management", "Appointment Management"]
)


# BRIEF 1: AUTHENTICATION & USER
if menu == "Authentication & User":
    st.header("Brief 1: Authentication & Authorization")

    col1, col2 = st.columns(2)

    with col1:
        # --- SIGNUP ---
        with st.expander("🚀 POST /api/signup/", expanded=True):
            st.subheader("Registrasi User Baru")
            with st.form("signup_form"):
                signup_username = st.text_input("Username")
                signup_email = st.text_input("Email")
                signup_password = st.text_input("Password", type="password")
                signup_role = st.selectbox("Role", ["patient", "doctor", "administrator"])
                submitted = st.form_submit_button("Daftar")

                if submitted:
                    with st.spinner("Mengirim data..."):
                        payload = { "username": signup_username, "email": signup_email, "password": signup_password, "role": signup_role }
                        try:
                            response = requests.post(f"{BASE_URL}/signup/", json=payload)
                            st.write("Status Code:", response.status_code)
                            st.json(response.json())
                        except requests.exceptions.ConnectionError:
                            st.error("Koneksi Gagal: Pastikan server Django (manage.py runserver) sudah berjalan.")

        # --- LOGIN ---
        with st.expander("🔑 GET /api/login/", expanded=True):
            st.subheader("Login User")
            with st.form("login_form"):
                login_username = st.text_input("Username", key="login_user")
                login_password = st.text_input("Password", type="password", key="login_pass")
                login_submitted = st.form_submit_button("Login")

                if login_submitted:
                     with st.spinner("Mencoba login..."):
                        params = {"username": login_username, "password": login_password}
                        try:
                            response = requests.get(f"{BASE_URL}/login/", params=params)
                            st.write("Status Code:", response.status_code)
                            st.json(response.json())
                        except requests.exceptions.ConnectionError:
                            st.error("Koneksi Gagal: Pastikan server Django sudah berjalan.")
    
    with col2:
        # --- GET, PUT, DELETE USER ---
        with st.expander("👤 Operasi User (GET, PUT, DELETE)", expanded=True):
            st.subheader("Cari, Update, atau Hapus User")
            user_id_op = st.number_input("Masukkan ID User", min_value=1, step=1)

            # GET
            if st.button("Cari User (GET)"):
                with st.spinner(f"Mencari user ID: {user_id_op}..."):
                    try:
                        response = requests.get(f"{BASE_URL}/user/{user_id_op}/")
                        st.write("Status Code:", response.status_code)
                        st.json(response.json())
                    except requests.exceptions.ConnectionError:
                        st.error("Koneksi Gagal: Pastikan server Django sudah berjalan.")
            
            st.markdown("---")
            # PUT (Update)
            st.write("Untuk Update:")
            update_username = st.text_input("Username Baru (opsional)", key="update_user")
            update_email = st.text_input("Email Baru (opsional)", key="update_email")
            if st.button("Update User (PUT)"):
                 with st.spinner(f"Mengupdate user ID: {user_id_op}..."):
                    payload = {}
                    if update_username:
                        payload['username'] = update_username
                    if update_email:
                        payload['email'] = update_email
                    
                    if not payload:
                        st.warning("Tidak ada data untuk diupdate. Isi salah satu field.")
                    else:
                        try:
                            response = requests.put(f"{BASE_URL}/user/{user_id_op}/update", json=payload)
                            st.write("Status Code:", response.status_code)
                            st.json(response.json())
                        except requests.exceptions.ConnectionError:
                            st.error("Koneksi Gagal: Pastikan server Django sudah berjalan.")

            st.markdown("---")
            # DELETE
            st.write("Untuk Hapus:")
            if st.button("Hapus User (DELETE)", type="primary"):
                 with st.spinner(f"Menghapus user ID: {user_id_op}..."):
                    try:
                        response = requests.delete(f"{BASE_URL}/user/{user_id_op}/update")
                        st.write("Status Code:", response.status_code)
                        if response.status_code == 204:
                            st.success(f"User dengan ID {user_id_op} berhasil dihapus.")
                        else:
                            st.json(response.json())
                    except requests.exceptions.ConnectionError:
                        st.error("Koneksi Gagal: Pastikan server Django sudah berjalan.")


# BRIEF 2: SERVICE MANAGEMENT
elif menu == "Service Management":
    st.header("Brief 2: Service Management")
    with st.expander("🩺 GET /api/services/", expanded=True):
        st.subheader("Tampilkan Semua Layanan Medis")
        if st.button("Ambil Data Layanan"):
            with st.spinner("Mengambil data..."):
                try:
                    response = requests.get(f"{BASE_URL}/services/")
                    st.write("Status Code:", response.status_code)
                    df = pd.DataFrame(response.json())
                    st.dataframe(df, use_container_width=True)
                except requests.exceptions.ConnectionError:
                    st.error("Koneksi Gagal: Pastikan server Django sudah berjalan.")
                except json.JSONDecodeError:
                     st.warning("Gagal mem-parsing JSON. Mungkin endpoint belum diimplementasikan di `api/views.py`?")


# BRIEF 3: APPOINTMENT MANAGEMENT
elif menu == "Appointment Management":
    st.header("Brief 3: Appointment Management")
    
    with st.expander("🗓️ GET /api/appointments/", expanded=True):
        st.subheader("Tampilkan Semua Appointments")
        if st.button("Ambil Data Appointment"):
             with st.spinner("Mengambil data..."):
                try:
                    response = requests.get(f"{BASE_URL}/appointments/")
                    st.write("Status Code:", response.status_code)
                    df = pd.DataFrame(response.json())
                    st.dataframe(df, use_container_width=True)
                except requests.exceptions.ConnectionError:
                    st.error("Koneksi Gagal: Pastikan server Django sudah berjalan.")