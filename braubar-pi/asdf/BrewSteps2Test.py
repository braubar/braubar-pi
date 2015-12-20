# StateMachine/mousetrap2/MouseTrap2Test.py
# A better mousetrap using tables
import sys

sys.path += ['../stateMachine', '../mouse']
from asdf.State import State
from asdf import StateMachine
from asdf.BrewAction import BrewAction


class StateT(State):
    def __init__(self):
        self.transitions = None

    def next(self, input):
        if self.transitions in input:
            return self.transitions[input]
        else:
            raise "Input not supported for current state"


class Waiting(StateT):
    def run(self):
        print("Waiting: Broadcasting cheese smell")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                BrewAction.maischen: MouseTrap.luring
            }
        return StateT.next(self, input)


class Luring(StateT):
    def run(self):
        print("Luring: Presenting Cheese, door open")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                BrewAction.beta: MouseTrap.trapping,
                BrewAction.ende: MouseTrap.waiting
            }
        return StateT.next(self, input)


class Trapping(StateT):
    def run(self):
        print("Trapping: Closing door")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                BrewAction.alpha: MouseTrap.holding
            }
        return StateT.next(self, input)


class Holding(StateT):
    def run(self):
        print("Holding: Mouse caught")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                BrewAction.leutern: MouseTrap.waiting
            }
        return StateT.next(self, input)


class MouseTrap(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, MouseTrap.waiting)


# Static variable initialization:
MouseTrap.waiting = Waiting()
MouseTrap.luring = Luring()
MouseTrap.trapping = Trapping()
MouseTrap.holding = Holding()

moves = map(str.strip,
            open("MouseMoves.txt").readlines())
mouseMoves = map(BrewAction, moves)
MouseTrap().runAll(mouseMoves)
