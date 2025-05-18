# Struktur Database untuk Capstone Project Module 2

Dokumen ini menjelaskan skema database yang digunakan dalam Capstone Project Module 2.

## Tabel Products

Berisi informasi tentang produk yang tersedia untuk dijual.

| Kolom      | Tipe Data    | Deskripsi                               |
|------------|--------------|------------------------------------------|
| id         | bigserial    | Primary key untuk mengidentifikasi produk |
| created_at | timestamp    | Waktu pembuatan record                    |
| category   | text         | Kategori produk                           |
| ean        | text         | European Article Number (barcode)         |
| price      | float        | Harga produk                              |
| quantity   | int          | Jumlah stok (default: 5000)               |
| rating     | float        | Rating produk                             |
| title      | text         | Nama/judul produk                         |
| vendor     | text         | Nama vendor/penyedia produk               |

## Tabel Users

Berisi informasi tentang pengguna dalam sistem.

| Kolom      | Tipe Data    | Deskripsi                               |
|------------|--------------|------------------------------------------|
| id         | bigserial    | Primary key untuk mengidentifikasi user  |
| created_at | timestamp    | Waktu pembuatan record                   |
| name       | text         | Nama pengguna                            |
| email      | text         | Alamat email pengguna                    |
| address    | text         | Alamat fisik pengguna                    |
| city       | text         | Kota tempat tinggal                      |
| state      | text         | Provinsi/negara bagian                   |
| zip        | text         | Kode pos                                 |
| birth_date | text         | Tanggal lahir                            |
| latitude   | float        | Latitude lokasi pengguna                 |
| longitude  | float        | Longitude lokasi pengguna                |
| password   | text         | Password pengguna (sebaiknya di-hash)    |
| source     | text         | Sumber registrasi pengguna               |

## Tabel Orders

Berisi informasi tentang pesanan yang dibuat oleh pengguna.

| Kolom      | Tipe Data    | Deskripsi                               |
|------------|--------------|------------------------------------------|
| id         | bigserial    | Primary key untuk mengidentifikasi order |
| created_at | timestamp    | Waktu pembuatan order                    |
| user_id    | bigint       | Foreign key ke tabel Users               |
| product_id | bigint       | Foreign key ke tabel Products            |
| discount   | float        | Jumlah diskon yang diberikan             |
| quantity   | int          | Jumlah produk yang dipesan               |
| subtotal   | float        | Subtotal harga sebelum pajak             |
| tax        | float        | Jumlah pajak yang dikenakan              |
| total      | float        | Total harga final                        |

## Tabel Reviews

Berisi informasi tentang ulasan produk dari pengguna.

| Kolom      | Tipe Data    | Deskripsi                               |
|------------|--------------|------------------------------------------|
| id         | bigserial    | Primary key untuk mengidentifikasi review|
| created_at | timestamp    | Waktu pembuatan review                   |
| reviewer   | text         | Nama reviewer                            |
| product_id | bigint       | Foreign key ke tabel Products            |
| rating     | int          | Rating yang diberikan (skala angka)      |
| body       | text         | Isi ulasan                               |

