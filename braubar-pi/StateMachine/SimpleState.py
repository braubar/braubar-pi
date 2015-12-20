import sched
import time


class SimpleState:
    count = 1
    state = None

    MAISCHEN = "maischen"
    BETA = "beta"
    ALPHA = "alpha"
    LEUTERN = "leutern"
    KOCHEN = "kochen"
    ENDE = "ende"

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def maischen(self, x):
        state = self.MAISCHEN

        trigger = 1
        print('maischen got', x)
        if not trigger:
            return 0
        return self.count

    def beta(self, x):
        state = self.BETA
        # x,time muss noch konvertiert werden
        # dumm dass es blockiert.
        print('beta got', x)
        delay = x.get('time')

        self.scheduler.enter(delay, 1, self.change_state, argument=x)
        self.scheduler.run()
        print('beta finished after ', x.get('time'))
        return self.count

    def alpha(self, x):
        state = self.ALPHA
        delay = x.get('time')
        self.scheduler.enter(delay, 1, self.change_state, argument=x)
        self.scheduler.run()
        print('alpha got', x)
        return self.count

    def leutern(self, x):
        state = self.LEUTERN
        print('leutern got', x)
        return self.count

    def kochen(self, x):
        state = self.KOCHEN
        print('kochen got', x)
        return self.count

    def end(self, x):
        state = self.ENDE
        print("this is the end, my friend")
        exit(0)

    def runall(self):
        print(self.machine)
        state, arg = self.machine.get((self.maischen, 0))
        i = 0
        while True:
            event = state(self.rezept.get(arg))
            res = self.machine.get((state, event))
            # print(res)
            # print(machine)
            if not res:
                print("halting on", state, event)
                break
            state, arg = res
            i += 1
            if i > 20:
                break

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
