import streamlit as st
import pandas as pd

# kalau lu udah pake gspread, biarin aja koneksinya yang lama
# ini aku pake df yang udah ada dari kode lu sebelumnya

# --- AI RINGKASAN 24 JAM - VERSI FIX ---
st.divider()
st.subheader("🤖 AI Ringkasan Otomatis 24 Jam")

# Pastikan df lu ada ya, dari kode atas lu
# df punya kolom: Waktu, Koin, Harga IDR

for koin in df['Koin'].unique():
    d = df[df['Koin'] == koin].copy()
    # urutin dari lama ke baru biar awal - akhir bener
    d = d.sort_values('Waktu')

    if len(d) > 1:
        awal = float(d.iloc[0]['Harga IDR'])
        akhir = float(d.iloc[-1]['Harga IDR'])
        high = float(d['Harga IDR'].max())
        low = float(d['Harga IDR'].min())
        persen = ((akhir - awal) / awal * 100)

        status = "NAIK 🟢" if persen > 0 else "TURUN 🔴"

        st.success(f"**{koin} {status} {persen:.2f}%** | Awal: Rp{awal:,.0f} -> Akhir: Rp{akhir:,.0f} | Tertinggi: Rp{high:,.0f} | Terendah: Rp{low:,.0f}")
