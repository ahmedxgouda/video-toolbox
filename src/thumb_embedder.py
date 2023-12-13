from typing import List
from subprocess import run, DEVNULL
from os import path, remove, rename, mkdir
from tool import Tool

class ThumbEmbedder (Tool):
    def __init__(self) -> None:
        self.__videos: List[str] = []
        self.__images: List[str] = []
        self.__toRemove: bool = False

    def setVideos(self, videos: List[str]):
        self.__videos = videos
    def setImages(self, images: List[str]):
        self.__images = images
    def setToRemove(self, toRemove: bool):
        self.__toRemove = toRemove
    def toRemove(self) -> bool:
        return self.__toRemove
    def getVideos(self) -> List[str]:
        return self.__videos
    def getImages(self) -> List[str]:
        return self.__images

    def run(self):
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
        run(["ffmpeg", "-i", video, "-i", image, "-map", "0", "-map", "1", "-c", "copy", "-c:v:1", extension, "-disposition:v:1", "attached_pic", outputPath], stdout=DEVNULL, stderr=DEVNULL)

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
        print("Enter the video and image paths. When you are done, press enter.")
        self.printValidPath()
        videos = []
        images = []
        while True:
            video = input("Enter the video path: ").strip()
            video = self.validPath(video)
            while video != "" and path.splitext(video)[1] != ".mp4":
                video = input("The embedder only accepts mp4 format, use the Converter to to mp4, if you want, or you can enter another video path: ")
            if video == "":
                break
            image = input("Enter the image path: ").strip()
            image = self.validPath(image)
            videos.append(video)
            images.append(image)
        self.setVideos(videos)
        self.setImages(images)
        super().askForInputs()
        wantToRemove = input("Do you want to remove the original videos? ").strip().lower()
        self.validInput(wantToRemove, ["yes", "no"], lambda: self.setToRemove(True), lambda: self.setToRemove(False))
            