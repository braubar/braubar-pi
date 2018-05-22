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
        db_name = 'brew.db'
        self.conn = sqlite3.connect(db_name)
        self.db = self.conn.cursor()
        if not self.check_table_exists("brewlog"):
            self.create_table()

    def check_table_exists(self, name):
        self.db.execute(
            '''SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = ?;
            ''',
            [name]
        )
        data = self.db.fetchall()
        if len(data) is 0:
            return False
        if data[0][0] == name:
            return True

    def log(self, current_temp, target_temp, change, sensor_id, current_state, brew_id, brew_start, timer_passed=0):
        brew_time = datetime.now().isoformat()
        try:
            self.db.execute(
                    '''INSERT INTO brewlog
                        VALUES (?,?,?,?,?,?,?,?,?)
                        ''', (brew_time,
                              current_temp,
                              target_temp,
                              change,
                              sensor_id,
                              current_state,
                              brew_id,
                              timer_passed,
                              brew_start))
            self.conn.commit()

        except sqlite3.Error as e:
            if e.args[0] == 'no such table: brewlog':
                self.create_table()
                print("checking DB and create table...")
            else:
                logging.error(e)
                print("DB Error ", e)

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
            # brewlog
            self.db.execute('''
                CREATE TABLE brewlog (
                    brew_time DATETIME NOT NULL,
                    current_temp FLOAT NOT NULL,
                    target_temp FLOAT NOT NULL,
                    change FLOAT,
                    sensor_id INT,
                    current_state TEXT,
                    brew_id INT,
                    timer_passed INT, 
                    brew_start DATETIME NOT NULL
                )
            ''')

            # brew_meta
            self.db.execute('''
                CREATE TABLE brew_meta (
                    id INT PRIMARY KEY NOT NULL,
                    sud_nr INT NOT NULL, 
                    start_time DATETIME,
                    end_time DATETIME
                )
            ''')
        except sqlite3.Error as e:
            print("An DB error occurred:", e.args[0])
            self.shutdown()
        finally:
            pass

    def get_last_brew_id(self):
        stmt_args = []
        stmt = '''select brew_id from brewlog order by brew_id DESC LIMIT 1'''
        data = None
        try:
            self.db.execute(stmt, stmt_args)
            data = self.db.fetchall()
        except sqlite3.Error as e:
            print("An DB error occurred:", e.args[0])
            self.shutdown()

        if data is not None and len(data) is not 0:
            return data[0][0]
        return 1


class BrewLogDAO:
    brew_time = None
    current_temp = None
    target_temp = None
    change = None
    sensor_id = None
    current_state = None
