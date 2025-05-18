"""
Modul untuk operasi database
"""

import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def load_environment():
    """Memuat variabel lingkungan dari file .env"""
    try:
        load_dotenv()
        required_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Variabel lingkungan yang diperlukan tidak ditemukan: {', '.join(missing_vars)}")
        
        logging.info("Variabel lingkungan berhasil dimuat")
        
    except Exception as e:
        logging.error(f"Gagal memuat variabel lingkungan: {str(e)}")
        raise

def create_db_engine():
    """Membuat SQLAlchemy engine untuk operasi database"""
    try:
        connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(connection_string)
        logging.info("Database engine berhasil dibuat")
        return engine
    except Exception as e:
        logging.error(f"Error membuat database engine: {e}")
        raise

def create_taxi_table(engine, config):
    """Membuat atau memperbarui tabel taxi_trips"""
    try:
        # Buat tabel jika belum ada
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {config['database']['table_name']} (
            id SERIAL PRIMARY KEY,
            vendor_id INTEGER,
            pickup_datetime TIMESTAMP,
            dropoff_datetime TIMESTAMP,
            passenger_count INTEGER,
            trip_distance FLOAT,
            pickup_location_id INTEGER,
            rate_code INTEGER,
            store_and_fwd_flag TEXT,
            dropoff_location_id INTEGER,
            payment_type INTEGER,
            fare_amount FLOAT,
            extra FLOAT,
            mta_tax FLOAT,
            tip_amount FLOAT,
            tolls_amount FLOAT,
            improvement_surcharge FLOAT,
            total_amount FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_source TEXT,
            trip_date DATE
        )
        """
        
        # Query untuk menambahkan kolom baru jika belum ada
        # add_columns_query = f"""
        # DO $$
        # BEGIN
        #     IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        #                  WHERE table_name = '{config['database']['table_name']}' 
        #                  AND column_name = 'pickup_location_id') THEN
        #         ALTER TABLE {config['database']['table_name']} ADD COLUMN pickup_location_id INTEGER;
        #     END IF;
            
        #     IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
        #                  WHERE table_name = '{config['database']['table_name']}' 
        #                  AND column_name = 'dropoff_location_id') THEN
        #         ALTER TABLE {config['database']['table_name']} ADD COLUMN dropoff_location_id INTEGER;
        #     END IF;
        # END $$;
        # """
        
        # Query untuk membuat index
        create_index_query = f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_indexes 
                         WHERE tablename = '{config['database']['table_name']}' 
                         AND indexname = 'idx_taxi_trip_date') THEN
                CREATE INDEX idx_taxi_trip_date ON {config['database']['table_name']}(trip_date);
            END IF;
            
            IF NOT EXISTS (SELECT 1 FROM pg_indexes 
                         WHERE tablename = '{config['database']['table_name']}' 
                         AND indexname = 'idx_taxi_pickup_location') THEN
                CREATE INDEX idx_taxi_pickup_location ON {config['database']['table_name']}(pickup_location_id);
            END IF;
            
            IF NOT EXISTS (SELECT 1 FROM pg_indexes 
                         WHERE tablename = '{config['database']['table_name']}' 
                         AND indexname = 'idx_taxi_dropoff_location') THEN
                CREATE INDEX idx_taxi_dropoff_location ON {config['database']['table_name']}(dropoff_location_id);
            END IF;
        END $$;
        """
        
        with engine.connect() as conn:
            conn.execute(text(create_table_query))
            # conn.execute(text(add_columns_query))
            conn.execute(text(create_index_query))
            conn.commit()
            
        logging.info(f"Tabel {config['database']['table_name']} berhasil dibuat/diperbarui")
        
    except Exception as e:
        logging.error(f"Error saat membuat/memperbarui tabel: {e}")
        raise

def check_for_duplicates(engine, df, config):
    """Memeriksa duplikasi data"""
    try:
        if df.empty:
            logging.info("DataFrame kosong, tidak ada duplikasi")
            return False
            
        # Buat temporary table dengan nama yang unik
        temp_table_name = f"temp_taxi_trips_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Buat temporary table dengan index
        create_temp_table_query = f"""
        CREATE TEMPORARY TABLE {temp_table_name} (
            pickup_datetime TIMESTAMP,
            dropoff_datetime TIMESTAMP,
            vendor_id INTEGER,
            total_amount FLOAT,
            trip_date DATE
        ) ON COMMIT DROP
        """
        
        # Buat index untuk mempercepat pencarian
        create_index_query = f"""
        CREATE INDEX idx_temp_taxi_trips ON {temp_table_name} (pickup_datetime, dropoff_datetime, vendor_id, total_amount)
        """
        
        # Query untuk memeriksa dan menampilkan data duplikat berdasarkan hari dan bulan
        check_duplicates_query = f"""
        WITH duplicate_stats AS (
            SELECT 
                DATE_TRUNC('day', t1.pickup_datetime) as trip_day,
                DATE_TRUNC('month', t1.pickup_datetime) as trip_month,
                COUNT(*) as duplicate_count
            FROM {temp_table_name} t1
            JOIN {config['database']['table_name']} t2 ON 
                t1.pickup_datetime = t2.pickup_datetime AND
                t1.dropoff_datetime = t2.dropoff_datetime AND
                t1.vendor_id = t2.vendor_id AND
                t1.total_amount = t2.total_amount
            GROUP BY 
                DATE_TRUNC('day', t1.pickup_datetime),
                DATE_TRUNC('month', t1.pickup_datetime)
        )
        SELECT 
            trip_day,
            trip_month,
            duplicate_count
        FROM duplicate_stats
        ORDER BY trip_month, trip_day
        """
        
        # Eksekusi query dalam satu transaksi
        with engine.begin() as conn:
            conn.execute(text(create_temp_table_query))
            conn.execute(text(create_index_query))
            
            df[['pickup_datetime', 'dropoff_datetime', 'vendor_id', 'total_amount', 'trip_date']].to_sql(
                temp_table_name, 
                conn, 
                if_exists='append', 
                index=False
            )
            
            result = conn.execute(text(check_duplicates_query)).fetchall()
            
            if result:
                logging.warning("Ditemukan data duplikat:")
                current_month = None
                for row in result:
                    # Tampilkan header bulan jika berbeda
                    if current_month != row.trip_month:
                        current_month = row.trip_month
                        logging.warning(f"\nBulan: {current_month.strftime('%B %Y')}")
                    
                    logging.warning(f"  Tanggal: {row.trip_day.strftime('%d %B %Y')} - Jumlah duplikat: {row.duplicate_count}")
                return True
            else:
                logging.info("Tidak ditemukan data duplikat")
                return False
            
    except Exception as e:
        logging.error(f"Error dalam pemeriksaan duplikasi: {e}")
        return False

def load_data_to_db(engine, df, config):
    """Memuat data ke database dengan progress bar"""
    try:
        if df.empty:
            logging.warning("Tidak ada data untuk dimuat")
            return 0
        
        # Periksa duplikasi
        has_duplicates = check_for_duplicates(engine, df, config)
        if has_duplicates:
            logging.warning("Ditemukan data duplikat. Proses insert dibatalkan.")
            return 0
        
        # Hitung jumlah batch
        batch_size = config['database']['batch_size']
        total_rows = len(df)
        num_batches = (total_rows + batch_size - 1) // batch_size
        
        logging.info(f"Memulai proses insert {total_rows} baris data dalam {num_batches} batch")
        
        # Buat progress bar
        from tqdm import tqdm
        with tqdm(total=total_rows, desc="Inserting data", unit="rows") as pbar:
            rows_inserted = 0
            
            # Proses insert per batch
            for i in range(0, total_rows, batch_size):
                batch_df = df.iloc[i:i + batch_size]
                
                try:
                    # Insert batch ke database
                    batch_df.to_sql(config['database']['table_name'], engine, if_exists='append', index=False)
                    rows_inserted += len(batch_df)
                    
                    # Update progress bar
                    pbar.update(len(batch_df))
                    
                except Exception as e:
                    logging.error(f"Error saat insert batch {i//batch_size + 1}: {e}")
                    continue
        
        logging.info(f"Proses insert selesai: {rows_inserted} baris berhasil dimuat")
        return rows_inserted
        
    except Exception as e:
        logging.error(f"Error saat memuat data ke database: {e}")
        return 0 