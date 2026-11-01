# 🚆 End-to-End Commuter Life Satisfaction ETL Pipeline

Sebuah proyek pipeline data sederhana yang mengekstrak, membersihkan, mentransformasikan, dan memuat data survei kepuasan hidup komuter perkotaan ke dalam basis data **PostgreSQL** yang terisolasi menggunakan **Docker** dan **Docker Compose**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Desktop-2496ED?logo=docker)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas)

---

## 📌 1. Business Understanding

### Latar Belakang
Di kawasan metropolitan (seperti Jabodetabek), jutaan pekerja menghabiskan waktu 1 hingga 4 jam setiap hari untuk perjalanan pulang-pergi (*commuting*). Kondisi perjalanan—seperti pemilihan moda transportasi, waktu tempuh, dan tingkat kepadatan—berpengaruh langsung terhadap tingkat stres dan kesejahteraan psikologis (*Subjective Well-Being*).

### Masalah
Data survei mentah sering kali menggunakan kode kuesioner numerik (`a1`, `a2`, `b1`), memiliki nilai kosong (*missing values*), serta format tidak terstandarisasi. Hal ini menyulitkan para pengambil keputusan dan analis data untuk langsung menggunakannya.

### Tujuan Proyek
- Mengotomatisasi alur **Extract, Transform, Load (ETL)** secara terstruktur tanpa alat orkestrasi berat (*lightweight pipeline*).
- Melakukan *semantic transformation* (mengubah kode angka menjadi label deskriptif yang mudah dipahami).
- Menyediakan basis data analitik terpusat (*Single Source of Truth*) di PostgreSQL menggunakan container Docker.

---

## 🏗️ 2. Arsitektur Pipeline

```text
[ data_commuter.csv ] (Dataset Mentah Kaggle)
         │
         ▼ (Extract)
    [ Pandas DataFrame ]
         │
         ▼ (Transform)
    ├── Standarisasi nama kolom ke snake_case
    ├── Semantic Renaming (a1 -> kode_gender, a2 -> usia, b1 -> kode_transportasi)
    ├── Mapping kode angka ke label (1 -> 'Laki-laki', 4 -> 'KRL Commuter Line')
    └── Age Binning (<25, 25-40, 41-60, >60 tahun)
         │
         ▼ (Load via SQLAlchemy)
[ PostgreSQL Database (Container Docker) ]
```

---

## 📊 3. Ringkasan Temuan Data (Key Insights)

Berdasarkan 384 responden komuter perkotaan:
- **Dominasi KRL**: Sebanyak **61.7% komuter (237 responden)** mengandalkan moda transportasi **KRL Commuter Line**, menjadikannya tulang punggung mobilitas harian.
- **Demografi Responden**: Terdiri dari **74.2% Laki-laki** (285 responden) dan **25.8% Perempuan** (99 responden).
- **Usia Produktif**: Mayoritas komuter berada pada kelompok usia produktif **25–40 tahun**.

---

## 📁 4. Struktur Proyek

```text
commuter-etl/
├── data/
│   └── data_commuter.csv      # File dataset mentah
├── src/
│   └── etl.py                 # Script ETL (Extract, Transform, Load)
├── Dockerfile                 # Konfigurasi container environment Python
├── docker-compose.yml         # Orkestrasi PostgreSQL & runner ETL
├── requirements.txt           # Dependensi pustaka Python
├── .gitignore                 # Filter file sampah/cache Git
└── README.md                  # Dokumentasi proyek
```

---

## 🚀 5. Cara Menjalankan Proyek

### Prasyarat:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) sudah terinstal dan dalam kondisi aktif (*running*).

### Langkah Menjalankan:
1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/USERNAME_ANDA/commuter-etl.git
   cd commuter-etl
   ```

2. **Jalankan pipeline dan database dengan satu perintah:**
   ```bash
   docker compose up --build
   ```

3. **Verifikasi data hasil transformasi di PostgreSQL:**
   ```bash
   docker exec -it postgres_commuter psql -U postgres -d commuter_db -c "SELECT usia, kelompok_usia, jenis_kelamin, nama_transportasi FROM dim_kepuasan_komuter LIMIT 5;"
   ```

4. **Menghentikan container:**
   ```bash
   docker compose down
   ```

---

## 📤 6. Panduan Publikasi ke GitHub

Untuk mengunggah proyek ini ke akun GitHub pribadi:

1. Buat repository baru di [GitHub](https://github.com/new) dengan nama `commuter-etl` (tanpa mencentang opsi *Add README*).
2. Jalankan perintah berikut di terminal:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commuter etl pipeline with docker and postgres"
   git branch -M main
   git remote add origin https://github.com/USERNAME_ANDA/commuter-etl.git
   git push -u origin main
   ```