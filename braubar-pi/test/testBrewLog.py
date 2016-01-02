

from brewlog import BrewLog, BrewLogDAO

log = BrewLog()

log.log(43.0, 45.0, 5.0, 1, "einmaischen")
log.log(45.0, 45.0, -5.0, 1, "einmaischen")
log.log(45.4, 45.0, -5.0, 1, "einmaischen")


print(log.readAll())

print(log.getTempValues())


log.shutdown()

