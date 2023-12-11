from typing import List
from subprocess import run, DEVNULL
from os import path, listdir, mkdir
from tool import Tool

class Converter (Tool):
    def __init__(self) -> None:
        self.__videos: List[str] = []
        self.__outputDir: str = ""
        self.__isAudio: bool = False
        self.__newFormat: str = ""
    
    # getters and setters
    def setVideos(self, videos: List[str]) -> None:
        self.__videos = videos
    def getVideos(self) -> List[str]:
        return self.__videos
    def getDir(self) -> str:
        return self.__outputDir
    def setDir(self, outputDir: str) -> None:
        self.__outputDir = outputDir
    def isAudio(self) -> bool:
        return self.__isAudio
    def setIsAudio(self, isAudio: bool) -> None:
        self.__isAudio = isAudio
    def getNewFormat(self) -> str:
        return self.__newFormat
    def setNewFormat(self, newFormat: str) -> None:
        self.__newFormat = newFormat

    def askForInputs(self):
        print("Welcome to the converter!")
        videos = []
        options = ["1", "2"]
        audioOrVideo = input("Do you want to convert to 1) audio or 2) video? ").strip()
        self.validInput(audioOrVideo, options,lambda: self.setIsAudio(True), lambda: self.setIsAudio(False))
        dirOrFile = input("Do you want to convert a 1) directory or a 2) file? ").strip()
        self.validInput(dirOrFile, options, lambda: self.__getDirOrvideos__(True, videos), lambda: self.__getDirOrvideos__(False, videos))
        self.setDir(input("Enter the output directory: ").strip())
        if not path.exists(self.getDir()):
            mkdir(self.getDir())
        if not self.isAudio():
            self.setNewFormat(input("Enter the new format: ").strip())
        self.setVideos(videos)

    def __getDirOrvideos__(self, isDir: bool, videos: List[str]) -> None:
        if isDir:
            inputDir = input("Enter the directory path: ")
            videos = [path.join(inputDir, file) for file in listdir(inputDir) if path.splitext(file)[1] == ".mp4"]
        else:
            print("Enter the video paths. When you are done, press enter.")
            while True:
                video = input("Enter video path: ").strip()
                if video == "":
                    break
                videos.append(video)
        
    def convertToMp3(self, video: str, outputDir: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(".mp4", ".mp3"))
        # print convertion progress
        print(f"Converting {path.basename(video)} to mp3...")
        run(["ffmpeg", "-i", video, "-vn", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3", outputFile], stderr=DEVNULL, stdout=DEVNULL)
        # check if convertion was successful
        if not path.exists(outputFile):
            print(f"Error converting {path.basename(video)} to mp3")
            return
        print(f"Successfully converted {path.basename(video)} to mp3")
        
    def convertToNewFormat(self, video: str, outputDir: str, newFormat: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(".mp4", "." + newFormat))
        print(f"Converting {path.basename(video)} to {newFormat}...")
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
