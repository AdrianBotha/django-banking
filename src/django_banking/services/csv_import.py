import os
from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import connection, transaction

from django_banking.models import CSVImport, ProcessingStatus
from django_banking.settings import CSV_UPLOAD_DIR, SQL_DIR
from utils import sql_utils


def save_file(file: InMemoryUploadedFile) -> str:
    # Rename file to prevent duplicates
    datetime_str = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    new_file_name = f"{datetime_str}-{file}"
    with open(os.path.join(CSV_UPLOAD_DIR, new_file_name), 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return new_file_name


def log_file_upload(original_name: str, stored_name: str) -> CSVImport:
    pending_status = ProcessingStatus.objects.get(slug=ProcessingStatus.PROCESSING_SLUG)
    csv_import = CSVImport(original_name=original_name, stored_name=stored_name, processing_status=pending_status)
    csv_import.save()
    return csv_import


def import_trades_csv(csv_import: CSVImport):
    # To improve speed, I would chunkify the csv into groups of 1000 or so before importing them.
    file_path = os.path.join(CSV_UPLOAD_DIR, csv_import.stored_name)
    with transaction.atomic(), connection.cursor() as cur:
        # Create temp table
        sql_utils.run_sql_file(cur, os.path.join(SQL_DIR, 'create_temp_trades_import_table.sql'))

        # Populate temp table
        with open(file_path, 'r') as f:
            next(f, None)  # skip the headers
            cur.copy_from(f, 'temp_trades_import', sep=',')

        # Process and insert data into trades table
        sql_utils.run_sql_file(cur, os.path.join(SQL_DIR, 'import_trades.sql'))

        # Mark import as done
        csv_import.processed_at = datetime.now()
        csv_import.processing_status = ProcessingStatus.objects.get(slug=ProcessingStatus.PROCESSED_SLUG)
        csv_import.save()
