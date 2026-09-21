import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("📈 LIVE CRYPTO - Pekanbaru")
st.caption("Data LIVE dari Google Sheet: data test gspread")

@st.cache_data(ttl=30)
def load_data():
    creds_dict = dict(st.secrets["gspread_creds"])
    if "\\n" in creds_dict["private_key"]:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open('data test gspread').worksheet('GRAFIK')
    except:
        sheet = client.open('data test gspread').sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# INI YANG BIKIN OTOMATIS UPDATE BUAT SEMUA ORANG - GAK PERLU KLIK REFRESH
@st.fragment(run_every=60)
def show_live():
    df = load_data()
    df['Waktu'] = pd.to_datetime(df['Waktu'], errors='coerce')
    df = df.dropna(subset=['Waktu'])
    df = df.sort_values('Waktu', ascending=False)

    wib = ZoneInfo("Asia/Jakarta")
    now_wib = datetime.now(wib).strftime("%Y-%m-%d %H:%M:%S WIB")
    latest = df.iloc[0]['Waktu']

    st.success(f"✅ LIVE - {len(df)} data | Update terakhir: {latest} | Jam: {now_wib} | Auto-update 60 detik")

    st.dataframe(df.head(100), use_container_width=True)

    for koin in df['Koin'].unique():
        st.subheader(f"Grafik {koin}")
        d = df[df['Koin']==koin].sort_values('Waktu')
        harga_col = 'Harga_IDR' if 'Harga_IDR' in d.columns else 'Harga_Rp' if 'Harga_Rp' in d.columns else d.columns[2]
        st.line_chart(d.sort_values('Waktu').set_index('Waktu')[harga_col])

show_live()

st.caption("Halaman ini update otomatis tiap 60 detik untuk semua viewer")
if st.button("🔄 Refresh Manual"):
    st.cache_data.clear()
    st.rerun()
