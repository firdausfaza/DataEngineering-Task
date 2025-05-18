"""
Modul untuk pemrosesan data NY Taxi
"""

import logging
import pandas as pd
import requests
from datetime import datetime
from utils import get_file_path
import os

def download_taxi_data(year, month, data_source, config):
    """Download taxi trip data untuk tahun dan bulan tertentu"""
    try:
        # Format URL berdasarkan sumber data dan tanggal
        url = config['data']['sources'][data_source]['url_template'].format(
            year=year, month=month
        )
        
        # Dapatkan path file
        file_path = get_file_path(year, month, data_source)
        
        # Cek apakah file sudah ada
        if os.path.exists(file_path):
            logging.info(f"File sudah ada di {file_path}")
            return pd.read_parquet(file_path)
        
        logging.info(f"Mengunduh data {data_source} untuk {year}-{month:02d}")
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            # Simpan file ke disk
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verifikasi file yang diunduh
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                logging.error("File yang diunduh kosong")
                os.remove(file_path)
                return None
            
            logging.info(f"File berhasil disimpan di {file_path}")
            return pd.read_parquet(file_path)
        else:
            logging.error(f"Gagal mengunduh data: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"Error mengunduh data taksi: {e}")
        return None

def transform_taxi_data(df, data_source, config):
    """Transform taxi trip data to match our database schema"""
    try:
        logging.info("Transforming taxi data")
        
        # Make a copy to avoid modifying the original DataFrame
        transformed_df = df.copy()
        
        # Get datetime column names from config
        datetime_cols = config['data']['sources'][data_source]['datetime_columns']
        
        # Map datetime columns
        transformed_df['pickup_datetime'] = df[datetime_cols['pickup']]
        transformed_df['dropoff_datetime'] = df[datetime_cols['dropoff']]
        
        # Map other columns
        column_mapping = {
            'VendorID': 'vendor_id',
            'passenger_count': 'passenger_count',
            'trip_distance': 'trip_distance',
            'RatecodeID': 'rate_code',
            'store_and_fwd_flag': 'store_and_fwd_flag',
            'payment_type': 'payment_type',
            'fare_amount': 'fare_amount',
            'extra': 'extra',
            'mta_tax': 'mta_tax',
            'tip_amount': 'tip_amount',
            'tolls_amount': 'tolls_amount',
            'improvement_surcharge': 'improvement_surcharge',
            'total_amount': 'total_amount',
            'PULocationID': 'pickup_location_id',
            'DOLocationID': 'dropoff_location_id'
        }
        
        # Rename columns based on mapping
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                transformed_df[new_col] = df[old_col]
        
        # Add data source and trip date columns
        transformed_df['data_source'] = data_source
        transformed_df['trip_date'] = pd.to_datetime(transformed_df['pickup_datetime']).dt.date
        
        # Drop duplicate rows
        transformed_df = transformed_df.drop_duplicates()
        
        # Select only the required columns
        result_df = pd.DataFrame()
        for col in config['data']['columns']['required']:
            if col in transformed_df.columns:
                result_df[col] = transformed_df[col]
            else:
                result_df[col] = None
        
        logging.info(f"Transformation complete: {result_df.shape[0]} rows")
        return result_df
    
    except Exception as e:
        logging.error(f"Error transforming taxi data: {e}")
        return None

def filter_data_by_date(df, start_date=None, end_date=None):
    """Filter data by date range"""
    try:
        if start_date and end_date:
            logging.info(f"Filtering data from {start_date} to {end_date}")
            mask = (df['trip_date'] >= start_date) & (df['trip_date'] <= end_date)
            filtered_df = df[mask]
            logging.info(f"Filtered data: {filtered_df.shape[0]} rows")
            return filtered_df
        else:
            logging.info("No date filtering applied")
            return df
    except Exception as e:
        logging.error(f"Error filtering data by date: {e}")
        return df 