import time
import logging

start_time = time.time()


# Print time and message
def log(text):
    log_text = f'{round(time.time() - start_time, 2)}s: {text}'
    logging.info(log_text)
    print(log_text)
    print('=' * 100, '\n')
