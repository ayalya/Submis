import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load data
# @st.cache_data

hour_data = pd.read_csv(
    "https://raw.githubusercontent.com/ayalya/Submis/refs/heads/main/dashboard/main_data.csv"
)
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'], format="%Y-%m-%d")

hour_data = pd.read_csv("https://raw.githubusercontent.com/ayalya/Submis/refs/heads/main/dashboard/main_data.csv")
# hour_data = hour_data.drop(columns=['Unnamed: 0', "z_score", 'anomaly', 'instant'])

# =================== Sidebar ====================
st.sidebar.title("Dashboard Bike Sharing")
st.sidebar.write("Analisis Data Peminjaman Sepeda")

# Pilihan menu
menu = st.sidebar.selectbox(
    "Pilih Analisis",
    [
        "Home",
        "Tren Peminjaman",
        "Hari Libur vs Hari Kerja",
        "Pengaruh Cuaca",
        "Outlier Analysis",
    ],
)

content = st.empty()
# ================== Overview ====================
if menu == "Home":
    with content.container():
        st.title("📊 Bike Sharing 🚴‍♂️")
        st.write(
            "Dataset yang digunakan berisi jumlah sepeda sewaan per jam antara tahun 2011 dan 2012 di sistem berbagi sepeda Capital dengan informasi cuaca dan musim yang sesuai."
        )

        # Menampilkan data awal
        st.subheader("Sample Data")
        over = hour_data
        over = over.drop(
            columns=[
                "Unnamed: 0",
                "z_score",
                "anomaly",
                "instant",
            ]
        )
        over = over.rename(
            columns={
                "dteday": "tanggal",
                "yr": "year",
                "mnth": "month",
                "hr": "jam",
                "cnt": "count",
                "hum": "humdity",
            }
        )
        over["tanggal"] = pd.to_datetime(over["tanggal"], format="%Y-%m-%d")
        st.dataframe(over.head())

        st.write("Adapun fitur yang digunakan sebagai berikut:")
        st.write(
            """
            - tanggal   : tanggal peminjaman
            - season    : musim (1: musim semi, 2: musim panas, 3: musim gugur, 4: musim dingin)
            - year      : tahun (0: 2011, 1:2012)
            - mnth      : bulan (1 sampai 12)
            - holiday   : hari libur atau tidak (0: libur, 1: kerja)
            - weekday   : hari kerja sampai seminggu (0 sampai 6)
            - workingday: jika hari tersebut bukan akhir pekan atau hari libur maka nilainya 1, jika tidak maka nilainya 0.
            - weathersit:
                        1: Cerah, Sedikit awan, Sebagian berawan, Sebagian berawan
                        2: Kabut + Mendung, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
                        3: Salju Ringan, Hujan Ringan + Badai Petir + Awan berserakan, Hujan Ringan + Awan berserakan
                        4: Hujan Lebat + Hujan Es + Badai Petir + Kabut, Salju + Kabut
            - temp      : Suhu yang dinormalisasi dalam Celcius. Nilai dibagi menjadi 41 (maks)
            - atemp     : Suhu perasaan yang dinormalisasi dalam Celcius. Nilai dibagi menjadi 50 (maks)
            - humdity   : Kelembapan yang dinormalisasi. Nilai dibagi menjadi 100 (maks)
            - windspeed : Kecepatan angin yang dinormalisasi. Nilai dibagi menjadi 67 (maks)
            - casual    : jumlah pengguna biasa yang telah diolah outliernya menggunakan IQR
            - registered: jumlah pengguna terdaftar yang telah diolah outliernya menggunakan IQR
            - count     : jumlah total sepeda sewaan termasuk casual dan registered yang telah diolah outliernya menggunakan IQR
            """
        )

        # Menampilkan ringkasan statistik
        st.subheader("Statistik Deskriptif")
        st.write(over.describe())

        # Matriks Korelasi
        st.subheader("Matriks Korelasi")
        fig, ax = plt.subplots(figsize=(12, 6))
        correlation_matrix = over.corr()

        sns.heatmap(correlation_matrix, cmap="Greens", annot=True)
        # plt.title("Matriks Korelasi", fontsize=16)
        st.pyplot(fig)

        st.write(
            """
                - Fitur dengan identitas, seperti dteday, month, hr, yr, dan season memiliki keterikatan satu sama lainnya.
                - Keadaan cuaca, seperti season, temp, atemp, dan windspeed memiliki keterkaitan yang positif dengan pengguna casual, registered, dan cnt."""
        )
# ============== Tren Peminjaman Sepeda =============
elif menu == "Tren Peminjaman":
    with content.container():
        st.title("📈 Tren Peminjaman Sepeda Per Jam")

        st.subheader("Stacked Bar Chart Peminjaman Sepeda per Jam pada Setiap Hari")
        # Plot Line Chart
        fig, ax = plt.subplots(figsize=(12, 6))
        data_grouped = hour_data.groupby("hr")[["casual", "registered"]].sum()
        data_grouped.plot(kind="bar", stacked=True, color=["Purple", "Green"], ax=ax)
        # ax.set_title("Stacked Bar Chart Peminjaman Sepeda per Jam")
        ax.set_xlabel("Jam")
        ax.set_ylabel("Jumlah Peminjaman")
        ax.legend(["Casual", "Registered"])
        st.pyplot(fig)

        # cek ombak

# ============== Perbandingan Hari Libur vs Hari Kerja =============
elif menu == "Hari Libur vs Hari Kerja":
    with content.container():
        st.title("📊 Perbandingan Pengguna di Hari Libur dan Hari Kerja")

        st.subheader("Pola Peminjaman Sepeda pada Hari Libur dan Hari Kerja")
        g = sns.FacetGrid(hour_data, col="workingday", height=5, aspect=1.5)
        color = sns.color_palette("mako")
        # Membuat plot dengan seaborn
        g = sns.FacetGrid(hour_data, col="workingday", height=5, aspect=1.5)
        g.map_dataframe(
            sns.lineplot, x="hr", y="casual", label="Casual", ci=None, color="purple"
        )
        g.map_dataframe(
            sns.lineplot,
            x="hr",
            y="registered",
            label="Registered",
            ci=None,
            color="green",
        )

        # Judul dan Label
        g.set_axis_labels("Jam", "Jumlah Peminjaman Sepeda")
        g.set_titles(col_template="Workingday: {col_name}")

        for ax in g.axes.flat:
            ax.set_xticks(hour_data["hr"].unique())
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.legend(
                title="User Type", labels=["Casual", "Registered"], loc="upper right"
            )

        # Menampilkan di Streamlit
        st.pyplot(g.figure)

        # Melebur (melt) data agar casual dan registered bisa tampil dalam satu boxplot
        hour_data_melted = hour_data.melt(
            id_vars=["workingday"],
            value_vars=["casual", "registered"],
            var_name="User Type",
            value_name="Count",
        )

        # Membuat figure dan axis
        st.subheader("Distribusi Peminjaman Sepeda pada Hari Kerja dan Libur")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(
            data=hour_data_melted,
            x="workingday",
            y="Count",
            hue="User Type",
            palette="mako",
            ax=ax,
        )
        # ax.set_title('Sebaran Peminjaman Sepeda pada Hari Kerja dan Libur', fontsize=14)
        ax.set_xticklabels(["Libur (0)", "Hari Kerja (1)"])
        ax.set_xlabel("Working Day", fontsize=12)
        ax.set_ylabel("Jumlah Peminjaman", fontsize=12)
        plt.grid(True)
        st.pyplot(fig)


# ============== Pengaruh Cuaca =============
elif menu == "Pengaruh Cuaca":
    with content.container():
        st.title("🌩️🌤️ Pengaruh Cuaca terhadap Peminjaman Sepeda ⛈️☀️")

        # Boxplot cuaca
        st.subheader("Persebaran Peminjaman Sepeda Musiman")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(
            data=hour_data, x="hr", y="cnt", hue="season", ax=ax, color="dark", ci=None
        )
        ax.set_xticks(hour_data["hr"].unique())
        plt.grid(True)
        # ax.set(title='Persebaran Peminjaman Sepeda Musiman')
        ax.set_xlabel("Hour")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # ==========BOXPLOT==============
        st.subheader("Distribusi Peminjaman Berdasarkan Musim")
        hour_data_melted = hour_data.melt(
            id_vars=["season"],
            value_vars=["casual", "registered"],
            var_name="User Type",
            value_name="Count",
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        # Boxplot dengan hue berdasarkan kategori casual & registered
        sns.boxplot(
            data=hour_data_melted,
            x="season",
            y="Count",
            hue="User Type",
            palette="muted",
            ax=ax,
        )

        # ax.set(title='Distribusi Peminjaman Berdasarkan Musim', xlabel='Musim', ylabel='Jumlah Peminjaman')
        ax.grid(True)
        ax.legend(title="Tipe Pengguna")
        st.pyplot(fig)

        # ===================== COR MATRIX =================
        st.subheader("Distribusi Peminjaman Berdasarkan Musim")
        corr_Season = hour_data[
            [
                "temp",
                "atemp",
                "hum",
                "windspeed",
                "season",
                "casual",
                "registered",
                "cnt",
            ]
        ].corr()

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(8, 6))  # Buat figure untuk Streamlit
        sns.heatmap(corr_Season, square=True, annot=False, cmap="Blues", ax=ax)

        # Tampilkan di Streamlit
        st.pyplot(fig)

# ============== Handling Outlier =============
elif menu == "Outlier Analysis":
    with content.container():
        st.title("📈 Time Series Data Anomali")
        fig, ax = plt.subplots(figsize=(12, 6))

        hour_data["z_score"] = (hour_data["cnt"] - hour_data["cnt"].mean()) / hour_data[
            "cnt"
        ].std()

        # Menentukan threshold anomali (Z-Score > 3 atau < -3)
        threshold = 3
        hour_data["anomaly"] = hour_data["z_score"].abs() > threshold

        sns.lineplot(
            data=hour_data,
            x="dteday",
            y="cnt",
            label="Jumlah Peminjaman",
            alpha=0.6,
            ci=None,
        )
        sns.lineplot(
            data=hour_data,
            x="dteday",
            y="registered",
            label="Registered",
            alpha=0.6,
            ci=None,
        )
        sns.lineplot(
            data=hour_data, x="dteday", y="casual", label="Casual", alpha=0.6, ci=None
        )
        sns.scatterplot(
            data=hour_data[hour_data["anomaly"]],
            x="dteday",
            y="cnt",
            color="red",
            label="Anomali Count",
            s=50,
        )
        sns.scatterplot(
            data=hour_data[hour_data["anomaly"]],
            x="dteday",
            y="registered",
            color="Orange",
            label="Anomali Registered",
            s=50,
        )
        sns.scatterplot(
            data=hour_data[hour_data["anomaly"]],
            x="dteday",
            y="casual",
            color="Green",
            label="Anomali Casual",
            s=50,
        )
        # plt.title('Tren Peminjaman Sepeda dan Anomali')
        ax.xaxis.set_major_locator(mdates.MonthLocator())  
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format bulan (Jan 2021, Feb 2021, ...)

        plt.xticks(rotation=45)  # Rotasi agar mudah dibaca
        ax.set_xlabel('Tanggal')
        ax.set_ylabel('Jumlah Peminjaman')
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)  

        st.pyplot(fig)

    # st.write("""
    # Kesimpulan dari Time-Series Anomali.
    # - Peminjaman meningkat pada pertengahan tahun.
    # - Anomali peminjaman mayoritas terlihat pada saat penjualan mengalami meningkatan.
    # - Distribusi persebaran outlier pada pelanggan casual dan registered memiliki jarak yang sama berada di angka 300-350.
    # - Anomali sangat terlihat pada peminjaman di akhir tahun 2012 yang diikuti dengan penurunan peminjaman yang sangat drastis.
    # - Anomali peminjam registered lebih tinggi dibandingkan dengan peminjam casual
    # """)


st.sidebar.markdown("---")
st.sidebar.write("Dibuat oleh Alya Fauzia Azizah")
st.sidebar.write("Submission Belajar Analisis Data dengan Python")
