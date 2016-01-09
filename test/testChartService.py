import unittest
import sys
import datetime
import matplotlib.pyplot as plt
import numpy as np

from sklearn import linear_model

sys.path += ["./service"]
import chartService


class TestChartService(unittest.TestCase):
    def test_something(self):
        cs = chartService.ChartService()
        cs.temp_increase(1452345148839)

    #     self.assertEqual(True, True)

    def testLin_Reg(self):
        cs = chartService.ChartService()
        stmt = '''select brew_id, brew_time, current_temp
                    from brewlog
                    where brew_id=?
                    and datetime(brew_time) >= datetime(current_timestamp,'-1 minutes', "localtime")
                    order by brew_time asc;
                '''
        stmt_args = [1452351456671]
        dat = cs.select(stmt, stmt_args)
        data = [(1452263810951, '2016-01-08T15:39:42.066381', 47.06),
                 (1452263810951, '2016-01-08T15:39:39.938612', 47.06),
                 (1452263810951, '2016-01-08T15:39:37.818718', 47.06),
                 (1452263810951, '2016-01-08T15:39:35.689863', 47.06),
                 (1452263810951, '2016-01-08T15:39:31.419443', 47.06),
                 (1452263810951, '2016-01-08T15:39:33.564566', 47.06),
                 (1452263810951, '2016-01-08T15:39:29.293816', 47.06),
                 (1452263810951, '2016-01-08T15:39:27.172160', 47.06),
                 (1452263810951, '2016-01-08T15:39:25.057442', 47.06),
                 (1452263810951, '2016-01-08T15:39:22.938337', 47.06),
                 (1452263810951, '2016-01-08T15:39:20.822455', 47.12),
                 (1452263810951, '2016-01-08T15:39:18.702429', 47.12),
                 (1452263810951, '2016-01-08T15:39:16.585970', 47.12),
                 (1452263810951, '2016-01-08T15:39:14.461290', 47.12),
                 (1452263810951, '2016-01-08T15:39:12.345385', 47.12),
                 (1452263810951, '2016-01-08T15:39:10.224860', 47.12),
                 (1452263810951, '2016-01-08T15:39:08.094073', 47.12),
                 (1452263810951, '2016-01-08T15:39:05.957633', 47.12),
                 (1452263810951, '2016-01-08T15:39:03.830800', 47.12),
                 (1452263810951, '2016-01-08T15:39:01.709895', 47.12),
                 (1452263810951, '2016-01-08T15:38:59.572879', 47.12),
                 (1452263810951, '2016-01-08T15:38:57.395704', 47.18),
                 (1452263810951, '2016-01-08T15:38:55.269936', 47.18),
                 (1452263810951, '2016-01-08T15:38:53.154337', 47.18),
                 (1452263810951, '2016-01-08T15:38:51.030096', 47.18),
                 (1452263810951, '2016-01-08T15:38:48.893877', 47.18),
                 (1452263810951, '2016-01-08T15:38:46.774857', 47.18),
                 (1452263810951, '2016-01-08T15:38:44.633620', 47.25)]
        # x_sum = chartService.ChartService.lin_reg(data)
        # x = [(datetime.datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%f") -
        #       # datetime.datetime.strptime(data[0][1], "%Y-%m-%dT%H:%M:%S.%f")) /
        #       datetime.datetime.fromtimestamp(row[0] / 1000)) /
        #      datetime.timedelta(microseconds=1) / 1000 / 1000 / 60 for row in data]
        data.reverse()
        x = [cs.get_duration_timestamp(row[0], row[1]) for row in data]
        y = [row[2] for row in data]

        # print(len(x), len(y))
        a, b = cs.lin_reg(data)
        # Plot outputs
        # y = bx + a
        y_dach =  []
        for row in x:
            y_dach.append((b*row+a))
        plt.scatter(x, y, color='black')
        plt.scatter(x, y_dach, color='blue')

        plt.xticks((x))
        plt.yticks((y_dach))

        plt.show()


if __name__ == '__main__':
    unittest.main()
