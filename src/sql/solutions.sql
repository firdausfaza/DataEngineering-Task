-- SQL Solutions for Capstone Project Module 2
-- table -> order,product,review user

-- 1. Hitunglah ada berapa banyak transaksi di table Order?
-- Aggregate COUNT pada kolom Id.
-- Catatan: Menggunakan fungsi COUNT untuk menghitung total transaksi
SELECT 
    COUNT(id) AS total_transactions  -- Menghitung jumlah id transaksi
FROM 
    ORDERS;  -- Table orders berisi data transaksi

-- 2. Hitunglah berapa jumlah Order dari seluruh transaksi di Table Order? 
-- Aggragate SUM pada kolom Total.
-- Catatan: Menggunakan fungsi SUM untuk menjumlahkan total order 1,5jt
SELECT 
    SUM(total) AS total_order_amount  -- Menjumlahkan kolom total
FROM 
    ORDERS;  -- Table orders berisi data transaksi

-- 3. Hitung 10 product yang sering memberikan discount di tabel Order berdasarkan produk Title dari table Products? 
-- Join table Order dengan table produk untuk mendapatkan produk Title, aggragete Count untuk mendapatkan total order dan grouping berdasarkan kolom Title dari Table Products. 
-- Urutkan dari total transaksi tertinggi - terendah. Tamplikan 10 product teratas.
-- Catatan: Menggunakan JOIN dan GROUP BY untuk mengelompokkan data
SELECT 
    p.title,
    COUNT(o.id) AS discount_count  -- Menghitung jumlah diskon per produk
FROM 
    ORDERS o
JOIN 
    PRODUCTS p ON o.product_id = p.id
WHERE 
    o.discount > 0  -- Filter hanya transaksi dengan diskon
GROUP BY 
    p.title
ORDER BY 
    discount_count DESC
LIMIT 10;

-- 4. Hitung berapa jumlah Order dari transaksi di Table Order, berdasarkan kolom category dari tabel produk? 
-- Gunakan Konsep CTE, Join table Order dengan table Product, Hitung total menggunakan aggregate SUM, dan grouping berdasarkan kolom Category dari table Product. 
-- Urutkan dari total transaksi tertinggi - terendah.
-- Catatan: Menggunakan CTE untuk memudahkan pembacaan query
-- oJOIN untuk menghubungkan data pesanan dengan kategori produk
-- oGROUP BY dengan SUM() untuk menghitung total per kategori
WITH order_by_category AS (
    SELECT 
        p.category,
        o.total
    FROM 
        ORDERS o
    JOIN 
        PRODUCTS p ON o.product_id = p.id
)
SELECT 
    category,
    SUM(total) AS total_order_amount  -- Menjumlahkan total per kategori
FROM 
    order_by_category
GROUP BY 
    category
ORDER BY 
    total_order_amount DESC;

-- 5. Hitung berapa jumlah total Order di table Order, dari setiap title di table Product yang memiliki rating >=4?
-- Gunakan Konsep CTE, Join table Order dengan table Product, Hitung total menggunakan aggregate SUM, dan grouping berdasarkan kolom Title dari table Product. 
-- Urutkan dari total transaksi tertinggi - terendah.
-- Catatan: Menggunakan CTE dan filter rating untuk produk berkualitas tinggi
   -- 
   
  -- oCTE dengan filter rating untuk memilih produk berkualitas
--JOIN untuk menghubungkan data pesanan dengan data produk
-- Filter WHERE untuk hanya mengambil produk dengan rating ≥4
WITH high_rated_products AS (
    SELECT 
        p.title,
        o.total
    FROM 
        ORDERS o
    JOIN 
        PRODUCTS p ON o.product_id = p.id
    WHERE 
        p.rating >= 4  -- Filter produk dengan rating tinggi
)
SELECT 
    title,
    SUM(total) AS total_order_amount
FROM 
    high_rated_products
GROUP BY 
    title
ORDER BY 
    total_order_amount DESC;

-- 6. Dapatkan list reviews berdasarkan ketagori produk = 'Doohickey', dimana rating dari table reviews <= 3? Dan urutkan berdasarkan table created_at di table reviews.
-- Gunakan Konsep CTE, Join table Reviews dengan table Product, select kolom created_at, body dan rating dari table reviews, dan filter product category dan rating reviews <= 3. 
-- Urutkan dari kolom created terbaru - terlama.
-- Catatan: Menggunakan CTE untuk filter review produk kategori Doohickey
WITH doohickey_reviews AS (
    SELECT 
        r.created_at,
        r.body,
        r.rating
    FROM 
        REVIEWS r
    JOIN 
        PRODUCTS p ON r.product_id = p.id
    WHERE 
        p.category = 'Doohickey' AND r.rating <= 3  -- Filter kategori dan rating rendah
)
SELECT 
    created_at,
    body,
    rating
FROM 
    doohickey_reviews
ORDER BY 
    created_at DESC;

-- 7. Ada berapa source di table Users?
-- Ambil unik data di kolom source dari table Users.
-- Catatan: Menggunakan DISTINCT untuk mendapatkan nilai unik
SELECT 
    DISTINCT source  -- Mengambil nilai unik dari kolom source
FROM 
    USERS;

-- 8. Hitung total user di table Users yang memiliki email dari gmail.com.
-- Rename kolom alias total_user_gmail.
-- Catatan: Menggunakan LIKE untuk filter email domain
SELECT 
    COUNT(id) AS total_user_gmail  -- Menghitung jumlah user dengan email gmail
FROM 
    USERS
WHERE 
    email LIKE '%gmail.com';  -- Filter email domain gmail.com

-- 9. Dapatkan list id, title, price, and created at dari table Products, dengan kriteria price antara 30 - 50, dan urutkan dari transaksi terbaru - terlama?
-- Catatan: Menggunakan BETWEEN untuk range harga
SELECT 
    id,
    title,
    price,
    created_at
FROM 
    PRODUCTS
WHERE 
    price BETWEEN 30 AND 50  -- Filter range harga produk
ORDER BY 
    created_at DESC;

-- 10. Dapatkan list Name, Email, Address, Birtdate dari table Users yang lahir diatas tahun 1997? Buatlah dalam format database views.
-- Catatan: Membuat VIEW untuk menyimpan query
CREATE OR REPLACE VIEW young_users AS
SELECT 
    name,
    email,
    address,
    birth_date
FROM 
    USERS
WHERE 
    EXTRACT(YEAR FROM birth_date::DATE) > 1997;

    



select * from young_users yu

-- 11. Dapatkan list id, created_at, title, category, dan vendor dari table products, yang memiliki title yang sama / title muncul dengan value yang sama sebanyak lebih dari 1 kali.
-- Gunakan format cte dan row_number dalam mengerjakan soal berikut.
-- Catatan: Menggunakan multiple CTE dan ROW_NUMBER untuk mendeteksi duplikat
   
   
   
 with counted_title AS(
SELECT
	id,
	created_at,
	title,
	category,
	vendor,
	ROW_NUMBER() OVER(PARTITION BY TITLE) AS "title_row_num",
	COUNT(*) OVER(PARTITION BY title) AS number_of_titles
FROM products p
),
multiple_title AS (
SELECT
	*
FROM counted_title
where number_of_titles > 1
)

SELECT * FROM multiple_title;