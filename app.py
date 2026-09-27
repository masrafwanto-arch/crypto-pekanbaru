import streamlit as st
import pandas as pd

st.title("📈 Crypto Pekanbaru - FINAL")
st.write("Jika ini muncul, ringkasan di bawah HARUS muncul")

# DATA DUMMY TEST - NANTI KITA GANTI BALIK KE SHEET
data = [
    {"Waktu":"26 Sep 19:00","Koin":"BTC","Harga IDR":1700000000},
    {"Waktu":"27 Sep 19:41","Koin":"BTC","Harga IDR":1720000000},
    {"Waktu":"26 Sep 19:00","Koin":"ETH","Harga IDR":50000000},
    {"Waktu":"27 Sep 19:41","Koin":"ETH","Harga IDR":49000000},
]
df = pd.DataFrame(data)

st.divider()
st.subheader("🤖 AI Ringkasan Otomatis 24 Jam")
for koin in df['Koin'].unique():
    d = df[df['Koin']==koin]
    awal = d.iloc[0]['Harga IDR']
    akhir = d.iloc[-1]['Harga IDR']
    persen = (akhir-awal)/awal*100
    st.success(f"**{koin}** {'NAIK 🟢' if persen>0 else 'TURUN 🔴'} {persen:.2f}% | Rp{awal:,.0f} -> Rp{akhir:,.0f}")

st.divider()
st.info("Kalau ringkasan dummy di atas muncul, berarti masalahnya cuma koneksi gspread. Abis ini aku benerin koneksi Sheet nya.")
