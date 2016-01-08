import sqlite3
import json
import math

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
    def brew_status(brew_id):
        last_row = ChartService.last_row(brew_id=brew_id)
        # return json.dumps({"status": 501})
        return json.dumps(last_row)

    @staticmethod
    def system_status(brew_id):
        return json.dumps({"status": 501})

    @staticmethod
    def temp_increase(brew_id):
        conn = sqlite3.connect('brew.db')
        db = conn.cursor()
        stmt_args = []
        stmt = '''select brew_time, current_temp
                    from brewlog
                    where brew_id=?
                    and datetime(brew_time) >= datetime(current_timestamp,'-1 minutes', "localtime")
                    order by brew_time desc;
                '''
        stmt_args.append(brew_id)

        db.execute(stmt, stmt_args)
        data = db.fetchall()
        conn.close()
        return round(data.pop(0)[1] - data.pop()[1], 2)
