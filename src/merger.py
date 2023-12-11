from typing import List
from subprocess import run, DEVNULL
from os import path
from tool import Tool

class Merger (Tool):
    def __init__(self) -> None:
        self.__videos: List[str] = []
        self.__outputDir: str = ""
        self.__newVideo: str = ""
    def getVideos(self) -> List[str]:
        return self.__videos
    def setVideos(self, videos: List[str]) -> None:
        self.__videos = videos
    def getDir(self) -> str:
        return self.__outputDir
    def setDir(self, outputDir: str) -> None:
        self.__outputDir = outputDir
    def getNewVideo(self) -> str:
        return self.__newVideo
    def setNewVideo(self, newVideo: str) -> None:
        self.__newVideo = newVideo
    def askForInputs(self):
        print("Welcome to the merger!")
        print("Enter the video paths. When you are done, press enter.")
        print("Please, make sure that all the videos have the same encoding, resolution and format.")
        videos = []
        while True:
            video = input("Enter video path: ").strip()
            if video == "":
                break
            videos.append(video)
        self.setDir(input("Enter the output directory: ").strip())
        self.setNewVideo(input("Enter the new video name: ").strip())
        self.setVideos(videos)
    def run(self):
        print("Merging...")
        outputFile = path.join(self.__outputDir, self.__newVideo)
        with open("files.txt", "w") as f:
            for video in self.__videos:
                f.write(f"file '{video}'\n")
        run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "files.txt", "-c", "copy", outputFile], stderr=DEVNULL, stdout=DEVNULL)
        # remove the txt file after merging
        run(["rm", "files.txt"])
        if not path.exists(outputFile):
            print("Error merging")
            return
        print(f"Successfully merged to {path.basename(outputFile)}")
