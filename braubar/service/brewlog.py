import logging
from datetime import datetime
import sqlite3
import time
from service.brewconfig import BrewConfig


logfile = BrewConfig.LOG_BASE + time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime()) + ".log"
logging.basicConfig(filename=logfile, level=logging.WARN, format='{%(asctime)s: %(message)s}')

class BrewLog:
    db = None

    def __init__(self):
        self.conn = sqlite3.connect('brew.db')
        self.db = self.conn.cursor()

    def log(self, current_temp, target_temp, change, sensor_id, current_state, brew_id):
        brew_time = datetime.now().isoformat()
        try:
            self.db.execute(
                    '''INSERT INTO brewlog
                        VALUES (?,?,?,?,?,?,?)
                        ''', (brew_time,
                              current_temp,
                              target_temp,
                              change,
                              sensor_id,
                              current_state,
                              brew_id))
            self.conn.commit()

        except sqlite3.Error as e:
            if e.args[0] == 'no such table: brewlog':
                self.create_table()
                print("checking DB and create table...")
            else:
                logging.error(e)
                print("big error", e)

    def readAll(self):
        self.db.execute('''
          SELECT * FROM brewlog;
          ''')
        data = self.db.fetchall()
        return data

    def getTempValues(self):
        self.db.execute('''
          SELECT current_temp FROM brewlog;
          ''')
        data = self.db.fetchall()
        return data

    def shutdown(self):
        self.db.close()
        self.conn.close()

    def create_table(self):
        try:
            self.db.execute('''
                CREATE TABLE brewlog (
                    brew_time DATETIME NOT NULL,
                    current_temp FLOAT NOT NULL,
                    target_temp FLOAT NOT NULL,
                    change FLOAT,
                    sensor_id INT,
                    current_state TEXT,
                    brew_id INT
                )
            ''')
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            self.shutdown()
        finally:
            pass


class BrewLogDAO:
    brew_time = None
    current_temp = None
    target_temp = None
    change = None
    sensor_id = None
    current_state = None
