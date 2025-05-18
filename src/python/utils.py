"""
Modul utilitas untuk ETL NY Taxi
"""

import os
import logging
import yaml
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_config():
    """Memuat konfigurasi dari file YAML"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_logging(config):
    """Setup logging berdasarkan konfigurasi"""
    logging.basicConfig(
        level=getattr(logging, config['logging']['level']),
        format=config['logging']['format'],
        handlers=[
            logging.FileHandler(config['logging']['file']),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def setup_data_directories():
    """Membuat direktori untuk menyimpan data jika belum ada"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    raw_dir = os.path.join(data_dir, 'raw')
    processed_dir = os.path.join(data_dir, 'processed')
    
    for directory in [data_dir, raw_dir, processed_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Direktori {directory} berhasil dibuat")

def get_file_path(year, month, data_source):
    """Mendapatkan path file untuk data tertentu"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    raw_dir = os.path.join(data_dir, 'raw')
    return os.path.join(raw_dir, f"{data_source}_tripdata_{year}-{month:02d}.parquet")

def generate_date_ranges(start_date, end_date):
    """
    Menghasilkan daftar tahun dan bulan berdasarkan rentang tanggal
    
    Args:
        start_date (datetime): Tanggal awal
        end_date (datetime): Tanggal akhir
    
    Returns:
        list: Daftar tuple (tahun, bulan)
    """
    date_ranges = []
    current = start_date
    
    while current <= end_date:
        date_ranges.append((current.year, current.month))
        current += relativedelta(months=1)
    
    return date_ranges 