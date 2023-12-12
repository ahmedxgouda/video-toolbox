from typing import Callable, List
from os import path, mkdir

class Tool:
    def __init__(self) -> None:
        __outputDir: str = ""
    def setDir(self, outputDir: str) -> None:
        self.__outputDir = outputDir
    def getDir(self) -> str:
        return self.__outputDir
    
    def validInput(self, inp: str, options: List[str], thunk1: Callable[[], None], thunk2: Callable[[], None]) -> None:
        while inp not in options:
            inp = input("Invalid input. Please try again: ").strip()
        if inp == options[0]:
            thunk1()
        else:
            thunk2()
    def askForInputs(self) -> None:
        self.setDir(input("Enter the output directory: ").strip())
        self.createDirIfNotExists()
    def run(self) -> None:
        pass
    def validPath(self, inputPath: str) -> str:
        while inputPath != "" and not (path.exists(inputPath) and path.isfile(inputPath)):
            inputPath = input("Invalid path. Please try again: ").strip()
        return inputPath
        
    def validDir(self, inputDir: str) -> str:
        while inputDir != "" and not (path.exists(inputDir) and path.isdir(inputDir)):
            inputDir = input("Invalid directory. Please try again: ").strip()
        return inputDir
    
    def createDirIfNotExists(self) -> None:
        if not path.exists(self.getDir()):
            mkdir(self.getDir())
    