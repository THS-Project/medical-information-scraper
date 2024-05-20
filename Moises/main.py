import datetime
import time
import logging
import os
import chroma.write_to_chroma_script as write_chroma
import chroma.create_chromadb as create_chroma

# Print time and message
def log(text):
    log_text = f'{round(time.time() - start_time, 2)}s: {text}'
    logging.info(log_text)
    print(log_text)
    print('=' * 100, '\n')


def start_project():
    # Check if chroma db exists
    if not os.path.isfile("chromadb/chroma.sqlite3"):
        create_chroma.create_db()


if __name__ == '__main__':
    start_time = time.time()

    logging.basicConfig(filename=f"scraper_{datetime.date.today()}.log", level=logging.INFO)
    write_chroma.chroma_write()
