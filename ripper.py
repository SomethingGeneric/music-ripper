import os, sys

import youtube_dl
from youtubesearchpython import VideosSearch

try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def print_lines(lines):
    c = 0
    for line in lines:
        print(str(c) + " : " + line)
        c += 1

if len(sys.argv) > 1:
    data_fn = sys.argv[1]
    print("We'll load data from " + data_fn)
    with open(data_fn) as f:
        lines = f.read().split("\n")
else:

    in_fn = input("Image filename: ")

    raw = pytesseract.image_to_string(Image.open(in_fn))

    lines = raw.split("\n")

    for line in lines:
        if len(line.replace(" ", "")) < 6:
            lines.remove(line)
        #if line == "" or line == " ":
        #    lines.remove(line)

    c = 0
    for line in lines:
        print(str(c) + " : " + line)
        c += 1

    rem = True
    while rem:
        remove = input("Enter # to remove (or blank when done): ")
        if remove == "" or remove == "\n":
            rem = False
            pass
        else:
            try:
                index = int(remove)
                lines.pop(index)
                print("New data: ")
                print_lines(lines)
            except IndexError:
                print("No such #")
            except:
                print("Is that a number?")

    print("Trimmed data: ")
    print_lines(lines)

    edit = True
    while edit:
        n = input("Enter # to edit (or blank when done): ")
        if n == "" or n == "\n":
            edit = False
            pass
        else:
            try:
                index = int(n)
                new = input("New value for " + n + " : ")
                lines[index] = new
                print("New data: ")
                print_lines(lines)
            except IndexError:
                print("No such #")
            except:
                print("uhh something's fucked")

    print("Edited data: ")
    print_lines(lines)

    cmb = False if input("Would you like to combine lines? (Y/n)") == "n" else True

    if cmb:
        more = True
        while more:
            indices = input("Enter #,# (or blank if done): ")
            if "," in indices and indices != "":
                nums = indices.split(",")
                if nums[0].isdigit() and nums[1].isdigit():
                    first = int(nums[0])
                    second = int(nums[1])
                    try:
                        lines[first] = lines[first] + " " + lines[second]
                        lines.pop(second)
                        print("New data: ")
                        print_lines(lines)
                    except:
                        print("you goofed")
            else:
                more = False

    print("Combined data: ")
    print_lines(lines)

    sv = False if input("Would you like to save the output? (Y/n)") == "n" else True

    if sv:
        fn = input("Filename: ")
        with open(fn, "w") as f:
            f.write("\n".join(lines))


download = False if input("Would you like to download files? (Y/n)") == "n" else True

if not download:
    sys.exit(1)
else:
    for line in lines:
        try:
            print("Searching " + line)
            videosSearch = VideosSearch(line, limit=1)

            first = videosSearch.result()["result"][0]

            print(" -- Video info -- ")
            print("Title: " + first["title"])
            print("Published: " + first["publishedTime"])
            print("Duration: " + first["duration"])
            print("Link: " + first["link"])
            print(" ---------------- ")

            get = (
                False
                if input("Would you like to download this video? (Y/n)") == "n"
                else True
            )

            if get:
                print("Downloading...")
                ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([first["link"]])
        except Exception as e:
            print("Failed on " + line + ": " + str(e))

print("All done. :)")