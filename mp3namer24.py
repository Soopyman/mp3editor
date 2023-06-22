# Title: MP3 Metadata Editor/Downloader
# Author: Soopyman https://github.com/Soopyman

# References Used
# https://eyed3.readthedocs.io/en/latest/ #eyed3 documentation
# https://docs.python.org/3/library/os.html #os documentation
# https://y2down.cc/en/youtube-playlist.html higher quality mp3 downloader

import eyed3
import os
import pytube
from pytube import Playlist
from pytube import YouTube
from moviepy.editor import *

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

class songData:
    def __init__(self, title: str, filepath: str):
        self.title = title
        self.artist = ''
        self.album = ''
        self.tracknum = None
        self.filepath = filepath
        alist = self.filepath.split("\\")
        self.filename = alist[-1]

    def getFilepath(self):
        return self.filepath

    def getFilename(self):
        return self.filename

    def getTitle(self):
        return self.title

    def setTitle(self, title: str):
        self.title = title
    
    def editTitle(self, edit): #also strips of trailing white spaces
        self.title = self.title.replace(edit, '')
        self.title = self.title.strip()
    
    def getArtist(self):
        return self.artist

    def setArtist(self, artist):
        self.artist = artist
    
    def getAlbum(self):
        return self.album
    
    def setAlbum(self, album):
        self.album = album
    
    def getTrackNum(self):
        return self.tracknum
    
    def setTrackNum(self, tracknum):
        self.tracknum = tracknum

class fileEditor:
    def __init__(self):
        self.files = []
        self.filepath = ''
        self.orderedlist = ''
        self.albumartist = ''
        self.albumname = ''
    
    def initFiles(self, path):
        goodFolder = False
        loadedFolder = False
        if isinstance(path, str):
            choice = "Would you like to load from the most recent MP3 downloaded folder? Y/N: "
            userInput = getInput(choice)
            if userInput == 'y':
                self.filepath = path
                loadedFolder = True
            else:
                pass
        while not goodFolder:
            if loadedFolder == False:
                self.filepath = input("\n\n\nWARNING: Only MP3 Files will be read.\nPlease specify a filepath from your hard drive: ")
            try:
                self.files = os.listdir(path= self.filepath)
                for i in range(len(self.files)):
                    if ".mp3" not in self.files[i]:
                        self.files.pop(i)
                goodFolder = True
            except:
                print("Bad filepath!")
        self.writeData()
        if loadedFolder == True:
            self.sortByDate()
        self.setArtist()
        self.setAlbum()
        
    def writeData(self):
        for i in range(len(self.files)):
            songObj = songData(self.files[i][:-4], self.filepath+"\\"+self.files[i])    #initialize our song obj
            self.files[i] = songObj
    
    def sortByDate(self):
        newfiles = []
        os.chdir(self.filepath)
        files = filter(os.path.isfile, os.listdir(self.filepath))
        files = [os.path.join(self.filepath, f) for f in files]
        files.sort(key=lambda x: os.path.getmtime(x))
        for i in range(len(self.files)):  #length of the list of files
            strlist = files[i].split("\\")
            filename = strlist[-1]
            for j in range(len(self.files)): #find same filename
                if self.files[j].getFilename() == filename:
                    self.files[j].setTrackNum(i+1)
                    fileidx = j
                    break
            newfiles.append(self.files[fileidx])
        self.files = newfiles
    
    def sortAlphabetically(self):
        self.files.sort(key=lambda x: x.getTitle())
        for i in range(len(self.files)):
            self.files[i].setTrackNum(i+1)
    
    def sortByTrackNum(self):
        self.files.sort(key=lambda x: x.getTrackNum())
    
    def orderTracks(self):
        self.printFiles()
        userInput = input("\n\n\n 1. Order by date downloaded\n 2. Order alphabetically\n 3. Re-Order by Track Num\nPlease Enter 1-3 (or anything else to go back): ")
        if userInput == '1':
            self.sortByDate()
            print("Done.")
        elif userInput == '2':
            self.sortAlphabetically()
            print("Done.")
        elif userInput == '3':
            self.sortByTrackNum()
            print("Done.")

    def printFiles(self):
        print('\n\n\n\n')
        i = 1
        spacer = ")   "
        for song in self.files:
            if i==10:
                spacer = spacer[:-1]
            print("     "+str(i) + spacer + song.getTitle())
            i+=1

    def getOrdList(self):
        return self.orderedlist

    def getFiles(self):
        return self.files
    
    def getTitles(self):
        titlelist = []
        for i in range(len(self.files)):
            titlelist.append(self.files[i].getTitle())
        return titlelist
    
    def getPath(self):
        return self.filepath
    
    def getArtist(self):
        return self.albumartist
    
    def getAlbum(self):
        return self.albumname
    
    def setArtist(self):  #func to set the artists name for all songs
        goodArtist = False
        while not goodArtist:
            artistName = input("WARNING: This will set the artist name in the metadata for all songs.\nPlease enter the name of the artist for this Album/Set (or enter to skip): ")
            if artistName == '':
                return
            userInput = input(artistName + " is the correct artist? Y/N: ")
            if userInput.lower() == 'y':
                goodArtist = True
                self.albumartist = artistName
                for i in range(len(self.files)):
                    self.files[i].setArtist(artistName)
            
    def setAlbum(self):
        goodAlbum = False
        while not goodAlbum:
            albumName = input("Enter the name of the album (or enter nothing to skip): ")
            if albumName == '':
                goodAlbum = True
            else:
                userInput = input(albumName + " is the correct name for the album? Y/N: ")
                if userInput.lower() == 'y':
                    goodAlbum = True
                    self.albumname = albumName
                    for i in range(len(self.files)):
                        self.files[i].setAlbum(albumName)

    def removeSubstring(self):
        done = False
        while not done:
            self.printFiles()
            substring = input("What substring would you like to remove from ALL tracks?\n(You may enter nothing (''), as your substring to go back): ")
            if substring == '':
                done = True
                break
            userInput = input(substring + " is the string you want to be removed? Y/N: ")
            if userInput.lower() == 'y':
                for i in range(len(self.files)):
                    self.files[i].editTitle(substring)

    def removedOrderedNum(self):
        self.printFiles()
        userInput = input("Your files contain ascending numbers starting from what number? Enter nothing if you'd like to go back: ")
        if userInput == '':
            pass
        else:
            try:
                i = int(userInput)
                for j in range(len(self.files)):
                    self.files[j].editTitle(str(i))
                    i+=1
            except:
                print("Invalid Input")
    
    def fileSelect(self, string):
        validInput = False
        while not validInput:
            self.printFiles()
            userInput = input(string)
            if userInput == '':
                validInput = True
            else:
                try:
                    num = int(userInput)
                    if 1 <= num <= len(self.files):
                        validInput = True
                    else:
                        print("Invalid Track #\n")
                except:
                    print("Invalid Input!!!\n") 
        return userInput 
    
    def removeISubstring(self):
        done = False
        while not done:
            self.printFiles()
            choice = "Enter the song # you would like to remove a substring from\nOr enter nothing if you would like to exit and go back: "
            userInput = self.fileSelect(choice)
            if userInput == '':
                done = True
                break
            num = int(userInput)
            print("\n")
            idx = num-1
            title = self.files[idx].getTitle()
            print("    "+title)
            substring = input("What would you like to remove from the string? Enter nothing if you would like to go back: ")
            if substring == '':
                pass
            else:
                self.files[idx].editTitle(substring)

    def renameFiles(self):
        done = False
        while not done:
            self.printFiles()
            choice = "Enter the song # you would like to rename\nOr enter nothing if you would like to exit and go back: "
            userInput = self.fileSelect(choice)
            if userInput == '':
                done = True
                break
            num = int(userInput)
            idx = num-1
            title = self.files[idx].getTitle()
            print("\n    "+title)
            newname = input("What would you like to rename the file to? Enter nothing to skip this file: ")
            if newname == '':
                pass
            else:
                self.files[idx].setTitle(newname)

    def swapTracks(self):
        done = False
        while not done:
            choice = "WARNING: This will also swap Track Numbers (if they exist)\nWhat file would you like to select? (enter nothing to go back): "
            userInput = self.fileSelect(choice)
            if userInput == '':
                done = True
                break
            else:
                idxsel = int(userInput) - 1
                tempfileselected = self.files[idxsel]
                numsel = tempfileselected.getTrackNum()
            choice2 = "File Selected: "+tempfileselected.getTitle()+ "\nWhat is the other file you would like to select?: "
            userInput2 = self.fileSelect(choice2)
            if userInput2 == '':
                done = True
                break
            else:
                idxmove = int(userInput2) - 1
                tempfilemoveto = self.files[idxmove]
                nummove = tempfilemoveto.getTrackNum()
                tempfilemoveto.setTrackNum(numsel)
                tempfileselected.setTrackNum(nummove)
                done = True
            self.files[idxsel] = tempfilemoveto
            self.files[idxmove] = tempfileselected

    def changeMetadata(self):
        #manually change metadata of files
        done = False
        cont = False
        while not done:
            cont = False
            choice = "Enter a # for one of the songs above, or enter nothing to go back: "
            userInput = self.fileSelect(choice)
            if userInput == '':
                done = True
                break
            cont = True
            num = int(userInput)
            idx = num-1
            while cont == True:
                #now to prompt the user with choice of how to edit the metadata
                print("\n      Title: "+self.files[idx].getTitle()+"\n      Artist: "+self.files[idx].getArtist()+"\n      Album: "+self.files[idx].getAlbum()+"\n      Track #: "+str(self.files[idx].getTrackNum()))
                userInput = input("1. Change Title\n2. Change Artist Name\n3. Change Album Name\n4. Change Track #\n Any Other Key to Go Back: ")
                if userInput == '':
                    cont = False
                    break
                elif userInput == '1':
                    newtitle = input("What would you like to change the title of this track to? Enter nothing to go back: ")
                    if newtitle != '':
                        self.files[idx].setTitle(newtitle)
                elif userInput == '2':
                    newartist = input("What would you like to change the primary artist of this track to? Enter nothing to go back: ")
                    if newartist != '':
                        self.files[idx].setArtist(newartist)
                elif userInput == '3':
                    newalbum = input("What would you like to change the album name of this track to? Enter nothin to go back: ")
                    if newalbum != '':
                        self.files[idx].setAlbum(newalbum)
                elif userInput == '4':
                    newtracknum = input("What would you like the # of this track to be changed to? Enter nothing to go back: ")
                    if newtracknum != '':
                        try:
                            newtracknum = int(newtracknum)
                            self.files[idx].setTrackNum(newtracknum)
                        except:
                            print("Invalid Tracknum. Must be a Number.")
    
    def saveMetadata(self):
        #now we need to start adding our metadata to the files
        for song in self.files:
            file = eyed3.load(song.getFilepath())
            file.tag.artist = song.getArtist()
            file.tag.album = song.getAlbum()
            file.tag.album_artist = "Various Artists"
            file.tag.title = song.getTitle()
            if song.getTrackNum() != None:
                file.tag.track_num = song.getTrackNum()
            file.tag.save()
        print("Done.")


def downloadVideos():
    done = False
    path = ''
    while not done:
        playlistURL = input("Enter a valid YouTube Playlist Link (or enter nothing to go back): ")
        if playlistURL == '':
            done = True
            return path
        path = input("Enter the path you would like the playlist to be stored: ")
        p = Playlist(playlistURL)
        i = 0
        for url in p.video_urls:
            print(str(i) + " song(s) downloaded...")
            yt = YouTube(str(url))
            video = yt.streams.filter(only_audio=True).first()
            mp4file = video.download(output_path=path)
            mp4_without_frames = AudioFileClip(mp4file)     
            mp4_without_frames.write_audiofile(mp4file[:-4]+'.mp3')     
            mp4_without_frames.close() 
            os.remove(mp4file)
            i+=1
        print("\nDone!\n")
        choice = "Would you like to download another playlist? Y/N: "
        userInput = getInput(choice)
        if userInput == 'n':
            done = True
    return path

def filesNav(LoadedFileEditor):
    ourClass = LoadedFileEditor
    #prompt the user with choices
    done = False
    while not done:
        ourClass.printFiles()
        userInput = input("1. Remove a substring from all files\n2. Manually remove a string from each individual file\n3. Manually rename each file\n4. Remove ascending numbers\n5. Swap Tracks\n6. Metadata Settings\n7. Save metadata to files\n8. Go Back\nPLEASE ENTER AN INPUT 1-8: ")
        #1. remove a substring from all files
        if userInput == '1':
            ourClass.removeSubstring()
        #2. manually remove a string from each individual file
        elif userInput == '2':
            ourClass.removeISubstring()
        #3. manually rename each file
        elif userInput == '3':
            ourClass.renameFiles()
        #4. remove a ascending number order
        elif userInput == '4':
            ourClass.removedOrderedNum()
        #5. swap tracks
        elif userInput == '5':
            ourClass.swapTracks()
        #6. change settings
        elif userInput == '6':
            userInput2 = input("\n\n\n\n    1) Re-Initialize Files\n    2) Change Artist Name      "+ourClass.getArtist()+"\n    3) Change Album Name       "+ourClass.getAlbum()+"\n    4) Order Track Numbers\n    5) Manually Change Individual File Metadata\n Any Other Key) Back: ")
            try:
                num = int(userInput2)
                if 1 <= num <= 5:
                    if num == 1:
                        ourClass.initFiles(None)
                    if num == 2:
                        ourClass.setArtist()
                    if num == 3:
                        ourClass.setAlbum()
                    if num == 4:
                        ourClass.orderTracks()
                    if num == 5:
                        ourClass.changeMetadata()
            except:
                pass
        #7. save the metadata to the files
        elif userInput == '7':
            userInput3 = input("Are you sure you want to write to these files? All of your files metadata will be overwritten. Y/N: ")
            if userInput3.lower() == 'y':
                ourClass.saveMetadata()
                done = True
        #8. 
        elif userInput == '8':
            done = True
        else:
            print("Invalid Input. Please try again.")
    return ourClass

def main():

    exit = False
    isClass = False
    path = None
    newpath = None
    while not exit:

        navInput = input("\n\n\n\n\n Welcome to the MP3 Machine!\n\n1. Edit Current Files/New Files\n2. Download YouTube MP3 Playlist\n3. Exit the Program\nPlease Enter One of the 3 numbers above: ")
        #if our class doesnt exist
        if navInput == '1':
            if isClass == False:
                #initialize our class
                ourClass = fileEditor()
                ourClass.initFiles(path)
                isClass = True
            filesNav(ourClass)
        
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