CAPSTONE PROJECT MODULE 2

GENERAL INFORMATION

Pada Modul 2 siswa telah mempelajari Database dan SQL, beberapa materi yang telah dipelajari di antaranya adalah : 
PostgreSQL dan datamart concept.
Insert data into postgresql.
SQL Basic
Data Manipulation
Data Filtering and Aggregating
SQL Joins dan Subqueri
SQL Views and CTE’s
SQL Window Functions
SQL Ranking and Filtering


Pengerjaan project ini akan melatih siswa untuk lebih siap dan lebih memahami bahasa pemrogaman Python dan SQL function ketika diaplikasikan ke dalam bidang pekerjaan Data Engineering. 

Setiap siswa akan mengerjakan semua case study, dengan tahapan pengerjaan sebagai berikut : 
Download Guideline Modul 2 guna mengetahui apa yang harus dikerjakan oleh siswa.
Download folder master_capstone2 dan capstone_postgress dari Gdrive folder berikut : 
https://drive.google.com/drive/folders/1DMZ1R76DJOeXoHrHb5F7P3awEY1sA3tM

Setelah download folders, lakukan beberapa hal berikut : 
Open aplikasi docker dari local computer Anda, jalankan docker-compose.yaml yang tersedia di folder capstone_postgress.
Open aplikasi VSCode, buat koneksi baru menggunakan postgress, sesuaikan nama user, database, dan password yang ada pada docker-compose.yaml pada koneksi database di DBeaver

Untuk Soal Pertama, setelah database berhasil terkoneksi di DBeaver, Kerjakan soal-soal berikut menggunakan bahasa SQL : 
Hitunglah ada berapa banyak transaksi di table Order?
Aggregate COUNT pada kolom Id.
Hitunglah berapa jumlah Order dari seluruh transaksi di Table Order? 
Aggragate SUM pada kolom Total.
Hitung 10 product yang sering memberikan discount di tabel Order berdasarkan produk Title dari table Products? 
Join table Order dengan table produk untuk mendapatkan produk Title, aggragete Count untuk mendapatkan total order dan grouping berdasarkan kolom Title dari Table Products. Urutkan dari total transaksi tertinggi - terendah. Tamplikan 10 product teratas.
Hitung berapa jumlah Order dari transaksi di Table Order, berdasarkan kolom category dari tabel produk? 
Gunakan Konsep CTE, Join table Order dengan table Product, Hitung total menggunakan aggregate SUM, dan grouping berdasarkan kolom Category dari table Product. Urutkan dari total transaksi tertinggi - terendah.
Hitung berapa jumlah total Order di table Order, dari setiap title di table Product yang memiliki rating >=4?
Gunakan Konsep CTE, Join table Order dengan table Product, Hitung total menggunakan aggregate SUM, dan grouping berdasarkan kolom Title dari table Product. Urutkan dari total transaksi tertinggi - terendah.
Dapatkan list reviews berdasarkan ketagori produk = ‘Doohickey’, dimana rating dari table reviews <= 3? Dan urutkan berdasarkan table created_at di table reviews.
Gunakan Konsep CTE, Join table Reviews dengan table Product, select kolom created_at, body dan rating dari table reviews, dan filter product category dan rating reviews <= 3. Urutkan dari kolom created terbaru - terlama.
Ada berapa source di table Users?
Ambil unik data di kolom source dari table Users.
Hitung total user di table Users yang memiliki email dari gmail.com.
Rename kolom alias total_user_gmail.
Dapatkan list id, title, price, and created at dari table Products, dengan kriteria price antara 30 - 50, dan urutkan dari transaksi terbaru - terlama?
Dapatkan list Name, Email, Address, Birtdate dari table Users yang lahir diatas tahun 1997? Buatlah dalam format database views.
Dapatkan list id, created_at, title, category, dan vendor dari table products, yang memiliki title yang sama / title muncul dengan value yang sama sebanyak lebih dari 1 kali.
Gunakan format cte dan row_number dalam mengerjakan soal berikut.


Untuk soal kedua, gunakan data source NY Taxi Trip yang ada di Capstone 1. Kemudian kerjakan sesuai alur proyek soal berikut : 
Pilihlah salah satu data source, seperti : Yellow Taxi Trip Records, Green Taxi Trip Records, dan lainnya. 
Buatlah skrip python untuk ekstrak data, kemudian insert data ke dalam PostgreSQL.
Untuk proses ekstraksi data, setiap 1 kali program running, gunakan proses filter data per hari / per minggu / perbulan. 
Kemudian data hasil ekstraksi, masukkan / insert data ke dalam postgresql. Gunakan skema insert data / incremental proses. Data baru selalu di append / ditambahkan ke dalam tabel. Pastikan tidak ada hasil data yang duplicate.
Proses filter data berdasarkan rantang waktu bisa di set manual / otomatis.
Sediakan error handling dan validasi data dari setiap step / blok kode.

Untuk soal pertama, berikan catatan di setiap blok kode query jika diperlukan. Dan juga pada setiap fungsi sql diusahakan semua query fungsi menggunakan huruf Capital / CapsLock.
Untuk soal kedua, buatlah fungsi / catetan fungsi / catata blok kode di perlukan di dalam file project .py / .ipynb.
Buatlah dokumentasi hasil dari project yang anda kerjakan dengan format Google Document / lainnya.
Buatlah video dokumentasi / penjelasan hasil capstone project, dengan maksimal durasi selama 30 menit. Manfaatkan file dokumentasi google docs / di sesuaikan dengan cara and menjelaskan project.


Setelah mengikut tahapan pengerjaan, setiap tahapan akan memiliki bobot penilaian, diantaranya sebagai berikut : 

Poin Penilaian 
Video Penjelasan : Maksimal 20 Point
Kelengkapan project.
Google Document 
Penjelasan skrip SQL dan python, serta hasil pengerjaan project.
Hasil Proyek Soal pertama : Maksimal 60 Point
Kerjakan setiap soal query SQL
Hasil Proyek Soal kedua : Maksimal 20 Point


Case Study
Data Master Capstone 2
NY Taxi Trip


Waktu Pengerjaan
Lama waktu pengerjaan Capstone Project Module 2 adalah 15 hari kerja. Pengerjaan
akan terhitung sejak H+1 setelah pengumuman Guidline Project.
Contoh : 
Pengumanan capstone tanggal 21 April 2025, Hari Senin.
Pengerjaan mulai dari 23 April 2025, Hari Selasa. Karena tanggal 22 April 2025 adalah batas maksimal pengupulan project capstone 1.
Pengumpulan maksimal 19 Mei 2025 23:59:59, Hari Senin.


Metode Pengumpulan
Pengumpulan dilakukan dengan cara:
Unggah video penjelasan project ke dalam cloud storage (Youtube, Google
Drive, Dropbox) masing-masing siswa. Buka hak akses untuk publik.
Kirim ke email Mentor : Samsudiney@gmail.com dan melalui google form yang akan di sediakan oleh team purwadika.

Video penjelasan maksimal berdurasi 30 menit dan wajib mengaktifkan kamera
depan atau webcam, sehingga wajah siswa ada dalam rekaman video.

Mengisi Google Forms yang telah disediakan oleh operasional untuk
mencantumkan link video, link google document / cloud storage / link github.

Pastikan siswa menerima email konfirmasi bahwa siswa telah sukses melakukan
pengisian dan pengumpulan Google Forms Capstone Project Module 2 yang dikirim secara otomatis oleh sistem. Cek folder spam apabila e-mail tidak ada di
folder inbox.


Catatan

Jika siswa mengumpulkan Capstone Project Module 2 melewati tenggat waktu
yang sudah ditentukan, maka akan ada pengurangan poin untuk nilai akhir sebagai
berikut:
Telat 1 detik sampai 24 jam: nilai akhir dikurangi 10 poin
Telat 24 jam sampai 72 jam: nilai akhir dikurangi 20 poin
Telat lebih dari 72 jam: nilai akhir menjadi 0

- Segala bentuk plagiarisme tidak akan ditoleransi dan mutlak diberikan nilai 0.
- Di larang plagiat dan copy paste secara saklek dari AI. artinya pahami blok kode nya, dan jelaskan sesuai pemahaman anda.



