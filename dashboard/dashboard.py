# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Import Dataset
all_df = pd.read_csv("./airquality_data.csv")

# Create function based on analysis in Notebook
def create_average_weather_data(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df_resampled = df.resample(rule='D', on='datetime').agg({
        'RAIN': 'mean',
        'TEMP': 'mean',
        'PRES': 'mean',
        'DEWP': 'mean',
        'WSPM': 'mean'
    })
    df_resampled = df_resampled.reset_index()
    df_resampled.rename(columns={
        'RAIN': 'rain_mean',
        'TEMP': 'temp_mean',
        'PRES': 'pres_mean',
        'DEWP': 'dewp_mean',
        'WSPM': 'wspm_mean'
    }, inplace=True)

    return df_resampled

def create_station_weather_summary(df):
    station2rain_summary= df.groupby('station').agg(
        mean=('RAIN', 'mean'),          # Rata-rata nilai RAIN per station
        count=('RAIN', lambda x: (x != 0).sum()),  # Hitung jumlah nilai RAIN yang tidak 0 per station
        max=('RAIN', 'max'),          # Nilai maksimum RAIN per station
        sum=('RAIN', 'sum')
    ).reset_index()
    station2rain_summary.columns = ['Station', 'mean_rain', 'count_non_zero_rain', 'max_rain', 'sum_rain']
    station2rain_summary = station2rain_summary.sort_values(by='mean_rain', ascending=False).reset_index(drop=True)
    return station2rain_summary

def create_station_quality_summary(df):
    station2mean_param_summary= df.groupby('station')[['CO','PM2.5', 'PM10', 'SO2', 'NO2', 'O3']].agg(['mean']).reset_index()
    station2mean_param_summary.columns = ['Station', 'mean_co', 'mean_pm2.5', 'mean_pm10', 'mean_so2', 'mean_no3', 'mean_o3']
    station2mean_param_summary = station2mean_param_summary.sort_values(by='mean_co', ascending=False).reset_index(drop=True)
    return station2mean_param_summary

def create_rain_quality_correlation(df):
    rain_correlation = df[[ 'RAIN','CO','PM2.5', 'PM10', 'SO2', 'NO2', 'O3']].corr()
    return rain_correlation

def create_rain_weather_correlation(df):
    weather_correlation = df[[ 'RAIN','TEMP', 'PRES', 'DEWP', 'WSPM']].corr()
    return weather_correlation

def create_rain_allparams_correlation(df):
    airquality_correlation = df[[ 'RAIN', 'TEMP', 'PRES', 'DEWP', 'WSPM' ,'CO','PM2.5', 'PM10', 'SO2', 'NO2', 'O3']].corr()
    return airquality_correlation

datetime_columns = ["datetime"]
all_df.sort_values(by="datetime", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["datetime"].min()
max_date = all_df["datetime"].max()

station_group = all_df.groupby('station').size().reset_index(name='count')
station_names = station_group[['station']]

with st.sidebar:
    # Title
    st.title("Air Quality Analyze")

    # Menambahkan logo perusahaan
    st.image("Project_Analisis_Data_Air_Quality\dashboard\logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Filter Station
    selected_station = st.multiselect("Pilih Stasiun", station_names, default=station_names)

filtered_df = all_df[(all_df["station"].isin(selected_station)) &
                (all_df["datetime"] >= str(start_date)) & 
                (all_df["datetime"] <= str(end_date))]

avg_weather_df = create_average_weather_data(filtered_df)
station_weather_df = create_station_weather_summary(filtered_df)
station_quality_df = create_station_quality_summary(filtered_df)
rain_quality_corr_df = create_rain_quality_correlation(filtered_df)
rain_weather_corr_df = create_rain_weather_correlation(filtered_df)
rain_allparams_corr_df = create_rain_allparams_correlation(filtered_df)

st.header('Air Quality & Weather Dashboard :sparkles:')

st.subheader('Statistic Avg')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    mean_rain = avg_weather_df.rain_mean.mean()
    mean_rain = round(mean_rain, 2)
    st.metric("Avg Curah Hujan", value=mean_rain)

with col2:
    mean_temp = avg_weather_df.temp_mean.mean()
    mean_temp = round(mean_temp, 2)
    st.metric("Avg Temperature", value=mean_temp)

with col3:
    mean_pres = avg_weather_df.pres_mean.mean()
    mean_pres = round(mean_pres, 2)
    st.metric("Avg Tekanan Udara", value=mean_pres)

with col4:
    mean_dewp = avg_weather_df.dewp_mean.mean()
    mean_dewp = round(mean_dewp, 2)
    st.metric("Avg Titik Embun", value=mean_dewp)

with col5:
    mean_wspm = avg_weather_df.wspm_mean.mean()
    mean_wspm = round(mean_wspm, 2)
    st.metric("Avg Kecepatan Angin", value=mean_wspm)

st.subheader("Tren Curah Hujan dalam Waktu Tertentu")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    filtered_df["datetime"],
    filtered_df["RAIN"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Tren Curah Hujan Berdasarkan Bulan dan Tahun pada Station")

plt.figure(figsize=(10, 6))
sns.lineplot(x='month', y='RAIN', hue='year', data=filtered_df, palette='Set1')

plt.xlabel("Bulan", fontsize=12)
plt.ylabel("Curah Hujan (mm)", fontsize=12)

st.pyplot(plt)

st.subheader("Tabel Wilayah Stasiun dengan Curah Hujan Tertentu")

st.dataframe(station_weather_df)

st.subheader("Wilayah Stasiun dengan Kadar Kualitas Udara Tertentu")
 
# Mengolah value pada curah hujan x kualitas udara
df_long = pd.melt(station_quality_df, id_vars=['Station'], value_vars=['mean_co', 'mean_pm2.5', 'mean_pm10', 'mean_so2', 'mean_no3', 'mean_o3'],
                  var_name='Parameter', value_name='Value')

df_co = df_long[df_long['Parameter'] == 'mean_co']  # Data hanya untuk mean_co
df_other = df_long[df_long['Parameter'] != 'mean_co']  # Data selain mean_co

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.lineplot(x="Station", y="Value", hue="Parameter", data=df_co, color='blue', ax=ax[0], marker='o')
ax[0].set_title('Persebaran mean_co per Station', fontsize=24)
ax[0].set_xlabel('Station')
ax[0].set_ylabel('Nilai mean_co')
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30, rotation=45)
 
sns.lineplot(x="Station", y="Value", hue="Parameter", data=df_other, ax=ax[1], marker='o')
ax[1].set_title('Persebaran Parameter Selain mean_co per Station', fontsize=24)
ax[1].set_xlabel('Station')
ax[1].set_ylabel('Nilai Parameter')
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30, rotation=45)
 
st.pyplot(fig)

st.subheader("Tabel Wilayah Stasiun dengan Kadar Kualitas Udara Tertentu")

# Mengelola data stasiun summary tarhadap kualitas udara
station_quality_df['air_quality_score'] = (1 / station_quality_df['mean_co']) + (1 / station_quality_df['mean_pm2.5']) + (1 / station_quality_df['mean_pm10']) + \
                          (1 / station_quality_df['mean_so2']) + (1 / station_quality_df['mean_no3']) + (1 / station_quality_df['mean_o3'])
df_sorted = station_quality_df.sort_values(by='air_quality_score', ascending=False)
df_sorted = df_sorted[['Station', 'air_quality_score']].reset_index(drop=True)

st.dataframe(df_sorted)

st.subheader("Korelasi Curah Hujan dengan Parameter Kualitas Udara")

plt.figure(figsize=(10, 8)) 
sns.heatmap(rain_quality_corr_df, annot=True, cmap='RdYlBu', fmt=".2f", linewidths=0.5, center=0)

# plt.title('Korelasi Antara Curah Hujan dan Parameter Kualitas Udara', fontsize=16)

st.pyplot(plt)

st.subheader("Korelasi Antara Curah Hujan dengan Parameter Cuaca")

plt.figure(figsize=(10, 8)) 
sns.heatmap(rain_quality_corr_df, annot=True, cmap='RdYlBu', fmt=".2f", linewidths=0.5, center=0)

# plt.title('Korelasi Antara Curah Hujan dengan Parameter Cuaca', fontsize=16)

st.pyplot(plt)

st.subheader("Korelasi Antar Parameter Kualitas Udara")

plt.figure(figsize=(10, 8)) 
sns.heatmap(rain_quality_corr_df, annot=True, cmap='RdYlBu', fmt=".2f", linewidths=0.5, center=0)

# plt.title('Korelasi Antar Parameter Kualitas Udara', fontsize=16)

st.pyplot(plt)