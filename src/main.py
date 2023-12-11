from converter import Converter
from merger import Merger
from clipper import Clipper
from thumb_embeder import ThumbEmbeder
from os import path, name as osName
from requests import get
from zipfile import ZipFile
from io import BytesIO
from subprocess import run, DEVNULL

class Program:
    def __init__(self) -> None:
        self.__embeder = ThumbEmbeder()
        self.__converter = Converter()
        self.__merger = Merger()
        self.__clipper = Clipper()

    def setEmbeder(self, embeder: ThumbEmbeder) -> None:
        self.__embeder = embeder
    def getEmbeder(self) -> ThumbEmbeder:
        return self.__embeder
    def setConverter(self, converter: Converter) -> None:
        self.__converter = converter
    def getConverter(self) -> Converter:
        return self.__converter
    def setMerger(self, merger: Merger) -> None:
        self.__merger = merger
    def getMerger(self) -> Merger:
        return self.__merger
    def setClipper(self, clipper: Clipper) -> None:
        self.__clipper = clipper
    def getClipper(self) -> Clipper:
        return self.__clipper

    def main(self):
        # check if ffmpeg is installed for windows and if not, download it and add it to the path
        self.installFFmpeg()
        print("Hello to your platform to play with videos!\nWhich tool do you want to use?")
        while True:
            option = input("1) Thumb-Embeder\n2) Video-Converter\n3) Video-Merger\n4) Video-Clipper: ").strip()
            if option in ["1", "2", "3", "4"]:
                break
            print("Invalid option")
        if option == "1":
            self.getEmbeder().askForInputs()
            self.getEmbeder().embedThumbs()
        elif option == "2":
            self.getConverter().askForInputs()
            self.getConverter().convertAll()
        elif option == "3":
            self.getMerger().askForInputs()
            self.getMerger().merge()
        elif option == "4":
            self.getClipper().askForInputs()
            self.getClipper().clip()
        else:
            print("Invalid option")
            return

    def installFFmpeg(self) -> None:
        # call ffmpeg to check if it is installed
        try:
            run(["ffmpeg", "-version"], stdout=DEVNULL, stderr=DEVNULL)
        except:
            print("ffmpeg is not installed")
            if osName == "nt":
                print("Downloading ffmpeg...")
                r = get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
                z = ZipFile(BytesIO(r.content))
                # get the exe files from the zip file and move them to the Windows directory
                for file in z.namelist():
                    if path.splitext(file)[1] == ".exe":
                        z.extract(file, "C:\\Windows\\System32\\")
                print("ffmpeg downloaded")
            else:
                print("Please install ffmpeg")
                return
if __name__ == "__main__":
    main = Program()
    main.main()
    while True:
        again = input("Do you want to use another tool? (y/n): ")
        if again == "y":
            main = Program()
            main.main()
        elif again == "n":
            input("Press enter to exit")
            break
        else:
            print("Invalid option")
            continue