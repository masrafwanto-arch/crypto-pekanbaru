import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("Crypto Pekanbaru Pro - Live 24 Jam")

SHEET_ID = "1aohdkcqgfhl16EANAh979m6oKjbmZrxHPH8EbRs1To4Q"
# Pakai link export yang lebih stabil
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1489387325"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL, header=None)
    df = df.dropna(how='all')
    # Ambil 4 kolom pertama aja
    df = df.iloc[:, :4]
    df.columns = ["Waktu", "Koin", "IDR", "USD"]
    df = df[df["Koin"].astype(str).str.contains("BITCOIN|ETHEREUM|SOLANA", na=False)]
    df["Waktu"] = pd.to_datetime(df["Waktu"], dayfirst=True, errors='coerce')
    return df.dropna(subset=["Waktu"])

try:
    df = load_data()
    st.metric("Total Data", len(df), f"Update: {df['Waktu'].max()}")
    koin = st.selectbox("Pilih Koin", ["BITCOIN", "ETHEREUM", "SOLANA"])
    fdf = df[df["Koin"] == koin]
    st.line_chart(fdf.set_index("Waktu")[["IDR"]])
    st.dataframe(fdf.tail(20), use_container_width=True)
except Exception as e:
    st.error(f"Sheet belum di-Share Public. Klik Share > Anyone with link. Error: {e}")
