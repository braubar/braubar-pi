# StateMachine/mouse/MouseAction.py

class BrewAction:
    def __init__(self, action):
        self.action = action

    def __str__(self): return self.action

    def __cmp__(self, other):
        print("cmp")
        return cmp(self.action, other.action)

    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.action)


# Static fields; an enumeration of instances:
BrewAction.maischen = BrewAction("maischen")
BrewAction.beta = BrewAction("beta")
BrewAction.alpha = BrewAction("alpha")
BrewAction.leutern = BrewAction("leutern")
BrewAction.kochen = BrewAction("kochen")
BrewAction.ende = BrewAction("ende")


