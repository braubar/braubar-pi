from state import State


class StateMachine:
    state = None
    stateList = None

    def __init__(self, stateList):
        self.stateList = stateList
        pass

    def start(self):
        pass

    def current(self):
        return self.state

    def status(self):
        pass
