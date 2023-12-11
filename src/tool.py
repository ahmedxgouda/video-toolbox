from typing import Callable, List

class Tool:
    def validInput(self, inp: str, options: List[str], thunk1: Callable[[], None], thunk2: Callable[[], None]):
        while inp not in options:
            inp = input("Invalid input. Please try again: ").strip()
        if inp == options[0]:
            thunk1()
        else:
            thunk2()
    def askForInputs(self):
        pass
    def run(self):
        pass
    