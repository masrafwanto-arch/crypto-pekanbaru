import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("📈 LIVE CRYPTO - Pekanbaru")
st.caption("Data LIVE dari Google Sheet: data test gspread")

try:
    # FIX UTAMA: Benerin \n jadi enter beneran biar gak error base64 129
    creds_dict = dict(st.secrets["gspread_creds"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open('data test gspread').sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if len(df) > 0:
        st.success(f"✅ Bot Aktif - {len(df)} data - Update: {df.iloc[-1]['Waktu']}")
        st.dataframe(df.sort_values('Waktu', ascending=False).head(100), use_container_width=True)

        df['Waktu'] = pd.to_datetime(df['Waktu'], errors='coerce')
        for koin in df['Koin'].unique():
            st.subheader(f"Grafik {koin}")
            d = df[df['Koin']==koin].sort_values('Waktu')
            # Ambil kolom harga otomatis (kolom ke-3)
            price_col = df.columns[2]
            st.line_chart(d.set_index('Waktu')[price_col])
    else:
        st.warning("Sheet kosong - cek bot python kamu jalan gak?")
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Cek Secrets di Streamlit sudah bener belum")
