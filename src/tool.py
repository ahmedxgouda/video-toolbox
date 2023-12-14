from typing import Callable, List, Optional
from os import path, mkdir, remove

class Tool:
    def __init__(self) -> None:
        __outputDir: str = ""
    def setDir(self, outputDir: str) -> None:
        self.__outputDir = outputDir
    def getDir(self) -> str:
        return self.__outputDir
    
    def validInput(self, inp: str, options: List[str], thunks: List[Callable[[], None]]) -> None:
        while inp not in options:
            inp = input("Invalid input. Please try again: ").strip()
        for i in range(len(options)):
            if inp == options[i]:
                thunks[i]()
                break
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
        
    def printValidPath(self) -> None:
        print("Example for a valid path: path/to/your/file")
        print('''Example for a invalid path: "path/to/your/file"''')
    
    def keepOutputIfExists(self, outputFile: str) -> bool:
        if path.exists(outputFile):
            replace = input("There is a file with the same name as your output, do you want to replace it? (y/n) ").strip()
            while replace not in ["y", "n"]:
                replace = input("Invalid input. Please try again: ").strip()
            if replace == "y":
                remove(outputFile)
                return False
            return True
        return False