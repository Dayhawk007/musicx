import pytube
import subprocess
import os
from youtube_search import YoutubeSearch
import eyed3
import requests
from bs4 import BeautifulSoup
def downloader(name):
    links=YoutubeSearch(name,max_results=1).to_dict()
    final_url="https://www.youtube.com"+links[0]["url_suffix"]
    parent_dir=os.getcwd()
    yt=pytube.YouTube(final_url)
    print("Title: ",yt.title)
    ys=yt.streams.filter(only_audio=True)
    print(ys)
    ys[0].download()
    new_filename = yt.title+".mp3"
    mp4=os.listdir(parent_dir)
    default_filename=ys[0].default_filename
    try:
        subprocess.run([
            os.getcwd()+r"\ffmpeg",
            '-i', os.path.join(parent_dir, default_filename),
            os.path.join(parent_dir,new_filename)
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
    except:
        print("FFMPEG error")

def run(search_key):
    if(search_key[:5]=="https"):
        print(search_key.split("/"))
        songs_first_l=[]
        songs_last_l=[]
        songs_list=[]
        with requests.session() as r:
            res = r.get(search_key)
            soup = BeautifulSoup(res.text, features="html.parser")
            for song_first in soup.find_all('span', {'class': 'track-name'}):
                try:
                    songs_first_l.append(song_first.text.strip())
                except:
                    pass
            for song_last in soup.find_all('span',{'class':'artists-albums'}):
                try:
                    songs_last_l.append(song_last.text.strip())
                except:
                    pass
            for f,l in zip(songs_first_l,songs_last_l):
                songs_list.append(f+" "+l)
            for song in songs_list:
                downloader(song)


    else:
        downloader(search_key)
