import sqlite3


def setup_db():
    conn = sqlite3.connect('brew.db')
    db = conn.cursor()
    db.execute('''
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

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_db()
