import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

st.set_page_config(page_title="Crypto Pekanbaru Pro", layout="wide")
st.title("📈 LIVE CRYPTO - Pekanbaru")
st.caption("Data LIVE dari Google Sheet: data test gspread")

try:
    creds_dict = dict(st.secrets["gspread_creds"])
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open('data test gspread').sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if len(df) > 0:
        st.success(f"✅ Bot Aktif - {len(df)} data - Update: {df.iloc[-1]['Waktu']}")
        st.dataframe(df.sort_values('Waktu', ascending=False).head(100), use_container_width=True)
        df['Waktu'] = pd.to_datetime(df['Waktu'])
        for koin in df['Koin'].unique():
            st.subheader(f"Grafik {koin}")
            d = df[df['Koin']==koin].sort_values('Waktu')
            st.line_chart(d.set_index('Waktu')[d.columns[2]])
    else:
        st.warning("Sheet kosong")
except Exception as e:
    st.error(f"Error: {e}")
