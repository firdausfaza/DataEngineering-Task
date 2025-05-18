#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NY Taxi Trip ETL Script
Script utama untuk proses ETL data NY Taxi Trip
"""

import sys
import argparse
from datetime import datetime
import logging

from utils import load_config, setup_logging, setup_data_directories, generate_date_ranges
from database import load_environment, create_db_engine, create_taxi_table, load_data_to_db
from data_processor import download_taxi_data, transform_taxi_data, filter_data_by_date

def run_etl(year, month, data_source, config, start_date=None, end_date=None):
    """Run the ETL process for a specific year and month"""
    try:
        logging.info(f"Starting ETL process for {data_source} taxi data: {year}-{month:02d}")
        
        # Create database engine
        engine = create_db_engine()
        
        # Create taxi_trips table if it doesn't exist
        create_taxi_table(engine, config)
        
        # Extract data
        df = download_taxi_data(year, month, data_source, config)
        if df is None or df.empty:
            logging.error("No data extracted. ETL process aborted.")
            return False
        
        # Transform data
        transformed_df = transform_taxi_data(df, data_source, config)
        if transformed_df is None or transformed_df.empty:
            logging.error("Data transformation failed. ETL process aborted.")
            return False
        
        # Filter data by date if specified
        if start_date or end_date:
            filtered_df = filter_data_by_date(transformed_df, start_date, end_date)
        else:
            filtered_df = transformed_df
        
        # Load data to database
        rows_inserted = load_data_to_db(engine, filtered_df, config)
        
        logging.info(f"ETL process completed for {data_source} taxi data: {year}-{month:02d}")
        return rows_inserted > 0
    
    except Exception as e:
        logging.error(f"Error in ETL process: {e}")
        return False

def run_etl_for_date_range(start_date, end_date, data_source, config):
    """Run ETL process for a date range"""
    try:
        # Generate list of year-month combinations
        date_ranges = generate_date_ranges(start_date, end_date)
        logging.info(f"Memproses data untuk {len(date_ranges)} bulan")
        
        total_rows_inserted = 0
        success_count = 0
        
        for year, month in date_ranges:
            logging.info(f"Memproses data untuk {year}-{month:02d}")
            
            # Run ETL for each month
            success = run_etl(year, month, data_source, config, start_date.date(), end_date.date())
            
            if success:
                success_count += 1
                logging.info(f"Berhasil memproses data untuk {year}-{month:02d}")
            else:
                logging.error(f"Gagal memproses data untuk {year}-{month:02d}")
        
        logging.info(f"Total bulan yang berhasil diproses: {success_count} dari {len(date_ranges)}")
        return success_count > 0
    
    except Exception as e:
        logging.error(f"Error dalam proses ETL untuk rentang tanggal: {e}")
        return False

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='NY Taxi Trip ETL Process')
    parser.add_argument('--start-date', type=str, required=True, 
                      help='Tanggal awal dalam format YYYY-MM-DD')
    parser.add_argument('--end-date', type=str, required=True, 
                      help='Tanggal akhir dalam format YYYY-MM-DD')
    parser.add_argument('--source', type=str, default='yellow', 
                      choices=['yellow', 'green'], 
                      help='Sumber data (yellow atau green)')
    
    return parser.parse_args()

def main():
    """Fungsi utama yang menjalankan proses ETL"""
    try:
        # Load konfigurasi
        config = load_config()
        
        # Setup logging
        logger = setup_logging(config)
        logger.info("Memulai proses ETL")
        
        # Setup direktori data
        setup_data_directories()
        
        # Memuat variabel lingkungan
        load_environment()
        
        # Parse command-line arguments
        args = parse_arguments()
        
        # Convert date strings to datetime objects
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        
        # Validate date range
        if start_date > end_date:
            logger.error("Tanggal awal harus lebih kecil dari tanggal akhir")
            sys.exit(1)
        
        # Run the ETL process for the date range
        success = run_etl_for_date_range(start_date, end_date, args.source, config)
        
        if success:
            logger.info("Proses ETL selesai dengan sukses")
            sys.exit(0)
        else:
            logger.error("Proses ETL gagal")
            sys.exit(1)
            
    except ValueError as e:
        logger.error(f"Format tanggal tidak valid: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Terjadi kesalahan dalam proses ETL: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 