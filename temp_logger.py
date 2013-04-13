import time
from datetime import datetime
from temp_lib import read_temp
from config import SLEEP_TIME
from timeseries_db import add_temp

while __name__ == '__main__':
    add_temp(datetime.now(), read_temp())
    time.sleep(SLEEP_TIME)
