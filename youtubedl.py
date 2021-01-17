import pytube
import subprocess
import os
from youtube_search import YoutubeSearch
import eyed3
import requests
links=YoutubeSearch(input("Enter the name of the song you want to download\n"),max_results=1).to_dict()
final_url="https://www.youtube.com"+links[0]["url_suffix"]
parent_dir=r"C:\Users\Owner\PycharmProjects\Codechef"
yt=pytube.YouTube(final_url)
print("Title: ",yt.title)
ys=yt.streams.filter(only_audio=True)
ys[0].download()
new_filename = yt.title+".mp3"
mp4=os.listdir(parent_dir)
default_filename=ys[0].default_filename
subprocess.run([
    'ffmpeg',
    '-i', os.path.join(parent_dir, default_filename),
    os.path.join(parent_dir, new_filename)
])
for item in mp4:
    if item.endswith(".mp4"):
        os.remove(os.path.join(parent_dir, item))
audiofile=eyed3.load(new_filename)
audiofile.tag.album_artist=links[0]['channel']
audiofile.tag.title=yt.title
res=requests.get(links[0]["thumbnails"][0])
audiofile.tag.images.set(3, res.content , "" ,u"")
audiofile.tag.save()