from os import path, mkdir
from subprocess import run, DEVNULL

class Clipper:
    def __init__(self) -> None:    
        self.__video = ""
        self.__outputDir = ""
        self.__start = ""
        self.__end = ""
        self.__newVideo = ""
    
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
        self.setVideo(input("Enter video path: ").strip())
        self.setDir(input("Enter the output directory: ").strip())
        if not path.exists(self.getDir()):
            mkdir(self.getDir())
        print("Enter the start and end times in the format hh:mm:ss")
        self.setStart(input("Enter start time: ").strip())
        self.setEnd(input("Enter end time: ").strip())
        self.setNewVideo(input("Enter the new clip name: ").strip())
    def clip(self) -> None:
        outputFile = path.join(self.getDir(), self.getNewVideo())
        print(f"Clipping {path.basename(self.getVideo())} from {self.getStart()} to {self.getEnd()}...")
        run(["ffmpeg", "-i", self.getVideo(), "-ss", self.getStart(), "-to", self.getEnd(), outputFile], stderr=DEVNULL, stdout=DEVNULL)
        if not path.exists(outputFile):
            print(f"Error clipping {path.basename(self.getVideo())}")
            return
        print(f"Here is your new clip: {path.basename(outputFile)}")