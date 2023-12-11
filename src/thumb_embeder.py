from typing import List
import subprocess
from os import path, remove, rename, mkdir

class ThumbEmbeder:
    def __init__(self) -> None:
        self.__videos: List[str] = []
        self.__images: List[str] = []
        self.__outputDir: str = ""
        self.__toRemove: bool = False

    def setVideos(self, videos: List[str]):
        self.__videos = videos
    def setImages(self, images: List[str]):
        self.__images = images
    def setDir(self, outputDir: str):
        self.__outputDir = outputDir
    def setToRemove(self, toRemove: bool):
        self.__toRemove = toRemove
    def toRemove(self) -> bool:
        return self.__toRemove
    def getVideos(self) -> List[str]:
        return self.__videos
    def getImages(self) -> List[str]:
        return self.__images
    def getDir(self) -> str:
        return self.__outputDir

    def embedThumbs(self):
        videos = self.getVideos()
        images = self.getImages()
        if len(videos) != len(images):
            raise ValueError("The number of videos and images must be the same")
        for i in range(len(videos)):
            self.embedThumb(videos[i], images[i])

    def embedThumb(self, video: str, image: str):
        if not path.exists(self.getDir()):
            mkdir(self.getDir())

        outputPath = video.replace(path.dirname(video), self.getDir())
        outputPath = outputPath.replace(path.splitext(outputPath)[1], "-thumb" + path.splitext(outputPath)[1])
        extension = path.splitext(image)[1][1:]
        print("Embedding thumbnail...")
        subprocess.run(["ffmpeg", "-i", video, "-i", image, "-map", "0", "-map", "1", "-c", "copy", "-c:v:1", extension, "-disposition:v:1", "attached_pic", outputPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if not path.exists(outputPath):
            print("Error embedding thumbnail")
            return
        print("Successfully embedded thumbnail")
        self.__removeOriginal(video, outputPath)
    def __removeOriginal(self, videoPath: str, outputPath: str):
        if self.toRemove():
            if path.exists(outputPath):
                remove(videoPath)
                # rename the output file to the original name with the output directory
                rename(outputPath, videoPath.replace(path.dirname(videoPath), self.getDir()))

    def askForInputs(self):
        print("Welcome to the Thumb-Embeder!")
        videos = []
        images = []
        while True:
            video = input("Enter the video path: ").strip()
            image = input("Enter the image path: ").strip()
            videos.append(video)
            images.append(image)
            if input("Do you want to add more videos and images? ").strip().lower() == "no":
                break
        self.setVideos(videos)
        self.setImages(images)
        self.setDir(input("Enter the output directory: ").strip())
        self.setToRemove(input("Do you want to keep the original videos? ").strip().lower() == "no")