from datetime import datetime
import sqlite3


class BrewLog:
    db = None

    def __init__(self):
        self.conn = sqlite3.connect('brew.db')
        self.db = self.conn.cursor()

    def log(self, current_temp, target_temp, change, sensor_id, current_state, brew_id):
        brew_time = datetime.now()
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


class BrewLogDAO:
    brew_time = None
    current_temp = None
    target_temp = None
    change = None
    sensor_id = None
    current_state = None
