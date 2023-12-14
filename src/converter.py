from typing import List
from subprocess import run, DEVNULL
from os import path, listdir, mkdir, remove
from tool import Tool

class Converter (Tool):
    def __init__(self) -> None:
        self.__videos: List[str] = []
        self.__isAudio: bool = False
        self.__newFormat: str = ""
        self.__validFormats: List[str] = ["mp4", "mkv", "avi", "webm", "mov", "flv", "wmv", "mpg", "mpeg", "m4v"]
    
    # getters and setters
    def setVideos(self, videos: List[str]) -> None:
        self.__videos = videos
    def getVideos(self) -> List[str]:
        return self.__videos
    def isAudio(self) -> bool:
        return self.__isAudio
    def setIsAudio(self, isAudio: bool) -> None:
        self.__isAudio = isAudio
    def getNewFormat(self) -> str:
        return self.__newFormat
    def setNewFormat(self, newFormat: str) -> None:
        self.__newFormat = newFormat
    def getValidFormats(self) -> List[str]:
        return self.__validFormats
    def setValidFormats(self, validFormats: List[str]) -> None:
        self.__validFormats = validFormats

    def askForInputs(self):
        print("Welcome to the converter!")
        videos = []
        options = ["1", "2"]
        audioOrVideo = input("Please, choose the conversion type:\n1) Video -> Audio\n2) Video -> Another Format of Video ").strip()
        self.validInput(audioOrVideo, options, [lambda: self.setIsAudio(True), lambda: self.setIsAudio(False)])
        dirOrFile = input("Do you want to convert a 1) directory or a 2) file? ").strip()
        self.validInput(dirOrFile, options, [lambda: self.__getDirOrvideos__(True, videos), lambda: self.__getDirOrvideos__(False, videos)])
        super().askForInputs()
        self.setVideos(videos)

        if not self.isAudio():
            newFormat = input("Enter the new format: ").strip()
            while newFormat not in self.getValidFormats():
                newFormat = input("Invalid format. Please try again: ").strip()
            self.setNewFormat(newFormat)

    def __getDirOrvideos__(self, isDir: bool, videos: List[str]) -> None:
        if isDir:
            inputDir = input("Enter the directory path: ")
            inputDir = self.validDir(inputDir)
            for file in listdir(inputDir):
                if path.splitext(file)[1][1:] in self.getValidFormats():
                    videos.append(path.join(inputDir, file))
        else:
            print("Enter the video paths. When you are done, press enter.")
            self.printValidPath()
            while True:
                video = input("Enter video path: ").strip()
                video = self.validPath(video)
                if video == "":
                    break
                videos.append(video)
        
    def convertToMp3(self, video: str, outputDir: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(path.splitext(video)[1], ".mp3"))
        # print convertion progress
        print(f"Converting {path.basename(video)} to mp3...")
        if self.keepOutputIfExists(outputFile):
            return
        run(["ffmpeg", "-i", video, "-vn", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3", outputFile], stderr=DEVNULL, stdout=DEVNULL)
        # check if convertion was successful
        if not path.exists(outputFile):
            print(f"Error converting {path.basename(video)} to mp3")
            return
        print(f"Successfully converted {path.basename(video)} to mp3")
        
    def convertToNewFormat(self, video: str, outputDir: str, newFormat: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(path.splitext(video)[1], "." + newFormat))
        print(f"Converting {path.basename(video)} to {newFormat}...")
        if self.keepOutputIfExists(outputFile):
            return
        run(["ffmpeg", "-i", video, outputFile], stderr=DEVNULL, stdout=DEVNULL)
        if not path.exists(outputFile):
            print(f"Error converting {path.basename(video)} to {newFormat}")
            return
        print(f"Successfully converted {path.basename(video)} to {newFormat}")

    def run(self):
        videos = self.getVideos()
        if self.isAudio():
            for video in videos:
                
                self.convertToMp3(video, self.getDir())
        else:
            for video in videos:
                self.convertToNewFormat(video, self.getDir(), self.getNewFormat())
