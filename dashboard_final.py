import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("📈 LIVE CRYPTO - Pekanbaru")
st.caption("Data LIVE dari Google Sheet: data test gspread")

if st.button("🔄 Refresh Sekarang"):
    st.cache_data.clear()

@st.cache_data(ttl=30)
def load_data():
    creds_dict = dict(st.secrets["gspread_creds"])
    if "\\n" in creds_dict["private_key"]:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    # Baca GRAFIK dulu (data barumu ada disitu), kalau gagal baca Sheet1
    try:
        sheet = client.open('data test gspread').worksheet('GRAFIK')
    except:
        sheet = client.open('data test gspread').sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

try:
    df = load_data()
    df['Waktu'] = pd.to_datetime(df['Waktu'], errors='coerce')
    df = df.dropna(subset=['Waktu'])

    wib = ZoneInfo("Asia/Jakarta")
    now_wib = datetime.now(wib).strftime("%Y-%m-%d %H:%M:%S WIB")
    latest = df.sort_values('Waktu', ascending=False).iloc[0]['Waktu']

    st.success(f"✅ Bot Aktif - {len(df)} data - Update terakhir: {latest} | Jam sekarang: {now_wib}")
    st.dataframe(df.sort_values('Waktu', ascending=False).head(100), use_container_width=True)

    # Grafik
    for koin in df['Koin'].unique():
        st.subheader(f"Grafik {koin}")
        d = df[df['Koin']==koin].sort_values('Waktu')
        st.line_chart(d.set_index('Waktu')['Harga_Rp' if 'Harga_Rp' in d.columns else d.columns[2]])

except Exception as e:
    st.error(f"Error: {e}")
