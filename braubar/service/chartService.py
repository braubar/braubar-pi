import sqlite3
import json
TOLERANCE = 0.2


class ChartService:
    @staticmethod
    def last_row(brew_id=None):
        conn = sqlite3.connect('brew.db')
        db = conn.cursor()
        stmt_args = []
        if brew_id:
            stmt = '''select * from brewlog
            where brew_id = ?
            ORDER BY brew_time DESC
            LIMIT 1;'''
            stmt_args.append(brew_id)
        else:
            stmt = '''select * from brewlog
            ORDER BY brew_time DESC
            LIMIT 1;'''

        db.execute(stmt, stmt_args)
        data = db.fetchall()[0]
        conn.close()
        return {
            "brew_time": data[0],
            "current_temp": data[1],
            "target_temp": data[2],
            "change": data[3],
            "sensor_id": data[4],
            "current_state": data[5],
            "brew_id": data[6]
        }

    @staticmethod
    def brew_chart_old(brew_id=None):
        conn = sqlite3.connect('brew.db')
        db = conn.cursor()
        stmt_args = []
        if brew_id:
            stmt = '''
                SELECT * from brewlog where brew_id = ?
            '''
            stmt_args.append(brew_id)
        else:
            stmt = '''
                SELECT * from brewlog
            '''

        db.execute(stmt, stmt_args)
        data = db.fetchall()
        conn.close()

        temp_current = []
        temp_target = []
        temp_date = []
        temp_change = []

        last_temp = 0.0
        last_change = 0.0
        count = 0
        total = 0
        for row in data:
            temp = row[1]
            change = row[3]
            if (last_temp <= temp - TOLERANCE or temp + TOLERANCE <= last_temp) or last_change != change:
                temp_date.append(row[0])
                temp_current.append(row[1])
                temp_target.append(row[2])
                temp_change.append(change)
                count += 1
                last_change = change
                last_temp = temp
            total += 1
        print(count, "lines", "id", brew_id, "total", total)

        return temp_date, temp_current, temp_target, temp_change


    @staticmethod
    def brew_chart(brew_id=None):
        conn = sqlite3.connect('brew.db')
        db = conn.cursor()
        stmt_args = []
        if brew_id:
            stmt = '''
                    SELECT * from brewlog where brew_id = ?
                '''
            stmt_args.append(brew_id)
        else:
            stmt = '''
                    SELECT * from brewlog
                '''

        db.execute(stmt, stmt_args)
        data = db.fetchall()
        conn.close()

        last_temp = 0.0
        last_change = 0.0
        count = 0
        total = 0
        result = []
        for row in data:
            temp = row[1]
            change = row[3]
            if (last_temp <= temp - TOLERANCE or temp + TOLERANCE <= last_temp) or last_change != change:
                r = {
                    "date": row[0],
                    "current": temp,
                    "target": row[2],
                    "change": change,
                    "sensor": row[4],
                    "state": row[5],
                    "brew_id": row[6]
                }
                result.append(r)
                count += 1
                last_change = change
                last_temp = temp
            total += 1
        print(count, "lines", "id", brew_id, "total", total)
        return json.dumps(result)


@staticmethod
def chart_file(count, last_temp, temp_change, temp_current, temp_date, temp_target):
    f = open("./log/brewlog_29-12-2015_00-54-13.log")
    for line in f.readlines():
        temp = line[26:-2].split()[3][:-1]
        temp = float(temp)
        if last_temp != temp or last_temp <= temp - TOLERANCE and temp + TOLERANCE >= last_temp:
            temp_current.append(temp)
            temp_target.append(line[26:-2].split()[1][:-1])
            temp_date.append(line[1:24])
            temp_change.append(line[26:-2].split()[5][:-1])
        else:
            count += 1
        last_temp = temp
    print("omitted", count, "lines")
