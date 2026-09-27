import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Crypto Pekanbaru", layout="wide")
st.title("📈 Crypto Pekanbaru - Laporan Final 24 Jam")
st.caption("Data final berhenti di 19:41 | 26-27 Sep 2026")

# KONEKSI SHEET
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gspread"], scope)
client = gspread.authorize(creds)
sheet = client.open("data test gspread").worksheet("GRAFIK")
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.write(f"Total data: {len(df)} baris")
st.dataframe(df.tail(20))

# GRAFIK
if "Waktu" in df.columns:
    st.line_chart(df, x="Waktu", y="Harga IDR", color="Koin")

# --- AI RINGKASAN (PASTI MUNCUL) ---
st.divider()
st.subheader("🤖 AI Ringkasan Otomatis 24 Jam")

for koin in df['Koin'].unique():
    d = df[df['Koin'] == koin].copy()
    # ambil baris pertama dan terakhir
    awal = d.iloc[0]['Harga IDR']
    akhir = d.iloc[-1]['Harga IDR']

    # hapus Rp dan koma kalau ada, biar bisa dihitung
    def to_num(x):
        try:
            return float(str(x).replace("Rp","").replace(",","").replace(".",""))
        except:
            return float(x)

    # coba hitung persen
    try:
        awal_n = to_num(awal)
        akhir_n = to_num(akhir)
        high_n = df[df['Koin']==koin]['Harga IDR'].apply(to_num).max()
        low_n = df[df['Koin']==koin]['Harga IDR'].apply(to_num).min()
        persen = (akhir_n - awal_n) / awal_n * 100
        st.success(f"**{koin}** {'NAIK 🟢' if persen>0 else 'TURUN 🔴'} {persen:.2f}% | Awal Rp{awal_n:,.0f} -> Akhir Rp{akhir_n:,.0f} | High Rp{high_n:,.0f} | Low Rp{low_n:,.0f}")
    except Exception as e:
        st.warning(f"{koin}: Awal {awal} -> Akhir {akhir} (error hitung: {e})")
