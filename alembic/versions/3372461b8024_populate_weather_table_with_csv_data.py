"""populate weather table with csv data

Revision ID: 3372461b8024
Revises: 222c78fa18ab
Create Date: 2023-01-06 16:12:38.782055

"""
import csv
import os
from datetime import datetime
from os.path import dirname, join

import sqlalchemy as sa

from alembic import op
from core.logger import get_logger

# revision identifiers, used by Alembic.
revision = "3372461b8024"
down_revision = "222c78fa18ab"
branch_labels = None
depends_on = None

current_dir = dirname(__file__)
logger = get_logger()


def upgrade() -> None:
    start_time = datetime.now()
    # TODO: implement parallel version because it can be done in parallel but we dont need to do such for now
    files_list = list(os.listdir(join(current_dir, "../wx_data")))
    counter = 0
    total_files = len(files_list)

    for csv_file_name in files_list:
        counter += 1
        if csv_file_name[:3] != "UCS" and csv_file_name[-4:] != ".txt":
            # invalid filename format
            continue

        station_name = csv_file_name[:-4]
        logger.info(
            f"preparing to insert data for station: {station_name} - Progress: {counter} out of {total_files}"
        )
        copy_csv_to_table(station_name)

    # update not read values
    op.execute(
        """
    UPDATE weather SET max_temperature = NULL where max_temperature = -9999;
    """
    )
    op.execute(
        """
    UPDATE weather SET min_temperature = NULL where min_temperature = -9999;
    """
    )
    op.execute(
        """
    UPDATE weather SET precipitation_mm = NULL where precipitation_mm = -9999;
    """
    )

    finish_time = datetime.now()
    conn = op.get_bind()
    res = conn.execute("SELECT count(*) FROM weather;")
    results = res.fetchall()
    logger.info(
        f"start: {start_time} end: {finish_time} total inserted records: {results[0][0]}"
    )


def downgrade() -> None:
    op.execute("DELETE FROM weather;")


def copy_csv_to_table(station_name):
    csv_file_name = join(current_dir, "../wx_data", f"{station_name}.txt")
    read_bulk_size = 100
    with open(csv_file_name, newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter="\t")
        rows = [None] * read_bulk_size
        rows_count = 0
        for row in reader:
            rows[rows_count] = row
            rows_count += 1
            if rows_count == read_bulk_size:
                create_insert_command(station_name, rows)
                rows_count = 0
        if rows_count > 0:
            create_insert_command(station_name, rows[:rows_count])


def create_insert_command(station, rows):
    # TODO: ENSURE DATA WE ARE PASSING ARE SAFE - not SQL INJECTION POSSIBLE THROUGH THEM
    values = ",".join(
        [f"""('{station}', '{row[0]}', {row[1]},{row[2]}, {row[3]})""" for row in rows]
    )
    result = op.execute(
        f"""
    INSERT INTO weather 
    (station, measure_date, max_temperature, min_temperature, precipitation_mm) 
    VALUES 
    {values} 
    ON CONFLICT DO NOTHING;
    """
    )
