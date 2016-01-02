import sqlite3


class BrewLog:
    db = None

    def __init__(self):
        conn = sqlite3.connect('brew.db')
        self.db = conn.cursor()

    def log(self, brewLogDAO):
        self.db.execute(
                '''INSERT INTO brewlog
                    VALUES (?,?,?,?,?,?)
                    ''', (brewLogDAO.brew_time,
                            brewLogDAO.current_temp,
                            brewLogDAO.target_temp,
                            brewLogDAO.change,
                            brewLogDAO.sensor_id,
                            brewLogDAO.current_state))

    def readAll(self):
        self.db.execute('''
          SELECT * FROM brewlog;
          ''')gi



    def setup(self):
        """
        This is only called on first execute
        :return:
        """
        self.db.execute('''
                    CREATE TABLE brewlog (
                      date DATETIME,
                      current_temp FLOAT,
                      target_temp FLOAT,
                      change FLOAT ,
                      sensor_id INT,
                      current_state TEXT)
                      ''')

    def shutdown(self):
        self.db.close()


class BrewLogDAO:
    brew_time = None
    current_temp = None
    target_temp = None
    change = None
    sensor_id = None
    current_state = None
