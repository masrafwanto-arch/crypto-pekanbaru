import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("Crypto Pekanbaru Pro - Live 24 Jam")

SHEET_ID = "1aohdkcqgfhl16EANAh979m6oKjbmZrxHPH8EbRs1To4Q"
# FIX: pake nama sheet, bukan gid - ini anti 404
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=GRAFIK"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL, header=None)
    df = df.iloc[:, :4]
    df.columns = ["Waktu", "Koin", "IDR", "USD"]
    df = df[df["Koin"].astype(str).str.contains("BITCOIN|ETHEREUM|SOLANA", na=False)]
    df["Waktu"] = pd.to_datetime(df["Waktu"], dayfirst=True, errors='coerce')
    df["IDR"] = pd.to_numeric(df["IDR"], errors='coerce')
    return df.dropna(subset=["Waktu"])

df = load_data()
st.success(f"CONNECTED! Total data: {len(df)} | Update: {df['Waktu'].max()}")
koin = st.selectbox("Pilih Koin", ["BITCOIN", "ETHEREUM", "SOLANA"])
fdf = df[df["Koin"] == koin].sort_values("Waktu")
st.line_chart(fdf.set_index("Waktu")["IDR"])
st.dataframe(fdf.tail(20), use_container_width=True)
