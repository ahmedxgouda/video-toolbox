from typing import List
import subprocess
from os import path, listdir

class Converter:
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
        videos = []
        self.__isAudio = input("To what do yow want to convert 1) an audio or 2) an another video format? ").lower() == "1"
        dirOrFile = input("Do you want to convert a 1) directory or a 2) file? ")
        if dirOrFile.lower() == "1":
            dir = input("Enter the directory path: ")
            videos = [path.join(dir, file) for file in listdir(dir) if path.splitext(file)[1] == ".mp4"]
        else:
            while True:
                video = input("Enter video path: ")
                if video == "":
                    break
                videos.append(video)
        self.__outputDir = input("Enter the output directory: ")
        if not self.__isAudio:
            self.__newFormat = input("Enter the new format: ")
        self.__videos = videos
    def convertToMp3(self, video: str, outputDir: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(".mp4", ".mp3"))
        subprocess.run(["ffmpeg", "-i", video, "-vn", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3", outputFile])
    def convertToNewFormat(self, video: str, outputDir: str, newFormat: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(".mp4", "." + newFormat))
        subprocess.run(["ffmpeg", "-i", video, outputFile])
    def convertAll(self):
        videos = self.getVideos()
        if self.__isAudio:
            for video in videos:
                self.convertToMp3(video, self.getDir())
        else:
            for video in videos:
                self.convertToNewFormat(video, self.getDir(), self.__newFormat)
        