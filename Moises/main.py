import datetime
import logging
import os
import chroma.write_to_chroma_script as write_chroma
import chroma.chromadb_init as create_chroma
import scraper.scraper as scraper
from Moises.create_log import log
from Moises.insert_data_to_db.insert_data import DataInsert
from Moises.chroma.read_from_chroma_script import get_data


def start_project():
    # Check if chroma db exists
    path = "chromadb/chroma.sqlite3"
    if not os.path.isfile(path):
        create_chroma.create_db()
    else:
        log(f'File {path} already exists')


if __name__ == '__main__':
    # read = False
    read = True

    if read:
        get_data()

    else:
        logging.basicConfig(filename=f"scraper_{datetime.date.today()}.log", level=logging.INFO)
        # Creat chroma db
        start_project()

        # Start scraper and transform data
        scraper.start_scraper()

        # Write to chroma database
        write_chroma.chroma_write()

        # Write to relational database
        data_insert = DataInsert()
        data_insert.insert_data_from_directory()


