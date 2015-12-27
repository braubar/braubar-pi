from brewtimer import BrewTimer


class SimpleState:
    count = 1
    state = None

    MAISCHEN = "maischen"
    BETA = "beta"
    ALPHA = "alpha"
    LEUTERN = "leutern"
    KOCHEN = "kochen"
    ENDE = "ende"

    state_list = []

    def __init__(self):
        self.state_list = [(self.maischen, SimpleState.MAISCHEN),
                           (self.beta, SimpleState.BETA),
                           (self.alpha, SimpleState.ALPHA),
                           (self.leutern, SimpleState.LEUTERN),
                           (self.kochen, SimpleState.KOCHEN),
                           (self.end, SimpleState.ENDE)]
        self.state_list.reverse()

    def start(self):
        if not self.state:
            return self.next()
        raise Exception("Braubar is already running")

    def maischen(self, x):
        state = self.MAISCHEN

        print("warten, bis der nächste aufgerufen wird. ")
        return self.rezept[state]

    def beta(self, x):
        state = self.BETA
        # x,time muss noch konvertiert werden
        delay = x.get('time')
        b = BrewTimer(delay, self.next())
        b.start()
        print('beta will be finished after ', delay)
        return x

    def alpha(self, x):
        state = self.ALPHA
        delay = x.get('time')
        b = BrewTimer(delay, self.next())
        b.start()
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

    def change_state(self, next, *kargs):
        # TODO change_state implementiren
        print("changestate doesnt work: ", next)


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
