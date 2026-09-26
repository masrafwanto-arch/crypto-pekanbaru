import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("Crypto Pekanbaru Pro - Live 24 Jam")

SHEET_ID = "1aohdkcqgfhl16EANAh979m6oKjbmZrxHPH8EbRs1To4Q"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=GRAFIK"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL, header=None)
    df.columns = ["Waktu", "Koin", "IDR", "USD"]
    df = df.dropna(subset=["Koin"])
    df["Waktu"] = pd.to_datetime(df["Waktu"], dayfirst=True, errors='coerce')
    return df.dropna(subset=["Waktu"])

df = load_data()
st.metric("Total Data", len(df), f"Update terakhir: {df['Waktu'].max()}")

koin = st.selectbox("Pilih Koin", ["BITCOIN", "ETHEREUM", "SOLANA"])
fdf = df[df["Koin"] == koin]

st.line_chart(fdf.set_index("Waktu")[["IDR"]])
st.dataframe(fdf.tail(10), use_container_width=True)