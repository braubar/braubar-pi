from brewmachine import *
import json

state_list = [Maischen, Beta, Alpha, Leutern, Kochen, Kochen]
state_list.reverse()

io = open("rezept.json").read()
rezept = json.loads(io)

foo = BrewMachine(state_list, rezept)

for _ in range(0, len(state_list) - 1):
    foo.next()
    print(foo.run())
