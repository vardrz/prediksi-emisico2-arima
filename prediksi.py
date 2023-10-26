import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title='Aplikasi Prediksi Emisi CO2 Indonesia', layout = 'centered')

st.title("Prediksi Emisi CO2 di Indonesia")

# Buat download dataset
file_path = 'dataset.xlsx'
if os.path.isfile(file_path):
    st.markdown("Silahkan download template dataset berikut, lalu upload pada menu dibawah.<br>Template ini berisi dataset emisi co2 di Indonesia sampai dengan tahun 2021, anda bisa perbarui dataset tersebut dengan informasi yang lebih update.", unsafe_allow_html=True)

    st.download_button(
        label="Download dataset.xlsx",
        data=open(file_path, 'rb'),
        file_name='dataset.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.markdown("<hr>", unsafe_allow_html=True)
else:
    st.write("File dataset.xlsx tidak ditemukan.")

# Buat upload dataset
uploaded_file = st.file_uploader("Unggah file Excel (xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Baca dataset
    df = pd.read_excel(uploaded_file)
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    df.set_index(['year'], inplace=True)

    # buat tampilan kanan kiri untuk data dan grafik
    left_column, right_column = st.columns(2)
    # Left
    left_column.write("Data")
    left_column.write(df)
    # Right
    right_column.write("Grafik")
    plt.figure(figsize=(10, 5))
    plt.plot(df['co2'], color='b')
    plt.xlabel('Tahun')
    plt.ylabel('Emisi CO2')
    plt.title('Grafik Emisi CO2 Tahunan')
    # plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    right_column.pyplot(plt)

    # Section Prediksi
    st.title("Prediksi beberapa tahun kedepan.")
    year = st.slider("Estimasi Tahun", 2, 30, step=1)

    ar =  ARIMA(df, order=(15,1,15)).fit()
    pred = ar.forecast(year)

    pred_with_last_df = pd.concat([pd.Series(df.iloc[-1]['co2'], index=[pred.index[0] - pd.DateOffset(years=1)]), pred])

    if st.button("Prediksi"):
        left_column, right_column = st.columns(2)
        # Left
        left_column.write("Data")
        pred.index.name = 'year'
        left_column.write(pred)
        # Right
        right_column.write("Grafik")
        plt.figure(figsize=(10, 5))
        plt.plot(df['co2'], label='Data Aktual', color='b')
        plt.plot(pred_with_last_df, label='Data Prediksi', color='r')
        plt.xlabel('Tahun')
        plt.ylabel('Emisi CO2')
        plt.title('Grafik Prediksi Emisi CO2')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        right_column.pyplot(plt)