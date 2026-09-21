import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("📈 LIVE CRYPTO - Pekanbaru")
st.caption("Data LIVE dari Google Sheet: data test gspread")

# Auto refresh tiap 30 detik
st_autorefresh = st.empty()
if st.button("🔄 Refresh Sekarang"):
    st.cache_data.clear()

@st.cache_data(ttl=30) # cache cuma 30 detik aja
def load_data():
    creds_dict = dict(st.secrets["gspread_creds"])
    if "\\n" in creds_dict["private_key"]:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)

    # Coba baca dari GRAFIK dulu, kalo gagal baru Sheet1 (soalnya data barumu ada di GRAFIK)
    try:
        sheet = client.open('data test gspread').worksheet('GRAFIK')
    except:
        sheet = client.open('data test gspread').worksheet('Sheet1')

    data = sheet.get_all_values()
    # Bersihin header kalau ada
    df = pd.DataFrame(data[1:], columns=data[0] if "Waktu" in data[0][0] else ["Waktu","Koin","Harga_Rp","Harga_USD"])
    return df

try:
    df = load_data()
    # Convert jam ke WIB
    df['Waktu'] = pd.to_datetime(df['Waktu'], errors='coerce')

    latest = df.sort_values('Waktu', ascending=False).iloc[0]
    # Ubah ke WIB
    wib = pytz.timezone('Asia/Jakarta')

    st.success(f"✅ Bot Aktif - {len(df)} data - Update: {latest['Waktu']} WIB")
    st.dataframe(df.sort_values('Waktu', ascending=False).head(100), use_container_width=True)

    st.info(f"Data terakhir di Sheet: {df['Waktu'].max()} | Sekarang: {datetime.now(wib).strftime('%Y-%m-%d %H:%M:%S WIB')}")

except Exception as e:
    st.error(f"Error: {e}")
