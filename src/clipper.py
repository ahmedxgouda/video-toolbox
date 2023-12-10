from os import path, mkdir
from subprocess import run, DEVNULL

class Clipper:
    __video = ""
    __outputDir = ""
    __start = ""
    __end = ""
    __newVideo = ""
    def getVideo(self) -> str:
        return self.__video
    def setVideo(self, video: str) -> None:
        self.__video = video
    def getDir(self) -> str:
        return self.__outputDir
    def setDir(self, outputDir: str) -> None:
        self.__outputDir = outputDir
    def getStart(self) -> str:
        return self.__start
    def setStart(self, start: str) -> None:
        self.__start = start
    def getEnd(self) -> str:
        return self.__end
    def setEnd(self, end: str) -> None:
        self.__end = end
    def getNewVideo(self) -> str:
        return self.__newVideo
    def setNewVideo(self, newVideo: str) -> None:
        self.__newVideo = newVideo
    def askForInputs(self) -> None:
        print("Welcome to the clipper!")
        self.__video = input("Enter video path: ")
        self.__outputDir = input("Enter the output directory: ")
        if not path.exists(self.__outputDir):
            mkdir(self.__outputDir)
        print("Enter the start and end times in the format hh:mm:ss")
        self.__start = input("Enter start time: ")
        self.__end = input("Enter end time: ")
        self.__newVideo = input("Enter the new clip name: ")
    def clip(self) -> None:
        outputFile = path.join(self.__outputDir, self.__newVideo)
        print(f"Clipping {path.basename(self.__video)} from {self.__start} to {self.__end}...")
        run(["ffmpeg", "-i", self.__video, "-ss", self.__start, "-to", self.__end, outputFile], stderr=DEVNULL, stdout=DEVNULL)
        if not path.exists(outputFile):
            print(f"Error clipping {path.basename(self.__video)}")
            return
        print(f"Here is your new clip: {path.basename(outputFile)}")