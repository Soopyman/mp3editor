# Title: MP3 Metadata Editor/Downloader
# Author: Soopyman https://github.com/Soopyman

# References Used
# https://eyed3.readthedocs.io/en/latest/ #eyed3 documentation
# https://docs.python.org/3/library/os.html #os documentation
# https://y2down.cc/en/youtube-playlist.html higher quality mp3 downloader

#file that contains main class (and a few other functions such as downloading videos)
#the main class acts as a sort of main hub to the program

import os #to access files and file information
import yt_dlp #to download from youtube
from pytube import Playlist #to grab each individual URL within a playlist

from files import fileEditor #to edit files (guts of the program)


# method to check if user had a valid y/n input
# returns the user input if so
def getInput(string):
    inputs = ['y', 'n']
    validInput = False
    while not validInput:
        userInput = input(string)
        userInput = userInput.lower()
        if userInput in inputs:
            validInput = True
        else:
            print("Input is invalid. Must enter Y/N.")
    return userInput

def downloadVideos():
    done = False
    path = ''
    while not done:
        playlist = False
        playlistURL = input("\nEnter a valid YouTube Playlist/Video Link (or enter nothing to go back): ")
        if playlistURL == '':
            done = True
            return path
        if "playlist?list" in playlistURL:
            playlist = True
        path = input("Enter the path you would like the playlist to be stored: ")
        p = Playlist(playlistURL)
        yt_opts = {
                'outtmpl': path+'/%(title)s.%(ext)s',
                'format': 'bestaudio',
                'ffmpeg_location': os.path.dirname(__file__) + '\\ffmpeg\\bin\\ffmpeg.exe',
                'cachedir': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        ydl = yt_dlp.YoutubeDL(yt_opts)
        i = 0
        if playlist == False:
            try:
                ydl.download(playlistURL)
            except:
                print("An Error Has Been Raised. Please try again.")
        else:
            for url in p.video_urls:
                downloaded = False
                while not downloaded:
                    try:
                        ydl.download(url)
                        downloaded = True
                    except:
                        print("Error. Retrying download...")
                i+=1
                print(str(i) + " song(s) downloaded...")
            print("\nDone!\n")
        choice = "Would you like to download another playlist? Y/N: "
        userInput = getInput(choice)
        if userInput == 'n':
            done = True
    return path

def main():

    exit = False
    isClass = False
    path = None
    newpath = None
    clearPath = False
    while not exit:

        navInput = input("\n\n\n\n\n\n\n\n\n\n\n\n\n Welcome to the MP3 Machine!\n    by Soopyman\n\n\n\n1. Edit Current Files/New Files\n2. Download YouTube MP3 Playlist\n3. Exit the Program\nPlease Enter One of the 3 numbers above: ")
        #if our class doesnt exist
        if navInput == '1':
            if path != None:
                choice = "Would you like to load from the most recently downloaded Playlist? Y/N: "
                userInput = getInput(choice)
                if userInput == 'y':
                    clearPath = True
                    isClass = False
                else:
                    path = None
            if isClass == False:
                #initialize our class
                ourClass = fileEditor()
                ourClass.initFiles(path)
                isClass = True
            if clearPath:
                path = None
                clearPath = False
            ourClass.filesNav()
        
        elif navInput == '2':
            #download mp3 files if necessary
            newpath = downloadVideos()
            if newpath != '':
                path = newpath

        elif navInput == '3':
            exit = True

        else:
            print("Invalid Input.")

main()