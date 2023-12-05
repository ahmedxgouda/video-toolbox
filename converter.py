from typing import List
import subprocess
from os import path

class Converter:
    def __init__(self, videos: List[str], outputDir: str) -> None:
        self.__videos = videos
        self.__outputDir = outputDir
    def getVideos(self) -> List[str]:
        return self.__videos
    def getDir(self) -> str:
        return self.__outputDir
    def convertToMp3(self, video: str, outputDir: str) -> None:
        outputFile = path.join(outputDir, path.basename(video).replace(".mp4", ".mp3"))
        subprocess.run(["ffmpeg", "-i", video, "-vn", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3", outputFile])
    def convertDirToMp3(self):
        for video in self.getVideos():
            self.convertToMp3(video, self.getDir())