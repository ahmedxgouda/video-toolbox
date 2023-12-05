from typing import List
import subprocess
from os import path, remove, rename

class ThumbEmbeder:
    def __init__(self, videos: List[str], images: List[str], outputDir: str, keepOriginal: bool) -> None:
        self.__videos = videos
        self.__images = images
        self.__outputDir = outputDir
        self.__keepOriginal = keepOriginal
    def getVideos(self) -> List[str]:
        return self.__videos
    def getImages(self) -> List[str]:
        return self.__images
    def getDir(self) -> str:
        return self.__outputDir
    def toRemove(self) -> bool:
        return self.__keepOriginal
    def embedThumbs(self):
        videos = self.getVideos()
        images = self.getImages()
        if len(videos) != len(images):
            raise ValueError("The number of videos and images must be the same")
        for i in range(len(videos)):
            self.embedThumb(videos[i], images[i])
    def embedThumb(self, video: str, image: str):
        outputPath = video.replace(path.dirname(video), self.getDir())
        outputPath = outputPath.replace(path.splitext(outputPath)[1], "-thumb" + path.splitext(outputPath)[1])
        subprocess.run(["ffmpeg", "-i", video, "-i", image, "-map", "0", "-map", "1", "-c", "copy", "-c:v:1", "png", "-disposition:v:1", "attached_pic", outputPath])
        self.removeOriginal(video, outputPath)
    def removeOriginal(self, videoPath: str, outputPath: str):
        if self.toRemove():
            if path.exists(outputPath):
                remove(videoPath)
                rename(outputPath, videoPath)