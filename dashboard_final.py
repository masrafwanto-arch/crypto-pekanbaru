import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("📈 LIVE CRYPTO - Pekanbaru")
st.caption("Data LIVE dari Google Sheet: data test gspread")

SHEET_ID = "1aohdkcqfhl16EANAh979m6oKjbmZrxHPH8EbRs1To4Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL, header=None)
    df.columns = ["Waktu", "Koin", "Harga_Rp", "Harga_USD"]
    return df

try:
    df = load_data()
    st.success(f"✅ Bot Aktif - {len(df)} data - Update: {df.iloc[-1]['Waktu']}")
    st.dataframe(df.sort_values('Waktu', ascending=False).head(100), use_container_width=True)
    
    # Grafik per koin
    df['Waktu'] = pd.to_datetime(df['Waktu'], errors='coerce')
    for koin in df['Koin'].unique():
        st.subheader(f"Grafik {koin}")
        d = df[df['Koin']==koin].sort_values('Waktu')
        st.line_chart(d.set_index('Waktu')['Harga_Rp'])
        
    st.caption(f"Auto-refresh 60 detik | Sheet: {SHEET_ID}")
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Pastikan kamu sudah klik Bagikan -> Anyone with the link -> Viewer")
