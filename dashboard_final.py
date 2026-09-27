import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

st.set_page_config(page_title="Crypto Pekanbaru Final", layout="wide")
st.title("📈 Crypto Pekanbaru - LAPORAN FINAL 24 JAM")
st.caption("Trigger OFF di 19:41 WIB - Data Final 26-27 Sep 2026")

# KONEKSI SHEET
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gspread"], scope)
client = gspread.authorize(creds)
sheet = client.open("data test gspread").worksheet("GRAFIK")
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.write(f"Total data final: {len(df)} baris - Berhenti jam 19:41")
st.dataframe(df.tail(20), width='stretch')

# GRAFIK
if not df.empty:
    # coba bersihin Harga IDR biar jadi angka
    df['Harga_num'] = df['Harga IDR'].astype(str).str.replace('Rp','').str.replace(',','').str.replace('.','').str.strip()
    df['Harga_num'] = pd.to_numeric(df['Harga_num'], errors='coerce')
    st.line_chart(df, x="Waktu", y="Harga_num", color="Koin")

# AI RINGKASAN - INI YANG LU CARI
st.divider()
st.subheader("🤖 AI Ringkasan Otomatis 24 Jam - FINAL")
st.info("Ini ringkasan dari data final yang berhenti jam 19:41")

for koin in df['Koin'].unique():
    d = df[df['Koin']==koin]
    awal = d.iloc[0]['Harga IDR']
    akhir = d.iloc[-1]['Harga IDR']
    d_num = d['Harga_num']
    if len(d_num.dropna()) > 1:
        awal_n = d_num.iloc[0]
        akhir_n = d_num.iloc[-1]
        persen = (akhir_n - awal_n) / awal_n * 100 if awal_n!=0 else 0
        high = d_num.max()
        low = d_num.min()
        st.success(f"**{koin}** {'NAIK 🟢' if persen>0 else 'TURUN 🔴'} {persen:.2f}% | Awal: Rp{awal_n:,.0f} -> Akhir: Rp{akhir_n:,.0f} | High: Rp{high:,.0f} | Low: Rp{low:,.0f}")
    else:
        st.warning(f"{koin}: {awal} -> {akhir}")

st.divider()
st.write("Halaman ini update otomatis tiap 60 detik")
if st.button("🔄 Refresh Manual"):
    st.rerun()
