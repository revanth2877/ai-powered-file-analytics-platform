import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Traffic Flow Dashboard', layout='wide')

st.title('🚦 Intelligent Traffic Flow & ETA Analysis')

# Load sample dataset safely
try:
    df = pd.read_csv('sample_trips.csv')
except Exception as e:
    st.error(f'Error loading dataset: {e}')
    st.stop()

# Convert datetime
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['hour'] = df['pickup_datetime'].dt.hour

# Metrics
avg_duration = round(df['trip_duration'].mean() / 60, 2)

col1, col2 = st.columns(2)

with col1:
    st.metric('Total Records', f'{len(df):,}')

with col2:
    st.metric('Average Trip Duration (min)', avg_duration)

# Hourly traffic analysis
hourly = df.groupby('hour').size().reset_index(name='trip_count')

st.subheader('Hourly Traffic Flow')

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(hourly['hour'], hourly['trip_count'], marker='o')
ax.set_xlabel('Hour')
ax.set_ylabel('Trips')
ax.grid(True)

st.pyplot(fig)

st.subheader('Sample GPS Trip Data')
st.dataframe(df.head(10))

st.markdown('---')
st.write('Dataset: NYC Taxi Trip Duration (Kaggle)')
