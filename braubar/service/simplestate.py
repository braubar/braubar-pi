import json
import os

RECIPE_FILE = "../config/recipe.json"

class SimpleState:
    count = 1
    state = None

    MAISCHEN = "maischen"
    BETA = "beta"
    ALPHA = "alpha"
    LEUTERN = "laeutern"
    KOCHEN = "kochen"
    ENDE = "ende"
    recipe = None
    state_list = []

    def __init__(self):
        self.state_list = [(self.maischen, SimpleState.MAISCHEN),
                           (self.beta, SimpleState.BETA),
                           (self.alpha, SimpleState.ALPHA),
                           (self.laeutern, SimpleState.LEUTERN),
                           (self.kochen, SimpleState.KOCHEN),
                           (self.end, SimpleState.ENDE)]
        self.state_list.reverse()
        self.recipe = json.load(open(RECIPE_FILE, 'r'))

    def start(self):
        if not self.state:
            return self.next()
        raise Exception("Braubar is already running")

    def maischen(self, x):
        state = self.MAISCHEN

        print("warten, bis der nächste aufgerufen wird. ")
        return self.recipe[state]

    def beta(self, x):
        state = self.BETA
        # x,time muss noch konvertiert werden
        delay = x.get('time')
        print('beta will be finished after ', delay)
        return x

    def alpha(self, x):
        state = self.ALPHA
        delay = x.get('time')
        print('alpha got', x)
        return x

    def laeutern(self, x):
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
        return method(self.recipe.get(state_name))

    def change_state(self, next, *kargs):
        # TODO change_state implementiren
        print("changestate doesnt work: ", next)
