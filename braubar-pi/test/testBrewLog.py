import datetime

from brewlog import BrewLog, BrewLogDAO

log = BrewLog()

# log.setup()

dao = BrewLogDAO
dao.change = 5.0
dao.current_state = "einmaischen"
dao.current_temp = 43.0
dao.target_temp = 45.0
dao.brew_time = datetime.datetime.now()
dao.sensor_id = 1

log.log(dao)

log.shutdown()