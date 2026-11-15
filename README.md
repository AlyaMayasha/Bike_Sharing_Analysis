# Bike Sharing Analysis Dashboard

## Deskripsi Proyek

Proyek ini merupakan analisis data penyewaan sepeda menggunakan **Bike Sharing Dataset**. Analisis dilakukan untuk mengidentifikasi pola penyewaan sepeda berdasarkan waktu, musim, hari kerja, dan kondisi cuaca selama periode 2011–2012.

Hasil analisis disajikan melalui notebook Jupyter dan dashboard interaktif menggunakan Streamlit.

## Tujuan Analisis

Proyek ini bertujuan untuk menjawab tiga pertanyaan bisnis:

1. Bagaimana pola rata-rata penyewaan sepeda berdasarkan bulan dan musim?
2. Bagaimana pola penyewaan sepeda berdasarkan jam pada hari kerja dibandingkan hari non-kerja?
3. Bagaimana perbedaan rata-rata penyewaan sepeda berdasarkan kondisi cuaca?

## Dataset

Dataset yang digunakan adalah Bike Sharing Dataset, yang terdiri dari:

- `day.csv`: data penyewaan sepeda harian.
- `hour.csv`: data penyewaan sepeda per jam.

Periode data: 1 Januari 2011–31 Desember 2012.

## Tahapan Analisis

1. **Data Wrangling:** pengumpulan, pemeriksaan kualitas, dan pembersihan data.
2. **Exploratory Data Analysis (EDA):** eksplorasi pola penyewaan berdasarkan bulan, musim, jam, hari kerja, dan kondisi cuaca.
3. **Analisis Lanjutan:** pengelompokan tingkat permintaan penyewaan harian menggunakan teknik binning berdasarkan tertil distribusi data.
4. **Visualisasi:** penyajian hasil analisis melalui grafik dan dashboard interaktif.

## Fitur Dashboard

Dashboard Streamlit menyediakan:

- Ringkasan total penyewaan dan rata-rata penyewaan harian.
- Filter rentang tanggal.
- Visualisasi pola penyewaan bulanan dan musiman.
- Perbandingan pola penyewaan per jam antara hari kerja dan non-kerja.
- Analisis rata-rata penyewaan berdasarkan kondisi cuaca.
- Pengelompokan tingkat permintaan menjadi rendah, sedang, dan tinggi.
- Insight dan rekomendasi bisnis.
- Preview dataset harian dan per jam.

## Struktur Proyek

```text
Bike_Sharing_Analysis/
├── .streamlit/
│   └── config.toml
├── data/
│   ├── day.csv
│   └── hour.csv
├── dashboard.py
├── notebook.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

## Instalasi dan Menjalankan Dashboard

### 1. Clone repository

```bash
git clone URL_REPOSITORY
```

### 2. Masuk ke folder proyek

```bash
cd Bike_Sharing_Analysis
```

### 3. Buat virtual environment

```bash
python -m venv .venv
```

### 4. Aktifkan virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instal dependencies

```bash
pip install -r requirements.txt
```

### 6. Jalankan dashboard

```bash
streamlit run dashboard.py
```

Dashboard akan tersedia melalui browser pada alamat:

```text
http://localhost:8501
```

## Teknologi yang Digunakan

- Python
- Pandas
- Matplotlib
- Streamlit
- Jupyter Notebook

## Catatan

Dataset yang digunakan mencakup periode 2011–2012. Oleh karena itu, hasil analisis menggambarkan pola historis pada periode tersebut dan tidak secara langsung merepresentasikan kondisi penyewaan sepeda saat ini.

Pengelompokan tingkat permintaan menggunakan teknik binning tertil pada data dalam rentang tanggal yang dipilih.

---

**Bike Sharing Analysis Project**  
Data Analysis Project
