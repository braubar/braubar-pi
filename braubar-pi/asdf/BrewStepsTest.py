# State Machine pattern using 'if' statements
# to determine the next state.

from BrewAction import BrewAction

from StateMachine import StateMachine
from asdf.State import State


# A different subclass for each state:

class Einmaischen(State):
    def run(self):
        # TODO wartet auf start durch Benutzer
        print("Einmaischen: warten auf Benutzereingabe")

    def next(self, input):
        if input == BrewAction.beta:
            return BrewProcess.beta
        return BrewProcess.einmaischen


class Leutern(State):
    def run(self):
        # TODO wartet auf start durch Benutzer
        print("Leutern: warten auf Benutzereingabe")

    def next(self, input):
        if input == BrewAction.maischen:
            return BrewProcess.einmaischen
        if input == BrewAction.kochen:
            return BrewProcess.kochen
        return BrewProcess.einmaischen


class Alpha(State):
    def run(self):
        print("Alpha-Amylase: x°C für y min")

    def next(self, input):
        if input == BrewAction.leutern:
            return BrewProcess.leutern
        return BrewProcess.alpha


class Kochen(State):
    def run(self):
        # nach x min n. ladung hopen
        # gesamt X min kochen
        print("Kochen: x°C für y min")

    def next(self, input):
        if input == BrewAction.hopfen:
            # zugabe zeiten vom hopfen
            return BrewProcess.kochen
        if input == BrewAction.maischen:
            BrewAction.maischen
        return BrewProcess.kochen


class Beta(State):
    def run(self):
        print("Beta-Amylase: x°C für y min")

    def next(self, input):
        if input == BrewAction.alpha:
            return BrewProcess.alpha
        return BrewProcess.beta


class Ende(State):
    def run(self):
        print("Ende")

    def next(self, input):
        return BrewProcess.ende


class BrewProcess(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, BrewProcess.einmaischen)


# Static variable initialization:
BrewProcess.einmaischen = Einmaischen()
BrewProcess.beta = Beta()
BrewProcess.alpha = Alpha()
BrewProcess.leutern = Leutern()
BrewProcess.kochen = Kochen()
BrewProcess.ende = Ende()

phasen = map(str.strip, open("steps.txt").readlines())
BrewProcess().runAll(map(BrewAction, phasen))
