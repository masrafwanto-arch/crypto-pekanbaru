import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Final", layout="wide")
st.title("📈 Crypto Pekanbaru - LAPORAN FINAL 24 JAM")
st.caption("Trigger OFF di 19:41 WIB - Data Final 26-27 Sep 2026")

# --- GANTI ID SHEET LU DI SINI ---
# Buka Google Sheet lu, link nya kayak gini:
# https://docs.google.com/spreadsheets/d/1AbCdEfGh123456/edit
# Copy yang 1AbCdEfGh123456 itu
SHEET_ID = "1AbCdEfGh123456" # <-- GANTI INI
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=GRAFIK"

st.write("Membaca data...")
try:
    df = pd.read_csv(URL)
    st.success(f"Total data final: {len(df)} baris - Berhenti 19:41")
    st.dataframe(df.tail(20), use_container_width=True)

    # Bersihin Harga jadi angka
    df['Harga_num'] = df['Harga IDR'].astype(str).str.replace('Rp','').str.replace(',','').str.replace('.','')
    df['Harga_num'] = pd.to_numeric(df['Harga_num'], errors='coerce')

    st.line_chart(df, x="Waktu", y="Harga_num", color="Koin")

    # --- AI RINGKASAN PASTI MUNCUL ---
    st.divider()
    st.subheader("🤖 AI Ringkasan Otomatis 24 Jam - FINAL")
    for koin in df['Koin'].unique():
        d = df[df['Koin']==koin].dropna(subset=['Harga_num'])
        if len(d) > 1:
            awal = d.iloc[0]['Harga_num']
            akhir = d.iloc[-1]['Harga_num']
            persen = (akhir-awal)/awal*100 if awal!=0 else 0
            high = d['Harga_num'].max()
            low = d['Harga_num'].min()
            st.success(f"**{koin}** {'NAIK 🟢' if persen>0 else 'TURUN 🔴'} {persen:.2f}% | Awal Rp{awal:,.0f} -> Akhir Rp{akhir:,.0f} | High Rp{high:,.0f} | Low Rp{low:,.0f}")

except Exception as e:
    st.error(f"Gagal: {e}")
    st.warning("Pastikan Sheet di Share -> Anyone with link -> Viewer, dan SHEET_ID sudah diganti")
