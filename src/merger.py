from typing import List, Tuple
from subprocess import run, DEVNULL
from os import path
from tool import Tool

class Merger (Tool):
    def __init__(self) -> None:
        self.__videos: List[str] = []
        self.__newVideo: str = ""
        self.__resolution: Tuple[str, str] = ("1920", "1080")
    def getVideos(self) -> List[str]:
        return self.__videos
    def setVideos(self, videos: List[str]) -> None:
        self.__videos = videos
    def getNewVideo(self) -> str:
        return self.__newVideo
    def setNewVideo(self, newVideo: str) -> None:
        self.__newVideo = newVideo
    def getResolution(self) -> Tuple[str, str]:
        return self.__resolution
    def setResolution(self, resolution: Tuple[str, str]) -> None:
        self.__resolution = resolution

    def askForInputs(self):
        print("Welcome to the merger!")
        print("Enter the video paths. When you are done, press enter.")
        self.printValidPath()
        videos = []
        while True:
            video = input("Enter video path: ").strip()
            video = self.validPath(video)
            if video == "":
                break
            videos.append(video)
        super().askForInputs()
        self.setNewVideo(input("Enter the new video name: ").strip())
        quality = input("Choose the quality of the video from the optionts below:\n1) 1080p\n2) 720p\n3) 480p\n4) 360p: ").strip()
        options = ["1", "2", "3", "4"]
        self.validInput(quality, options, [lambda: self.setResolution(("1920", "1080")), lambda: self.setResolution(("1280", "720")), lambda: self.setResolution(("854", "480")), lambda: self.setResolution(("640", "360"))])
        self.setVideos(videos)
    def run(self):
        print("Merging...")
        outputFile = path.join(self.getDir(), self.getNewVideo() + ".mkv")
        if self.keepOutputIfExists(outputFile):
            return
        # for changing the resolution of every video to 1920x1080
        filterComplexVideo = ""
        # for changing the audio channel layout to stereo
        filterComplexAudio = ""
        # for concatenating the output streams
        filterComplexOutput = ""
        # The command to run
        ffmpegCommand = ["ffmpeg"]
        for i in range(len(self.getVideos())):
            filterComplexVideo += f"[{i}:v]scale={self.getResolution()[0]}:{self.getResolution()[1]}[v{i}];"
            filterComplexAudio += f"[{i}:a]aformat=channel_layouts=stereo[a{i}];"
            filterComplexOutput += f"[v{i}][a{i}]"
            ffmpegCommand.append("-i")
            ffmpegCommand.append(self.getVideos()[i])
        # Now, combine the filter complexes and add them to the command
        filterComplex = filterComplexVideo + filterComplexAudio + filterComplexOutput
        filterComplex += f"concat=n={len(self.getVideos())}:v=1:a=1[v][a]"
        ffmpegCommand += ["-filter_complex", filterComplex, "-map", "[v]", "-map", "[a]", outputFile]
        run(ffmpegCommand)
        if not path.exists(outputFile):
            print("Error merging")
            return
        print(f"Successfully merged to {path.basename(outputFile)}")
