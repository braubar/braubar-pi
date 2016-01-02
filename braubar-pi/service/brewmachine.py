from helper.brewtimer import BrewTimer
from simplestate import SimpleState


class BrewMachine():
    state = None
    rezept = None

    def __init__(self, state_list, rezept):
        self.stateList = state_list
        self.rezept = rezept

    def status(self):
        return self.status

    def next(self):
        self.state = self.stateList.pop()()

    def run(self):
        if not self.state:
            self.next()
        return self.state.run()


class Maischen(State):
    temp = None
    time = None

    def __init__(self):
        self.name = "maischen"

    def run(self):
        self.time = 1
        # TODO starte temp control, release erst wenn ziel temp erreicht

        brew_timer = BrewTimer(self.time, self.release_state)

        return self.name

    def release_state(self):
        print("timer finished")
        self.finished = True


class Beta(State):
    def __init__(self):
        self.name = "beta"

    def run(self):
        # TODO starte temp control, timer erst mit erreichen der zieltemp anfangen
        return self.name


class Alpha(State):
    def __init__(self):
        self.name = "alpha"

    def run(self):
        # TODO starte temp control, timer erst mit erreichen der zieltemp anfangen
        return self.name


class Leutern(State):
    def __init__(self):
        self.name = "leutern"

    def run(self):
        # TODO starte temp control, release erst wenn ziel temp erreicht
        return self.name


class Kochen(State):
    def __init__(self):
        self.name = "kochen"

    def run(self):
        # TODO starte temp control, timer erst mit erreichen der zieltemp starten
        return self.name
