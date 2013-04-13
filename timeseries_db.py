from config import DB_FILE
import datetime
import sqlite3

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

def add_temp(ts, f):
    c.execute('INSERT INTO temp_data VALUES (?,?)', (ts, f))
    conn.commit()

def get_most_recent():
    conn.rollback()
    c.execute('SELECT ts, temp_f FROM temp_data ORDER BY ts DESC LIMIT 1')
    return c.fetchall()[0]

def get_last_24_hours():
    conn.rollback()
    # Use this because the "now" in sqllite is not in the same time frame
    # as the logger.
    lower_limit = datetime.datetime.now() - datetime.timedelta(hours=24)
    c.execute('SELECT strftime("%m-%d %H:00",ts) as_hour, AVG(temp_f) '
              'FROM temp_data WHERE ts > ?'
              'GROUP BY as_hour ORDER BY as_hour',  (lower_limit,))
    return c.fetchall()

def get_last_60_minutes():
    conn.rollback()
    lower_limit = datetime.datetime.now() - datetime.timedelta(minutes=60)
    c.execute('SELECT strftime("%m-%d %H:%M",ts) as_minute, AVG(temp_f) '
              'FROM temp_data WHERE ts > ?'
              'GROUP BY as_minute ORDER BY as_minute', (lower_limit,))
    return c.fetchall()

if __name__ == '__main__':
    c.execute("CREATE TABLE temp_data (ts DATETIME PRIMARY KEY, temp_f REAL)")
    conn.commit()
