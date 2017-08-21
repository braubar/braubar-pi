import json

RECIPE_FILE = "../config/recipe.json"

class SimpleState:
    count = 1
    state = None

    MAISCHEN = "maischen"
    EIWEISSRAST = "eiweissrast"
    BETA = "beta"
    ALPHA = "alpha"
    LEUTERN = "laeutern"
    KOCHEN = "kochen"
    VORKOCHEN = "vorkochen"
    ENDE = "ende"
    PAUSE = "pause"
    recipe = None
    state_list = []

    def __init__(self):
        self.state_list = [(self.pause, SimpleState.PAUSE),
                           (self.maischen, SimpleState.MAISCHEN),
                           (self.eiweissrast, SimpleState.EIWEISSRAST),
                           (self.beta, SimpleState.BETA),
                           (self.alpha, SimpleState.ALPHA),
                           (self.laeutern, SimpleState.LEUTERN),
                           (self.pause, SimpleState.PAUSE),
                           (self.vorkochen, SimpleState.VORKOCHEN),
                           (self.kochen, SimpleState.KOCHEN),
                           (self.pause, SimpleState.PAUSE),
                           (self.end, SimpleState.ENDE)]
        self.state_list.reverse()
        self.recipe = json.load(open(RECIPE_FILE, 'r'))

    def start(self):
        if not self.state:
            return self.next()
        raise Exception("Braubar is already running")

    def maischen(self, x):
        self.state = self.MAISCHEN

        print("warten, bis der nächste aufgerufen wird. ")
        return self.recipe[self.state]

    def beta(self, x):
        self.state = self.BETA
        # x,time muss noch konvertiert werden
        delay = x.get('time')
        print('beta will be finished after ', delay)
        return self.recipe[self.state]

    def eiweissrast(self, x):
        self.state = self.EIWEISSRAST
        # x,time muss noch konvertiert werden
        delay = x.get('time')
        print('eiweissrast will be finished after ', delay)
        return self.recipe[self.state]

    def alpha(self, x):
        self.state = self.ALPHA
        delay = x.get('time')
        print('alpha got', x)
        return self.recipe[self.state]

    def laeutern(self, x):
        self.state = self.LEUTERN
        print('leutern got', x)
        return self.recipe[self.state]

    def kochen(self, x):
        self.state = self.KOCHEN
        print('kochen got', x)
        return self.recipe[self.state]

    def vorkochen(self, x):
        self.state = self.VORKOCHEN
        print('vorkochen got', x)
        return self.recipe[self.state]

    def end(self, x):
        self.state = self.ENDE
        print("this is the end, my friend")
        exit(0)

    def pause(self, x):
        self.state = self.PAUSE
        print("State: pause")
        return self.recipe[self.state]

    def next(self):
        method, state_name = self.state_list.pop()
        return method(self.recipe.get(state_name))

    def change_state(self, next, *kargs):
        # TODO change_state implementiren
        print("changestate doesnt work: ", next)
