from typing import List
import subprocess
from os import path, remove, rename

class ThumbEmbeder:
    def setVideos(self, videos: List[str]):
        self.__videos = videos
    def setImages(self, images: List[str]):
        self.__images = images
    def setDir(self, outputDir: str):
        self.__outputDir = outputDir
    def setToRemove(self, toRemove: bool):
        self.__toRemove = toRemove
    def getVideos(self) -> List[str]:
        return self.__videos
    def getImages(self) -> List[str]:
        return self.__images
    def getDir(self) -> str:
        return self.__outputDir
    def toRemove(self) -> bool:
        return self.__toRemove
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
        extension = path.splitext(image)[1][1:]
        print("Embedding thumbnail...")
        try:
            subprocess.run(["ffmpeg", "-i", video, "-i", image, "-map", "0", "-map", "1", "-c", "copy", "-c:v:1", extension, "-disposition:v:1", "attached_pic", outputPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # get the stdout and stderr of the command
            print("Thumbnail embedded")
            self.__removeOriginal(video, outputPath)
        except:
            print("Failed to embed thumbnail")
    def __removeOriginal(self, videoPath: str, outputPath: str):
        if self.toRemove():
            if path.exists(outputPath):
                remove(videoPath)
                # rename the output file to the original name with the output directory
                rename(outputPath, videoPath.replace(path.dirname(videoPath), self.getDir()))
    def askForInputs(self):
        videos = []
        images = []
        while True:
            video = input("Enter the video path: ")
            image = input("Enter the image path: ")
            videos.append(video)
            images.append(image)
            if input("Do you want to add more videos and images? ").lower() == "no":
                break
        self.__videos = videos
        self.__images = images
        self.__outputDir = input("Enter the output directory: ")
        self.__toRemove = input("Do you want to keep the original videos? ").lower() == "no"