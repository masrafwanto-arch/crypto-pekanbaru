import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Final", layout="wide")
st.title("📈 Crypto Pekanbaru - LAPORAN FINAL 24 JAM")
st.caption("Trigger OFF di 19:41 WIB - Data Final 26-27 Sep 2026")

# ID SHEET LU UDAH AKU TEMPEL
SHEET_ID = "1aohdkcqfhl16EANAh979m6oKjbmZrxHPH8EbRs1To4Q"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=GRAFIK"

try:
    df = pd.read_csv(URL)
    st.success(f"✅ Data kebaca: {len(df)} baris - Berhenti jam 19:41")
    st.dataframe(df.tail(20), use_container_width=True)

    # Bersihin harga jadi angka biar bisa dihitung
    df['Harga_num'] = df['Harga IDR'].astype(str).str.replace('Rp','').str.replace(',','').str.replace('.','').str.replace(' ','')
    df['Harga_num'] = pd.to_numeric(df['Harga_num'], errors='coerce')
    df = df.dropna(subset=['Harga_num'])

    # Grafik
    st.subheader("📊 Grafik 24 Jam")
    st.line_chart(df, x="Waktu", y="Harga_num", color="Koin")

    # --- AI RINGKASAN PASTI MUNCUL DI SINI ---
    st.divider()
    st.subheader("🤖 AI Ringkasan Otomatis 24 Jam - FINAL")

    for koin in df['Koin'].unique():
        d = df[df['Koin']==koin]
        if len(d) > 1:
            awal = d.iloc[0]['Harga_num']
            akhir = d.iloc[-1]['Harga_num']
            persen = (akhir-awal)/awal*100 if awal!=0 else 0
            high = d['Harga_num'].max()
            low = d['Harga_num'].min()

            if persen > 0:
                st.success(f"**{koin}** NAIK 🟢 {persen:.2f}% | Awal Rp{awal:,.0f} -> Akhir Rp{akhir:,.0f} | Tertinggi Rp{high:,.0f} | Terendah Rp{low:,.0f}")
            else:
                st.error(f"**{koin}** TURUN 🔴 {persen:.2f}% | Awal Rp{awal:,.0f} -> Akhir Rp{akhir:,.0f} | Tertinggi Rp{high:,.0f} | Terendah Rp{low:,.0f}")

    st.divider()
    st.info("Projek 24 jam SELESAI. Data berhenti otomatis di 19:41 WIB.")

except Exception as e:
    st.error(f"Gagal baca Sheet: {e}")
    st.warning("WAJIB: Buka Google Sheet lu > Share > General Access > Anyone with the link > Viewer > Done")
