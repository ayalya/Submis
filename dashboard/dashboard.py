import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data (Pastikan Anda memiliki dataset yang sesuai)
@st.cache_data
def load_data():
    # Gantilah ini dengan path dataset yang sesuai
    df = pd.read_csv("https://raw.githubusercontent.com/ayalya/Submis/refs/heads/main/dashboard/main_data.csv")
    # df['weekday'] = df['weekday'].map({0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'})
    # df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return df

df = load_data()

# =============================== Sidebar filter ===============================
st.sidebar.write("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", ['Semua'] + list(df['yr'].unique()))
selected_day = st.sidebar.selectbox("Pilih Hari", ['Semua'] + list(df['weekday'].unique()))
selected_season = st.sidebar.selectbox("Pilih Musim", ['Semua'] + list(df['season'].unique()))

dayy = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
ses = ['Spring', 'Summer', 'Fall', 'Winter']

# Copy data
filtered_df = df.copy()

# Filter data sesuai pilihan pengguna
if selected_year != 'Semua':
    filtered_df = filtered_df[filtered_df['yr'] == selected_year]
if selected_day != 'Semua':
    filtered_df = filtered_df[filtered_df['weekday'] == selected_day]
if selected_season != 'Semua':
    filtered_df = filtered_df[filtered_df['season'] == selected_season]

# Urutkan kategori setelah filtering
filtered_df['weekday'] = pd.Categorical(filtered_df['weekday'], categories=dayy, ordered=True)
filtered_df['season'] = pd.Categorical(filtered_df['season'], categories=ses, ordered=True)

# Urutkan hasil akhir
filtered_df = filtered_df.sort_values(by=['yr', 'season', 'weekday'])

st.sidebar.markdown("---")
st.sidebar.write("Submission Belajar Analisis Data dengan Python di Platfrom Dicoding")

# =============== Header utama ================================
st.title("📊 Dashboard Peminjaman Sepeda")
st.markdown("Dataset yang digunakan berisi jumlah sepeda sewaan per jam antara tahun 2011 dan 2012 di sistem berbagi sepeda Capital dengan informasi cuaca dan musim yang sesuai.")

# --- PLOT 1: Tren Peminjaman per Jam ---
st.subheader("Tren Peminjaman Sepeda per Jam")
fig, ax = plt.subplots(figsize=(10, 5))

# Pastikan hanya 'casual' dan 'registered' yang digunakan
hourly_trend = filtered_df.groupby("hr")[['casual', 'registered']].mean().reset_index()
# Plot hanya untuk 'casual' dan 'registered'
hourly_trend.set_index('hr')[['casual', 'registered']].plot(kind="bar", stacked=True, color=['Purple', 'Green'], ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman")
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

# --- PLOT 2: Boxplot Peminjaman Berdasarkan Hari ---
st.subheader("Distribusi Peminjaman Sepeda Berdasarkan Hari")
fig, ax = plt.subplots(figsize=(10, 5))
df_melted = filtered_df.melt(id_vars=['weekday'], value_vars=['casual', 'registered'], var_name='User Type', value_name='Count')
sns.boxplot(data=df_melted, x='weekday', y='Count', hue='User Type', palette="mako", ax=ax)
ax.set_xlabel("Hari")
ax.set_ylabel("Jumlah Peminjaman")
# ax.set_title("Sebaran Peminjaman Sepeda per Hari")
st.pyplot(fig)

# --- PLOT 3: Distribusi Peminjaman Berdasarkan Musim ---
st.subheader("Distribusi Peminjaman Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x='season', y='cnt', palette="Set2", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
# ax.set_title("Peminjaman Sepeda Berdasarkan Musim")
st.pyplot(fig)

# --- PLOT 4: Perbandingan Peminjaman Hari Kerja vs Akhir Pekan ---
st.subheader("Perbandingan Pengguna di Hari Libur dan Hari Kerja")
hour_data_melted = filtered_df.melt(id_vars=['workingday'], value_vars=['casual', 'registered'], var_name='User Type', value_name='Count')
g = sns.FacetGrid(filtered_df, col='workingday', height=5, aspect=1.5)
g.map_dataframe(sns.lineplot, x='hr', y='casual',  ci=None, color='Purple')
g.map_dataframe(sns.lineplot, x='hr', y='registered',  ci=None, color='Green')

# Judul dan Label
g.set_axis_labels('Jam', 'Jumlah Peminjaman Sepeda')
g.set_titles(col_template="Workingday: {col_name}")

# Konfigurasi tambahan untuk sumbu
for ax in g.axes.flat:
    ax.set_xticks(filtered_df["hr"].unique())
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(title="User Type", labels=["Casual", "Registered"], loc="upper right")

       # Menampilkan di Streamlit
st.pyplot(g.figure)
# st.dataframe(filtered_df.head())

# Footer
st.markdown("---")
st.markdown("Dibuat oleh Alya Fauzia Azizah")
st.markdown("****Email:** alyafauziaaz25@gmail.com ID Dicoding: alyafauzia**")
