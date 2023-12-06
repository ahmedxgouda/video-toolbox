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
    def convertToMp3(self, video: str, outputDir: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(".mp4", ".mp3"))
        subprocess.run(["ffmpeg", "-i", video, "-vn", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3", outputFile])
    def convertDirToMp3(self):
        for video in self.getVideos():
            self.convertToMp3(video, self.getDir())
    def askForInputs(self):
        videos = []
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
        self.__videos = videos
        