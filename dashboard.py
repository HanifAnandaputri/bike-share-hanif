# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Bike Share Insight ")

# Deskripsi Dashboard
dashboard_description = """
Dashboard ini memberikan wawasan mendalam tentang sistem penyewaan sepeda dari data program bike-sharing modern. 
Pengguna dapat mengeksplorasi pola penggunaan sepeda berdasarkan musim, kondisi cuaca, dan tren harian.

Data mencakup setiap transaksi penyewaan, termasuk waktu dan lokasi, menjadikannya sumber informasi berharga untuk 
analisis mobilitas perkotaan dan pengambilan keputusan dalam perencanaan transportasi serta pengelolaan lingkungan.

Fitur filter memungkinkan pengguna menelusuri data berdasarkan tanggal, jenis pengguna, bulan, dan hari dalam seminggu. 
Visualisasi interaktif membantu memahami tren penyewaan serta pengaruh faktor musiman dan cuaca.

Dashboard ini dirancang untuk mendukung analisis bagi perencana kota, pengelola program bike-sharing, dan peneliti 
yang tertarik pada mobilitas dan keberlanjutan.

Sumber Data: [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)
"""
st.write(dashboard_description)

# Memuat Data
day_df = pd.read_csv(r'Dashboard\day.csv')
clean_df = pd.read_csv(r'Dashboard\clean_bike_share_data.csv')

# Menambahkan Sidebar untuk Filter
st.sidebar.header("Filter Data")

# Filter berdasarkan rentang tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", value=pd.to_datetime(day_df['dteday'].min()).date())
end_date = st.sidebar.date_input("Tanggal Akhir", value=pd.to_datetime(day_df['dteday'].max()).date())

# Mengkonversi kembali ke datetime untuk filter
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data sesuai rentang tanggal
filtered_data = day_df[(pd.to_datetime(day_df['dteday']) >= start_date) & (pd.to_datetime(day_df['dteday']) <= end_date)]

# Filter berdasarkan jenis pengguna
user_types = st.sidebar.multiselect("Pilih Jenis Pengguna:", options=["casual", "registered"], default=["casual", "registered"])
filtered_data = filtered_data[(filtered_data['casual'] > 0) | (filtered_data['registered'] > 0)]

# Filter berdasarkan bulan (dalam nama bulan bahasa Indonesia) dengan opsi "All"
bulan_options = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 
    6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 
    11: "November", 12: "Desember", "All": "Semua"
}
month_filter = st.sidebar.selectbox("Pilih Bulan:", options=list(bulan_options.keys()), format_func=lambda x: bulan_options[x])

if month_filter != "All":
    filtered_data = filtered_data[filtered_data['mnth'] == month_filter]

# Filter berdasarkan hari dalam seminggu (dalam nama hari bahasa Indonesia) dengan opsi "All"
hari_options = {
    0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 
    4: "Jumat", 5: "Sabtu", 6: "Minggu", "All": "Semua"
}
weekday_filter = st.sidebar.selectbox("Pilih Hari dalam Seminggu:", options=list(hari_options.keys()), format_func=lambda x: hari_options[x])

if weekday_filter != "All":
    filtered_data = filtered_data[filtered_data['weekday'] == weekday_filter]

# Menampilkan Data yang sudah difilter
st.subheader("Data Penyewaan Sepeda (Filtered)")
st.dataframe(filtered_data)

# Kolom
col1, col2, col3 = st.columns([1, 1, 1])

# Line Plot: Pergerakan Penyewaan Setiap Hari
with col1:
    st.subheader("Pergerakan Penyewaan Sepeda Harian ")
    st.write(' ')
    st.write(' ')
    fig, ax = plt.subplots(figsize=(5, 5))  # Menetapkan ukuran figure
    ax.plot(pd.to_datetime(filtered_data['dteday']), filtered_data['cnt'], label='Total Penyewaan', color='rosybrown')
    ax.set_title('Pergerakan Penyewaan Sepeda Harian')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Visualisasi Pertama: Distribusi Penyewaan Berdasarkan Musim
with col2:
    st.subheader("Distribusi Penyewaan Berdasarkan Musim")
    season_counts = clean_df.groupby('season')['cnt'].sum()
    fig1, ax1 = plt.subplots(figsize=(5, 4))  # Menetapkan ukuran figure
    season_counts.plot(kind='bar', ax=ax1, color='salmon')
    ax1.set_title('Total Penyewaan per Musim')
    ax1.set_ylabel('Jumlah Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# Visualisasi Kedua: Pengaruh Kondisi Cuaca
with col3:
    st.subheader("Pengaruh Kondisi Cuaca Terhadap Penyewaan")
    st.write(' ')
    st.write(' ')
    weather_counts = clean_df.groupby('weathersit')['cnt'].sum()
    fig2, ax2 = plt.subplots(figsize=(5, 4))  # Menetapkan ukuran figure
    weather_counts.plot(kind='bar', ax=ax2, color='olive')
    ax2.set_title('Total Penyewaan Berdasarkan Kondisi Cuaca')
    ax2.set_ylabel('Jumlah Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.write("---")
st.title('Pertanyaan Bisnis:')
st.write(
    """
    - **Bagaimana variasi pola penggunaan sepeda berdasarkan musim tahun 2011-2012?**
    - **Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?**
    
    **Mari kita lihat satu per satu:**
    
    """
)
st.write("---")

# Pertanyaan 1
st.write("""
         ### Pertanyaan 1: Bagaimana variasi pola penggunaan sepeda berdasarkan musim tahun 2011-2012?
Untuk menjawab pertanyaan ini, analisis akan menggunakan visualisasi data, korelasi, dan agregasi data sederhana untuk melihat pola penggunaan sepeda di setiap musim.
Langkah-langkah yang akan dilakukan:
1. Membuat plot untuk melihat distribusi jumlah penyewaan sepeda pada setiap musim (spring, summer, fall, dan winter).
Agregasi Data Penyewaan Per Musim:
3. Menghitung total dan rata-rata penyewaan sepeda untuk setiap musim guna melihat pola penggunaan sepeda di tiap musim.
Perbandingan Tahun 2011 dan 2012:
4. Membandingkan pola penyewaan sepeda pada tahun 2011 dan 2012 untuk melihat apakah ada perbedaan signifikan pada pola penggunaan di kedua tahun tersebut.

""")

# Membuat tab untuk setiap tabel
tabs = st.tabs(["Distribusi Musiman", "Total Musiman", "2011 v.s 2012"])

# Tab untuk grafik distribusi penyewaan sepeda berdasarkan musim
with tabs[0]:
    # Visualisasi distribusi penyewaan sepeda berdasarkan musim
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='season', y='cnt', data=clean_df, palette="pastel", ax=ax1)
    ax1.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig1)
    
    # Expander untuk insight
    with st.expander("Insight"):
        st.markdown("""
        1. Penyewaan Tertinggi di Musim Panas dan Musim Gugur. Hal ini mengindikasikan bahwa pengguna lebih aktif menggunakan sepeda pada musim-musim ini, yang mungkin disebabkan oleh cuaca yang lebih nyaman untuk bersepeda.
        2. Musim Semi memiliki jumlah penyewaan yang paling rendah. Hal ini terlihat dari nilai median yang lebih rendah dibandingkan dengan musim lainnya. Hal tersebut diduga karena cuaca yang lebih dingin dan tidak stabil pada musim semi yang memengaruhi keputusan orang untuk menggunakan sepeda.
        3. Meskipun Musim Dingin berikaitan dengan kondisi yang kurang nyaman untuk bersepeda, jumlah penyewaan masih cukup signifikan, dengan median yang berada di atas musim semi. Hal ini menunjukkan masih ada kelompok orang yang masih menggunakan layanan sepeda meski cuaca yang harsh, dugaan awal adalah kelompok 'registered'
        """)

# Tab untuk grafik total dan rata-rata penyewaan sepeda per musim
with tabs[1]:
    # Menghitung total dan rata-rata penyewaan sepeda per musim
    season_aggregation = clean_df.groupby('season')['cnt'].agg(['sum', 'mean']).reset_index().sort_values(by='sum')
    
    # Visualisasi agregasi total dan rata-rata penyewaan sepeda per musim
    fig2, ax2 = plt.subplots(1, 2, figsize=(12, 6))
    
    # Barplot untuk total penyewaan per musim
    sns.barplot(x='season', y='sum', data=season_aggregation, palette="pastel", ax=ax2[0])
    ax2[0].set_title('Total Penyewaan Sepeda per Musim')
    ax2[0].set_xlabel('Musim')
    ax2[0].set_ylabel('Total Penyewaan')
    
    # Barplot untuk rata-rata penyewaan per musim
    sns.barplot(x='season', y='mean', data=season_aggregation, palette="pastel", ax=ax2[1])
    ax2[1].set_title('Rata-rata Penyewaan Sepeda per Musim')
    ax2[1].set_xlabel('Musim')
    ax2[1].set_ylabel('Rata-rata Penyewaan')
    
    st.pyplot(fig2)
    
    # Expander untuk insight
    with st.expander("Insight"):
        st.markdown(""" 
        Musim Gugur memiliki total penyewaan sepeda tertinggi dengan angka 1,061,129 diikuti 
        Musim Panas dengan total penyewaan 918,589, sedangkan Musim Dingin memiliki total penyewaan 841,613. 
        Ini menunjukkan bahwa kedua musim ini juga populer, tetapi tidak sepopuler musim gugur yang mungkin disebabkan 
        oleh cuaca yang nyaman untuk beraktivitas dan pemandangan yang indah.
        """)

# Tab untuk grafik perbandingan penyewaan sepeda antara tahun 2011 dan 2012
with tabs[2]:
    # Menghitung total penyewaan sepeda per musim berdasarkan tahun
    season_year_agg = clean_df.groupby(['season', 'yr'])['cnt'].sum().reset_index().sort_values(by='cnt')
    season_year_agg['yr'] = season_year_agg['yr'].map({0: '2011', 1: '2012'})
    
    # Visualisasi perbandingan penyewaan sepeda tahun 2011 dan 2012
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', hue='yr', data=season_year_agg, palette="pastel", ax=ax3)
    ax3.set_title("Perbandingan Penyewaan Sepeda Tahun 2011 dan 2012 Berdasarkan Musim")
    ax3.set_xlabel("Musim")
    ax3.set_ylabel("Total Penyewaan")
    ax3.legend(title='Tahun')
    st.pyplot(fig3)
    
    # Expander untuk insight
    with st.expander("Insight"):
        st.markdown("""
        1. Peningkatan total penyewaan sepeda di setiap musim pada tahun 2012 dibandingkan tahun 2011. Hal ini menunjukkan tren positif dalam penggunaan sepeda di tahun 2012.
        2. Musim Gugur menunjukkan jumlah penyewaan tertinggi di antara semua musim pada kedua tahun tersebut
        3. Kenaikan penggunaan pada musim dingin di tahun 2012 tidak sebesar musim lainnya, hal ini menunjukkan bahwa pelanggan mempertimbangkan banyak faktor untuk beraktivitas.
        """)

# Pengantar 1 ke 2
st.write(
    """
###
Pada tab pertama, dieksplorasi distribusi penyewaan sepeda berdasarkan musim, yang memberikan wawasan mengenai kapan dan di mana pengguna paling aktif. Kami menggunakan box plot dan bar chart untuk memperlihatkan total penyewaan serta perbandingan antar musim.

Tab kedua fokus pada analisis total dan rata-rata penyewaan per musim, memungkinkan Anda untuk melihat tren penggunaan sepeda dari tahun ke tahun. Grafik-grafik ini memberikan gambaran yang jelas tentang bagaimana preferensi pengguna berubah dari musim ke musim.

Pada tab ketiga, data penyewaan antara tahun 2011 dan 2012 dibandingkan, dengan tujuan untuk menilai apakah terdapat perubahan signifikan dalam pola penggunaan sepeda di kedua tahun tersebut, sehingga dapat memberikan pandangan yang lebih luas tentang kebiasaan pengguna.

**Lalu, Bagaimana dengan pengaruh kondisi musim atau cuaca terhadap jumlah penyewaan sepeda?**
""")

st.write('---')

# Pertanyaan 2
st.write("""
         ### Pertanyaan 2: Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?
Untuk menjawab pertanyaan ini, analisis akan memanfaatkan visualisasi data, analisis korelasi, dan agregasi data sederhana untuk memahami hubungan antara kondisi cuaca dan jumlah penyewaan sepeda.

Langkah-langkah yang akan dilakukan:
1. Membuat plot untuk menunjukkan distribusi jumlah penyewaan sepeda berdasarkan kategori kondisi cuaca (weathersit). Hal ini bertujuan untuk melihat seberapa besar pengaruh kondisi cuaca terhadap jumlah penyewaan.
Analisis Korelasi:
2. Menghitung koefisien korelasi antara jumlah penyewaan sepeda (cnt) dan variabel cuaca lainnya, seperti suhu (temp dan atemp), kelembapan (hum), dan kecepatan angin (windspeed). Ini akan memberikan gambaran mengenai hubungan linier antara faktor-faktor cuaca dengan jumlah penyewaan.
Agregasi Data Penyewaan Berdasarkan Kondisi Cuaca:
3. Menghitung total dan rata-rata penyewaan sepeda untuk setiap kategori kondisi cuaca. Ini bertujuan untuk memahami pola penggunaan sepeda dalam konteks berbagai kondisi cuaca yang berbeda.
""")


# Tab untuk analisis cuaca
weather_tabs = st.tabs(["Distribusi Penyewaan", "Matriks Korelasi", "Agregasi Penyewaan"])

# Tab 1: Distribusi Penyewaan Berdasarkan Kondisi Cuaca
with weather_tabs[0]:
    st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    
    # Visualisasi distribusi penyewaan sepeda berdasarkan kondisi cuaca
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=clean_df, x='weathersit', y='cnt', palette='pastel', ax=ax)
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Berat'])
    st.pyplot(fig)

    # Expander untuk insight
    with st.expander("Insight"):
        st.markdown(""" 
        1. Penyewaan sepeda tertinggi terjadi pada kondisi berkabut, terlihat dari median yang lebih tinggi. Hal ini menunjukkan bahwa pengguna tetap aktif meskipun cuaca tidak sepenuhnya cerah.
        2. Variabilitas jumlah penyewaan pada cuaca cerah dan berkabut menunjukkan lebar yang hampir sama, mengindikasikan adanya hari dengan penyewaan tinggi dan rendah, yang mungkin dipengaruhi oleh faktor lain.
        3. Penyewaan sangat rendah saat cuaca hujan ringan dan berat, menunjukkan bahwa pengguna cenderung menghindari bersepeda dalam kondisi hujan, sehingga cuaca ekstrem berdampak signifikan terhadap perilaku penyewaan.
        """)

# Tab 2: Matriks Korelasi
with weather_tabs[1]:
    st.subheader("Matriks Korelasi antara Jumlah Penyewaan dan Variabel Cuaca")
    
    # Menghitung korelasi antara jumlah penyewaan dan variabel cuaca
    correlation_df = clean_df[['cnt', 'temp', 'atemp', 'hum', 'windspeed']]
    correlation = correlation_df.corr()
    
    # Menampilkan matriks korelasi
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title('Matriks Korelasi antara Jumlah Penyewaan dan Variabel Cuaca')
    st.pyplot(fig)

    # Expander untuk insight
    with st.expander("Insight"):
        st.markdown("""
        1. Temp dan atemp berkorelasi positif hampir sempurna. Ini menunjukkan bahwa perubahan suhu udara dan suhu yang dirasakan sangat sejalan, mempengaruhi keputusan pengguna untuk menyewa sepeda.
        2. Korelasi positif yang signifikan (> 0.5) antara temp dan jumlah penyewaan (cnt) mengindikasikan bahwa semakin tinggi suhu udara, semakin banyak pelanggan yang melakukan penyewaan sepeda. Hal ini menunjukkan bahwa pengguna lebih cenderung beraktivitas di luar saat cuaca hangat.
        3. Terdapat korelasi negatif antara windspeed dengan cnt, hum, dan temp. Hal ini mengindikasikan bahwa meningkatnya kecepatan angin dan kelembapan cenderung mengurangi minat pengguna untuk menyewa sepeda, yang bisa jadi disebabkan oleh ketidaknyamanan saat bersepeda dalam kondisi tersebut.
        """)

# Tab 3: Agregasi Penyewaan Berdasarkan Kondisi Cuaca
with weather_tabs[2]:
    st.subheader("Agregasi Penyewaan Berdasarkan Kondisi Cuaca")
    
    # Menghitung total dan rata-rata penyewaan untuk setiap kondisi cuaca
    weathersit_agg = clean_df.groupby('weathersit')['cnt'].agg(['sum', 'mean']).reset_index()
    weathersit_agg.columns = ['Kondisi Cuaca', 'Total Penyewaan', 'Rata-rata Penyewaan']
    weathersit_agg = weathersit_agg.sort_values(by='Total Penyewaan')
    
    # Menampilkan hasil agregasi
    st.dataframe(weathersit_agg)

    # Expander untuk insight
    with st.expander("Insight"):
        st.markdown("""
        1. Cuaca cerah dan berawan sedikit mencatatkan jumlah penyewaan tertinggi, dengan total mencapai 2.257.952. Hal ini menunjukkan bahwa pengguna lebih cenderung menyewa sepeda pada hari yang cerah.
        2. Walaupun cuaca berkabut + mendung masih memberikan jumlah penyewaan yang signifikan (996.858), penyewaan dalam kondisi salju ringan dan hujan ringan + petir sangat rendah (37.869). Ini menunjukkan bahwa pengguna cenderung menghindari bersepeda dalam kondisi cuaca yang kurang mendukung.
        """)

# Memberi garis pembatas
st.write('----')



# Conclusion
st.markdown('## Conclusion')

# Conclusion Pertanyaan 1
st.markdown("""
### Seberapa sering dan seberapa baru pengguna menyewa sepeda dari sistem bike sharing pada tahun 2011-2012?

> Dari pola penggunaan sepeda, dapat dilihat bahwa musim sangat mempengaruhi pola penggunaan sepeda. Jumlah penyewaan tertinggi terjadi pada musim gugur dan musim panas, menunjukkan bahwa pengguna lebih suka menggunakan sepeda di musim dengan suhu yang lebih tinggi. Musim dingin dan musim semi memiliki jumlah penyewaan yang lebih rendah, terutama pada hari-hari ketika cuaca buruk. Hal ini cenderung menggambarkan bahwa suhu dan cuaca adalah faktor-faktor penting dalam keputusan pengguna untuk menyewa sepeda.
""")

# Conclusion Pertanyaan 1
st.markdown(
    """
### Bagaimana karakteristik pengguna kasual dibandingkan dengan pengguna terdaftar dalam hal frekuensi dan waktu penyewaan?"

>Analisis ini menyimpulkan bahwa kondisi cuaca adalah salah satu faktor paling signifikan yang mempengaruhi jumlah penyewaan sepeda. Kondisi optimal tercapai saat cuaca cerah atau berawan, yang menghasilkan penyewaan yang sangat tinggi. Sebaliknya, penyewaan mengalami penurunan drastis dalam kondisi hujan ringan atau salju. Hal ini menunjukkan bahwa pengguna cenderung menghindari bersepeda dalam cuaca yang tidak mendukung.
""")   

# Keterangan
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.markdown("---")
st.sidebar.write("""
                 Written by:  **Hanif Anandaputri**
                 """)

