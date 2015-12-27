import sched
import time
from brewtimer import BrewTimer


class SimpleState:
    count = 1
    global state

    MAISCHEN = "maischen"
    BETA = "beta"
    ALPHA = "alpha"
    LEUTERN = "leutern"
    KOCHEN = "kochen"
    ENDE = "ende"

    state_list = []

    global state_machine

    @staticmethod
    def instance():
        if not state_machine:
            state_machine = SimpleState()
        return state_machine

    def __init__(self):
        self.state_list = [(self.maischen, SimpleState.MAISCHEN),
                           (self.beta, SimpleState.BETA),
                           (self.alpha, SimpleState.ALPHA),
                           (self.leutern, SimpleState.LEUTERN),
                           (self.kochen, SimpleState.KOCHEN),
                           (self.end, SimpleState.ENDE)]
        self.state_list.reverse()

    def maischen(self, x):
        state = self.MAISCHEN

        print('vorheriger state: ', x)
        return "warten, bis der nächste aufgerufen wird. "

    def beta(self, x):
        state = self.BETA
        # x,time muss noch konvertiert werden
        delay = x.get('time')
        BrewTimer(delay, self.next())
        print('beta will be finished after ', delay)
        return x

    def alpha(self, x):
        state = self.ALPHA
        delay = x.get('time')
        BrewTimer(delay, self.next())
        print('alpha got', x)
        return x

    def leutern(self, x):
        state = self.LEUTERN
        print('leutern got', x)
        return x

    def kochen(self, x):
        state = self.KOCHEN
        print('kochen got', x)
        return x

    def end(self, x):
        state = self.ENDE
        print("this is the end, my friend")
        exit(0)

    def next(self):
        method, state_name = self.state_list.pop()
        return method(SimpleState.rezept.get(state_name))

    # def runall(self):
    #     print(self.machine)
    #     state, arg = self.machine.get((self.maischen, 0))
    #     i = 0
    #     while True:
    #         event = state(self.rezept.get(arg))
    #         res = self.machine.get((state, event))
    #         # print(res)
    #         # print(machine)
    #         if not res:
    #             print("halting on", state, event)
    #             break
    #         state, arg = res
    #         i += 1
    #         if i > 20:
    #             break

    def change_state(self, next, *kargs):
        # TODO change_state implementiren
        print("changestate doesnt work: ", next)


        # d = timedelta(seconds=10)
        # t = threading.Thread(target=c.wait_with_status, args=[d.seconds])
        # t.start()
        # if t.is_alive():
        #     return 'thread runs for ' + str(c.delta) + ' more seconds'

    # s = SimpleState()
    machine = {
        (maischen, 0): (maischen, MAISCHEN),
        (maischen, 1): (beta, BETA),
        (beta, 1): (alpha, ALPHA),
        (alpha, 1): (leutern, LEUTERN),
        (leutern, 1): (kochen, KOCHEN),
        (kochen, 1): (end, ENDE)
    }

    rezept = {
        'maischen': {
            'temp': 45,
            'time': 0,
            'auto': 0
        },
        'beta': {
            'temp': 63,
            'time': 4,
            'auto': 1
        },
        'alpha': {
            'temp': 74,
            'time': 3,
            'auto': 1
        },
        'leutern': {
            'temp': 78,
            'time': 0,
            'auto': 0
        },
        'kochen': {
            'temp': 100,
            'time': 0,
            'auto': 0
        }
    }

# s.runall()
