#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function untuk menampilkan pesan dengan format
print_message() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Function untuk memeriksa hasil dari perintah terakhir
check_status() {
  if [ $? -ne 0 ]; then
    print_message "ERROR: $1"
    exit 1
  else
    print_message "SUCCESS: $2"
  fi
}

# Memulai setup
print_message "MEMULAI SETUP CAPSTONE PROJECT MODULE 2"
print_message "========================================"

# Memeriksa apakah Docker berjalan
print_message "Memeriksa status Docker..."
if ! docker info > /dev/null 2>&1; then
  print_message "ERROR: Docker tidak berjalan. Silakan nyalakan Docker dan coba lagi."
  exit 1
fi

# Memulai container PostgreSQL
print_message "Memulai container PostgreSQL..."
docker-compose up -d
check_status "Gagal memulai container PostgreSQL" "Container PostgreSQL berhasil dimulai"

# Menunggu PostgreSQL siap
print_message "Menunggu PostgreSQL siap digunakan..."
sleep 10
print_message "Mencoba terhubung ke PostgreSQL..."
# Menambahkan pemeriksaan koneksi (opsional, tergantung pada konfigurasi docker-compose)
docker-compose exec -T postgres pg_isready 2>/dev/null || sleep 10
check_status "PostgreSQL tidak dapat diakses setelah menunggu" "PostgreSQL siap digunakan"

# Menginstall dependencies Python
print_message "Menginstall dependencies Python..."
pip install -r requirements.txt
check_status "Gagal menginstall dependencies Python" "Dependencies Python berhasil diinstall"

# Membuat direktori untuk data yang diproses jika belum ada
print_message "Menyiapkan direktori data..."
mkdir -p data/processed
check_status "Gagal membuat direktori data/processed" "Direktori data/processed siap"

# Setup database
print_message "Menyiapkan database..."
python src/python/setup_database.py
check_status "Gagal menyiapkan database" "Database berhasil disiapkan"

# Menyelesaikan setup
print_message "SETUP BERHASIL DISELESAIKAN!"
print_message "========================================"
print_message "Anda sekarang dapat menjalankan:"
print_message "1. Query SQL: python src/python/run_sql_queries.py"
print_message "2. ETL NY Taxi: python src/python/ny_taxi_etl.py --year 2024 --month 1 --source yellow"
print_message "========================================"