import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Crypto Pekanbaru Live", layout="wide")
st.title("📈 Crypto Pekanbaru - Laporan 24 Jam")

# --- KONEK KE GOOGLE SHEET ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gspread"], scope)
client = gspread.authorize(creds)
sheet = client.open("data test gspread").worksheet("GRAFIK")
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Ubah kolom biar aman
df.columns = [c.lower() for c in df.columns]
# df harus ada kolom: timestamp, coin, idr

st.dataframe(df.tail(10))

# --- GRAFIK ---
st.line_chart(df, x="timestamp", y="idr", color="coin")

# --- AI RINGKASAN 24 JAM (FINAL) ---
st.divider()
st.subheader("🤖 AI Ringkasan Otomatis 24 Jam")

for koin in df['coin'].unique():
    d = df[df['coin'] == koin]
    if len(d) > 1:
        awal = float(d.iloc[0]['idr'])
        akhir = float(d.iloc[-1]['idr'])
        high = float(d['idr'].max())
        low = float(d['idr'].min())
        persen = ((akhir - awal) / awal * 100)

        status = "NAIK 🟢" if persen > 0 else "TURUN 🔴"

        st.success(f"**{koin} {status} {persen:.2f}%** | Mulai: Rp{awal:,.0f} -> Selesai: Rp{akhir:,.0f} | Tertinggi: Rp{high:,.0f} | Terendah: Rp{low:,.0f}")

st.caption("Data final 26-27 Sep 2026 | Trigger sudah dimatikan")
