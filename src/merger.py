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
        outputFile = path.join(self.getDir(), self.getNewVideo())
        filterComplex = ""
        ffmpegCommand = ["ffmpeg"]
        for i in range(len(self.getVideos())):
            filterComplex += f"[{i}:v]scale=1920:1080,setsar=1/1[v{i}];"
            ffmpegCommand.append("-i")
            ffmpegCommand.append(self.getVideos()[i])
        for i in range(len(self.getVideos())):
            filterComplex += f"[{i}:a]aformat=channel_layouts=stereo[a{i}];"
        for i in range(len(self.getVideos())):
            filterComplex += f"[v{i}][a{i}]"
        filterComplex += f"concat=n={len(self.getVideos())}:v=1:a=1[v][a]"
        ffmpegCommand += ["-filter_complex", filterComplex, "-map", "[v]", "-map", "[a]", outputFile]
        run(ffmpegCommand, stdout=DEVNULL, stderr=DEVNULL)
        if not path.exists(outputFile):
            print("Error merging")
            return
        print(f"Successfully merged to {path.basename(outputFile)}")
