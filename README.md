# Capstone Project Module 2 - Data Engineering

Repository ini berisi solusi untuk Capstone Project Module 2, yang berfokus pada PostgreSQL dan proses ETL dengan data NY Taxi Trip.

## Background Project

### Latar Belakang
Proyek ini dikembangkan sebagai bagian dari Capstone Project Module 2 di Purwadhika Digital Technology School, yang berfokus pada pengembangan keterampilan Data Engineering. Proyek ini menggunakan dataset NY Taxi Trip yang merupakan data publik dari New York City Taxi and Limousine Commission (TLC). Project ini bertujuan untuk membangun pipeline ETL yang efisien dan scalable untuk memproses data taxi trip, serta menyimpannya dalam database PostgreSQL.
Dataset ini berisi informasi tentang perjalanan taksi di New York City, termasuk waktu penjemputan dan pengantaran, jarak tempuh, jumlah penumpang, dan informasi pembayaran. Data ini sangat berguna untuk analisis transportasi, perencanaan kota, dan penelitian akademis.

### Teknologi yang Digunakan
- **Database**: PostgreSQL
- **Container**: Docker & Docker Compose
- **Programming Language**: Python 3.8+
- **Data Processing**: Pandas, SQLAlchemy
- **Version Control**: Git
- **Environment Management**: Virtual Environment

### Manfaat
1. **Efisiensi Data Processing**:
   - Otomatisasi proses ETL
   - Pengurangan waktu pemrosesan data
   - Optimasi penggunaan sumber daya

2. **Kualitas Data**:
   - Validasi data yang ketat
   - Pencegahan data duplikat
   - Konsistensi data terjamin

3. **Skalabilitas**:
   - Kemampuan menangani data dalam skala besar
   - Mudah dikembangkan untuk kebutuhan masa depan
   - Fleksibel untuk berbagai jenis data taxi

4. **Maintainability**:
   - Kode yang terstruktur dan terdokumentasi
   - Mudah di-debug dan di-maintain
   - Logging yang informatif untuk troubleshooting

## Diagram Proyek

### Diagram Alur ETL
```
┌─────────────┐
│    Start    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Download   │
│    Data     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ File Exists?│
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌─────┐
│ Yes │ │ No  │
└──┬──┘ └──┬──┘
   │       │
   ▼       ▼
┌─────┐ ┌─────┐
│Skip │ │Download│
└──┬──┘ └──┬──┘
   │       │
   └───┬───┘
       │
       ▼
┌─────────────┐
│ Load Data   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Transform   │
│   Data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Validate   │
│   Data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Duplicate?  │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌─────┐
│ Yes │ │ No  │
└──┬──┘ └──┬──┘
   │       │
   ▼       ▼
┌─────┐ ┌─────────────┐
│ Log │ │ Load to DB  │
└──┬──┘ └──────┬──────┘
   │           │
   └─────┬─────┘
         │
         ▼
┌─────────────┐
│    End      │
└─────────────┘
```

### Diagram Arsitektur Sistem
```
┌─────────────────────────────────────────────────────────────┐
│                      Data Sources                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    TLC Website                       │  │
│  └──────────────────────────┬───────────────────────────┘  │
└──────────────────────────────┼──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      ETL Process                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Python    │    │  Data       │    │  Data       │     │
│  │  Scripts    │───▶│ Validation  │───▶│Transform    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Storage                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Raw Data  │    │ Processed   │    │ PostgreSQL  │     │
│  │  (Parquet)  │    │ Data        │    │ Database    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Monitoring                              │
│  ┌─────────────┐    ┌─────────────┐                        │
│  │  Logging    │    │   Error     │                        │
│  │  System     │    │  Handling   │                        │
│  └─────────────┘    └─────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Struktur Database
```
┌─────────────────────────────────────────────────────────────┐
│                      TAXI_TRIPS                            │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                │ SERIAL                            │
│ vendor_id             │ INTEGER                           │
│ pickup_datetime       │ TIMESTAMP                         │
│ dropoff_datetime      │ TIMESTAMP                         │
│ passenger_count       │ INTEGER                           │
│ trip_distance         │ FLOAT                             │
│ pickup_location_id    │ INTEGER                           │
│ rate_code            │ INTEGER                           │
│ store_and_fwd_flag   │ TEXT                              │
│ dropoff_location_id  │ INTEGER                           │
│ payment_type         │ INTEGER                           │
│ fare_amount          │ FLOAT                             │
│ extra                │ FLOAT                             │
│ mta_tax              │ FLOAT                             │
│ tip_amount           │ FLOAT                             │
│ tolls_amount         │ FLOAT                             │
│ improvement_surcharge│ FLOAT                             │
│ total_amount         │ FLOAT                             │
│ created_at           │ TIMESTAMP                         │
│ data_source          │ TEXT                              │
│ trip_date            │ DATE                              │
└─────────────────────────────────────────────────────────────┘
```

### Proses Validasi Duplikasi
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    ETL      │     │   Temp      │     │  Database   │
│  Process    │     │   Table     │     │             │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │  Create Table     │                   │
       │─────────────────▶│                   │
       │                   │                   │
       │  Insert Data      │                   │
       │─────────────────▶│                   │
       │                   │                   │
       │  Check Duplicates │                   │
       │──────────────────────────────────────▶│
       │                   │                   │
       │  Return Result    │                   │
       │◀──────────────────────────────────────│
       │                   │                   │
       │  If Duplicate:    │                   │
       │  Log Details      │                   │
       │                   │                   │
       │  If No Duplicate: │                   │
       │  Insert to DB     │                   │
       │──────────────────────────────────────▶│
       │                   │                   │
┌──────┴──────┐     ┌──────┴──────┐     ┌──────┴──────┐
│    ETL      │     │   Temp      │     │  Database   │
│  Process    │     │   Table     │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Struktur Proyek

```
.
├── docker-compose.yml      # Konfigurasi Docker untuk PostgreSQL
├── .env                    # Variabel lingkungan untuk koneksi database
├── setup.sh               # Script setup untuk environment
├── data/                  # Folder untuk menyimpan data
│   ├── raw/              # Data mentah yang diunduh
│   └── processed/        # Data yang sudah diproses
├── src/                   # Kode sumber
│   ├── sql/              # File SQL
│   │   └── solutions.sql # Query SQL untuk Bagian 1
│   └── python/           # Script Python
│       └── ny_taxi_etl.py # Script ETL untuk data NY Taxi
├── sql/                   # File SQL untuk setup database
├── requirements.txt       # Daftar dependensi Python
└── README.md             # File ini
```

## Instruksi Setup

### Prasyarat

- Docker dan Docker Compose
- Python 3.8+
- Virtual Environment Python
- Ruang disk minimal 10GB (untuk menyimpan data)

### Instalasi

1. Clone repository ini:
   ```bash
   git clone <repository-url>
   cd capstone2
   ```

2. Buat dan aktifkan virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   # atau
   .\venv\Scripts\activate  # Untuk Windows
   ```

3. Install dependensi Python:
   ```bash
   pip install -r requirements.txt
   ```

4. Konfigurasi variabel lingkungan:
   Buat file `.env` dengan konfigurasi berikut:
   ```
   # Konfigurasi Database
   DB_HOST=localhost
   DB_PORT=5434
   DB_NAME=project_capstone
   DB_USER=project_capstone
   DB_PASSWORD=purwadika_capstone_two
   
   # Konfigurasi Logging
   LOG_LEVEL=INFO
   LOG_FILE=ny_taxi_etl.log
   ```

5. Jalankan container PostgreSQL:
   ```bash
   docker-compose up -d
   ```

## Penggunaan ETL NY Taxi Trip

Script ETL untuk data NY Taxi Trip diimplementasikan dalam `src/python/ny_taxi_etl.py`. Script ini:

1. Mengunduh data NY Taxi Trip dari website TLC
2. Menyimpan data mentah dalam format parquet di folder `data/raw`
3. Mentransformasi data sesuai skema database
4. Memuat data ke PostgreSQL
5. Menangani loading inkremental dan mencegah duplikasi

### Cara Penggunaan

```bash
python src/python/ny_taxi_etl.py --start-date 2023-01-01 --end-date 2023-02-28 --source yellow
```

Parameter:
- `--start-date`: Tanggal awal dalam format YYYY-MM-DD
- `--end-date`: Tanggal akhir dalam format YYYY-MM-DD
- `--source`: Sumber data (`yellow` atau `green`)

### Fitur Utama

1. **Proses ETL Otomatis**:
   - Mengunduh data untuk rentang tanggal yang ditentukan
   - Menyimpan data mentah dalam format parquet
   - Transformasi data otomatis
   - Pencegahan data duplikat
   - Logging yang informatif

2. **Manajemen Data**:
   - Data mentah disimpan di folder `data/raw`
   - Data yang sudah diproses disimpan di folder `data/processed`
   - Pengecekan file yang sudah ada untuk menghindari pengunduhan ulang
   - Verifikasi integritas file yang diunduh

3. **Penanganan Error**:
   - Validasi input
   - Penanganan error untuk setiap langkah
   - Logging error yang detail
   - Pembersihan file yang rusak

4. **Incremental Loading**:
   - Memproses data bulan per bulan
   - Dapat melanjutkan dari bulan yang gagal
   - Pencegahan duplikasi data

5. **Validasi Duplikasi Data**:
   - Pengecekan duplikasi berdasarkan pickup_datetime, dropoff_datetime, vendor_id, dan total_amount
   - Laporan duplikasi dikelompokkan berdasarkan bulan dan hari
   - Format log yang mudah dibaca dengan informasi jumlah duplikasi per hari
   - Contoh format log:
     ```
     Ditemukan data duplikat:
     
     Bulan: Januari 2024
       Tanggal: 15 Januari 2024 - Jumlah duplikat: 3
       Tanggal: 16 Januari 2024 - Jumlah duplikat: 2
     ```
   - Mencegah insert data duplikat ke database

### Catatan Penting

- Script akan membuat tabel `taxi_trips` jika belum ada
- Data baru akan ditambahkan ke tabel yang ada (append)
- Log proses disimpan di file `ny_taxi_etl.log`
- Pastikan koneksi database aktif sebelum menjalankan script
- Pastikan ada cukup ruang disk untuk menyimpan data

## Koneksi Database

- Host: localhost
- Port: 5434
- Database: project_capstone
- User: project_capstone
- Password: purwadika_capstone_two

## Dokumentasi

Untuk dokumentasi lebih detail, silakan merujuk ke:
1. Google Document yang berisi penjelasan lengkap
2. Video presentasi yang menjelaskan implementasi
3. Log file untuk detail proses ETL

## Troubleshooting

1. **Error Koneksi Database**:
   - Pastikan container PostgreSQL berjalan
   - Periksa konfigurasi di file `.env`
   - Pastikan port tidak digunakan oleh aplikasi lain

2. **Error Download Data**:
   - Periksa koneksi internet
   - Pastikan URL data masih valid
   - Periksa format tanggal yang digunakan
   - Pastikan ada cukup ruang disk

3. **Error Transformasi Data**:
   - Periksa format data yang diunduh
   - Pastikan semua kolom yang diperlukan ada
   - Periksa tipe data yang sesuai

4. **Error Penyimpanan Data**:
   - Pastikan folder `data/raw` dan `data/processed` ada
   - Periksa permission folder
   - Pastikan ada cukup ruang disk 