# Title: File Editor Class
# Author: Soopyman https://github.com/Soopyman
import eyed3
import os
from song import songData

#This is a class used to init, save, edit, and sort files/metadata accordingly.
#this class is also used to navigate, and display files
#the song class and files class work together to store and use information to make editing metadata a little easier
# the main guts of the program.

def getInput(string):   # y/n input method
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
            self.filepath = path
            loadedFolder = True
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

    def filesNav(self):
        #prompt the user with choices
        done = False
        while not done:
            self.printFiles()
            userInput = input("\n1. Remove a substring from all files\n2. Manually remove a string from each individual file\n3. Manually rename each file\n4. Order/Swap Tracks & Track #'s\n5. Metadata Settings\n6. Save metadata to files\n7. Go Back\nPLEASE ENTER AN INPUT 1-7: ")
            #1. remove a substring from all files
            if userInput == '1':
                self.removeSubstring()
            #2. manually remove a string from each individual file
            elif userInput == '2':
                self.removeISubstring()
            #3. manually rename each file
            elif userInput == '3':
                self.renameFiles()
            #4. order/swap tracks
            elif userInput == '4':
                self.orderTracks()
            #5. change settings
            elif userInput == '5':
                userInput2 = input("\n\n\n\n\n\n\n\n\n\n\n\n\n\n    1) Re-Initialize Files\n    2) Change Artist Name      "+self.getArtist()+"\n    3) Change Album Name       "+self.getAlbum()+"\n    4) Manually Change Individual File Metadata\n\n Any Other Key to Go Back: ")
                try:
                    num = int(userInput2)
                    if 1 <= num <= 4:
                        if num == 1:
                            self.initFiles(None)
                        if num == 2:
                            self.setArtist()
                        if num == 3:
                            self.setAlbum()
                        if num == 4:
                            self.changeMetadata()
                    pass
                except:
                    print("Invalid Input")
            #6. save the metadata to the files
            elif userInput == '6':
                userInput3 = input("Are you sure you want to write to these files? All of your files metadata will be overwritten. Y/N: ")
                if userInput3.lower() == 'y':
                    self.saveMetadata()
                    done = True
            #7. 
            elif userInput == '7':
                done = True
            else:
                print("Invalid Input. Please try again.")
    
    def sortByDate(self):
        newfiles = []
        os.chdir(self.filepath)
        files = filter(os.path.isfile, os.listdir(self.filepath))
        files = [os.path.join(self.filepath, f) for f in files]
        files.sort(key=lambda x: os.path.getctime(x))
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
        try:
            self.files.sort(key=lambda x: x.getTrackNum())
        except:
            print("Cannot Sort. Files do not contain TrackNums.")
    
    def sortByList(self):
        for i in range(len(self.files)):
            self.files[i].setTrackNum(i+1)
    
    def orderTracks(self):
        self.printFiles()
        userInput = input("\nWARNING: 1-2 Add Track #'s based on the finished sorted list.\n 1. Order by date downloaded\n 2. Order alphabetically\n 3. Order by track # (least to greatest)\n 4. Add Track Num by List order (current list)\n 5. Swap Tracks\nPlease Enter 1-5 (or anything else to go back): ")
        if userInput == '1':
            self.sortByDate()
            print("Done.")
        elif userInput == '2':
            self.sortAlphabetically()
            print("Done.")
        elif userInput == '3':
            self.sortByTrackNum()
            print("Done.")
        elif userInput == '4':
            self.sortByList()
            print("Done.")
        elif userInput == '5':
            self.swapTracks()
            
    def printFiles(self):
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
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
            substring = input("\nWhat substring would you like to remove from ALL tracks?\n(You may enter nothing ('') to go back, or enter '1234' to remove ascending numbers): ")
            if substring == '':
                done = True
                break
            elif substring == '1234':
                self.removeOrderedNum()
                done = True
                break
            userInput = input(substring + " is the string you want to be removed? Y/N: ")
            if userInput.lower() == 'y':
                for i in range(len(self.files)):
                    self.files[i].editTitle(substring)

    def removeOrderedNum(self):
        self.printFiles()
        userInput = input("\nYour files contain ascending numbers starting from what number? Enter nothing if you'd like to go back: ")
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
            choice = "\nEnter the song # you would like to remove a substring from\nOr enter nothing if you would like to exit and go back: "
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
            choice = "\nEnter the song # you would like to rename\nOr enter nothing if you would like to exit and go back: "
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
            choice = "WARNING: This will NOT swap Track Numbers \n(you may order tracks by list to sort track #'s back in order)\nWhat file would you like to select? (enter nothing to go back): "
            userInput = self.fileSelect(choice)
            if userInput == '':
                done = True
                break
            else:
                idxsel = int(userInput) - 1
                tempfileselected = self.files[idxsel]
            choice2 = "File Selected: "+tempfileselected.getTitle()+ "\nWhat is the other file you would like to select?: "
            userInput2 = self.fileSelect(choice2)
            if userInput2 == '':
                done = True
                break
            else:
                idxmove = int(userInput2) - 1
                tempfilemoveto = self.files[idxmove]
                done = True
            self.files[idxsel] = tempfilemoveto
            self.files[idxmove] = tempfileselected

    def changeMetadata(self):
        #manually change metadata of files
        done = False
        cont = False
        while not done:
            cont = False
            choice = "\nEnter a # for one of the songs above, or enter nothing to go back: "
            userInput = self.fileSelect(choice)
            if userInput == '':
                done = True
                break
            cont = True
            num = int(userInput)
            idx = num-1
            while cont == True:
                #now to prompt the user with choice of how to edit the metadata
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n      Title: "+self.files[idx].getTitle()+"\n      Artist: "+self.files[idx].getArtist()+"\n      Album: "+self.files[idx].getAlbum()+"\n      Track #: "+str(self.files[idx].getTrackNum()))
                userInput = input("\n1. Change Title\n2. Change Artist Name\n3. Change Album Name\n4. Change Track #\n5. Delete Track\n Any Other Key to Go Back: ")
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
                elif userInput == '5':
                    choice2 = "Are you sure you want to delete this track?\n This cannot be undone unless the folder is initialized again Y/N: "
                    userInput = getInput(choice2)
                    if userInput == 'y':
                        self.files.pop(idx)
                        cont = False
                        break
    
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