from converter import Converter
from merger import Merger
from clipper import Clipper
from thumb_embeder import ThumbEmbeder
from tool import Tool
from os import path, name as osName, listdir
from requests import get
from zipfile import ZipFile
from io import BytesIO
from subprocess import run, DEVNULL
from typing import Optional
from shutil import move, rmtree

class Program:
    def __init__(self) -> None:
        self.__tool: Optional[Tool] = None
        
    def getTool(self) -> Optional[Tool]:
        return self.__tool
    def setTool(self, tool: Optional[Tool]) -> None:
        self.__tool = tool

    def main(self):
        # check if ffmpeg is installed for windows and if not, download it and add it to the path
        self.__installFFmpeg()
        print("Hello to your platform to play with videos!\nWhich tool do you want to use?")
        while True:
            option = input("1) Thumb-Embeder\n2) Video-Converter\n3) Video-Merger\n4) Video-Clipper: ").strip()
            if option in ["1", "2", "3", "4"]:
                break
            print("Invalid option")
        if option == "1":
            self.setTool(ThumbEmbeder())
        elif option == "2":
            self.setTool(Converter())
        elif option == "3":
            self.setTool(Merger())
        elif option == "4":
            self.setTool(Clipper())
        else:
            print("Invalid option")
            return
        self.getTool().askForInputs()
        self.getTool().run()

    def __installFFmpeg(self) -> None:
        # call ffmpeg to check if it is installed
        try:
            run(["ffmpeg", "-version"], stdout=DEVNULL, stderr=DEVNULL)
        except:
            print("ffmpeg is not installed")
            if osName == "nt":
                print("Downloading ffmpeg...")
                request = get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
                tempDir = "temp"
                zipFile = ZipFile(BytesIO(request.content))
                zipFile.extractall(tempDir)
                # move the exe files to the path
                for file in listdir(tempDir):
                    move(path.join(tempDir, file), path.join("C:\\", "Windows", "System32", file))
                rmtree(tempDir)
                print("ffmpeg downloaded")
            else:
                print("Please install ffmpeg")
                return
if __name__ == "__main__":
    main = Program()
    main.main()
    while True:
        again = input("Do you want to use another tool? (y/n): ").lower().strip()
        if again == "y":
            main = Program()
            main.main()
        elif again == "n":
            input("Press enter to exit")
            break
        else:
            print("Invalid option")
            continue
