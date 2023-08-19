MP3 RENAMER README by Soopyman

Hello and Thank you for using my program!

You will need to install/have some python packages first using pip.
How to install pip may be found here: https://pip.pypa.io/en/stable/installation/

pip install packagename (or pip3 install)
PACKAGES:
os - to access files
eyed3 - to access metadata
yt_dlp - to download songs
pytube - to get playlist links

FFMPEG: https://ffmpeg.org/download.html
If you have GIT:
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg

If you don't have ffmpeg then, then install it inside of the MP3NAMER folder.
If you do have it, but you don't have it in the MP3NAMER folder, then you will need to manually change its location using the instructions below:
Inside of "mp3namer yt-dlp mp3.py", line 49 is where the ffmpeg location is. It must be set to the ffmpeg.exe path. 
Where it is routed from the directory of the folder to where the ffmpeg.exe file would be.
(It may be hard to find the ffmpeg default location. If so, just install it again into the MP3NAMER folder using the website above.)

USAGE:
This is a program used to download YT to MP3 files quickly, and be able to access and change metadata with a relatively simple interface.
The UI may be updated in the future instead of it being python (LOL)
I take no responsibility in any of the rights for the music any of you download. If anyone takes responsibility, it's YT-DLP.
I do take responsbility for owning this program and being the one to code/create it.

If you have any questions, feel free to post on the forum for this repository.