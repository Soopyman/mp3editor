# Title: Song Class
# Author: Soopyman https://github.com/Soopyman

#This is a class used to store the information about a song

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