import datetime
import sqlite3
import json
import math

TOLERANCE = 0.1
DBNAME = 'brew.db'

class ChartService:
    def last_row(self, brew_id=None):
        conn = sqlite3.connect(DBNAME)
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
            "brew_time": data[0][:-3],
            "current_temp": data[1],
            "target_temp": data[2],
            "change": self.calc_pid_output_for_chart(data[3]),
            "sensor_id": data[4],
            "current_state": data[5],
            "brew_id": data[6],
            "timer_passed": data[7],
            "brew_start": data[8]
        }

    def last_row2(self, brew_id=None):
        conn = sqlite3.connect(DBNAME)
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
        temp = data[1]
        change = data[3]
        return {
            "date": data[0],
            "current": temp,
            "target": data[2],
            "change": self.calc_pid_output_for_chart(change),
            "sensor": data[4],
            "state": data[5],
            "brew_id": data[6]
        }

    def brew_chart(self, brew_id=None):
        conn = sqlite3.connect(DBNAME)
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
                    "brew_time": row[0][:-3],
                    "current_temp": temp,
                    "target_temp": row[2],
                    "change": self.calc_pid_output_for_chart(change),
                    "sensor_id": row[4],
                    "current_state": row[5],
                    "brew_id": row[6],
                    "brew_start": row[7]
                }
                result.append(r)
                count += 1
                last_change = change
                last_temp = temp
            total += 1
        print(count, "lines", "id", brew_id, "total", total)
        return json.dumps(result)

    def brew_status(self, brew_id):
        last_row = self.last_row(brew_id=brew_id)
        # return json.dumps({"status": 501})
        return json.dumps(last_row)

    def system_status(self, brew_id):
        return json.dumps({"status": 501})

    def status(self, brew_id):
        status = {"ok": False}
        try:
            status = self.last_row(brew_id)
            brew_time = datetime.datetime.strptime(status["brew_time"], "%Y-%m-%dT%H:%M:%S.%f")
            brew_start = datetime.datetime.strptime(status["brew_start"], "%Y-%m-%dT%H:%M:%S.%f")
            duration = (brew_time - brew_start)
            status["duration"] = str(duration).split(".")[0]
            status["temp_increase"] = self.temp_increase(brew_id)
            status["ok"] = True
        except Exception as e:
            print(e)
        return status


    def temp_increase(self, brew_id):
        stmt_args = []
        stmt = '''select brew_id, brew_time, current_temp
                    from brewlog
                    where brew_id=?
                    and datetime(brew_time) >= datetime(current_timestamp,'-1 minutes', "localtime")
                    order by brew_time asc;
                '''
        stmt_args.append(brew_id)
        data = self.select(stmt, stmt_args)
        if len(data) > 0:
            a, b = self.lin_reg(data)
            # y = b*x + a
            y_before = b * data[0][2] + a
            y_now = b * data[-1][2] + a
            # TODO vor einer minute wir ein großer negativer wert angezeigt.
        else:
            return 0.0
        return round(y_now - y_before, 2)

    def select(self, stmt, stmt_args):
        conn = sqlite3.connect(DBNAME)
        db = conn.cursor()
        db.execute(stmt, stmt_args)
        data = db.fetchall()
        conn.close()
        return data

    def lin_reg(self, data):
        x_sum = float()
        y_sum = float()
        for row in data:
            x_sum += self.get_duration_timestamp(row[0], row[1])
            y_sum += row[2]
        l=len(data)
        if l==0:
            l=1
        x_strich = x_sum / l
        y_strich = y_sum / l

        sum_delta = 0.0
        sum_x_delta_pow = 0.0
        for row in data:
            sum_x_delta = (self.get_duration_timestamp(row[0], row[1]) - x_strich)
            sum_delta += sum_x_delta * (row[2] - y_strich)
            sum_x_delta_pow += math.pow(sum_x_delta, 2)
        if sum_x_delta_pow != 0.0:
            b_xy = sum_delta / sum_x_delta_pow
            a_xy = y_strich - b_xy * x_strich
        else:
            return 0.0, 0.0
        return a_xy, b_xy

    def get_duration_datetime_str(self, start_time, timestamp):
        brew_time = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
        brew_start = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f")
        return (brew_time - brew_start) / datetime.timedelta(milliseconds=1) / 1000 / 60

    def get_duration_timestamp(self, start_time, timestamp):
        brew_time = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
        brew_start = datetime.datetime.fromtimestamp(start_time / 1000)
        return (brew_time - brew_start) / datetime.timedelta(milliseconds=1) / 1000 / 60

    def calc_pid_output_for_chart(self, output):
        return output / 1000 / 2 + 50

    def get_last_brew_id(self):
        stmt_args = []
        stmt = '''select brew_id from brewlog order by brew_id DESC LIMIT 1'''
        data = self.select(stmt, stmt_args)
        if data is not None and len(data) is not 0 and data[0][0] is not None:
            return data[0][0]
        return 1
