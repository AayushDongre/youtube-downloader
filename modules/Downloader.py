import youtube_dl
import eyed3
import os

class Downloader:
    def __init__(self, url:str):

        self.errors = []
        self.url = url
        self.info = {}

        self.ydlOptions = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            # "outtmpl": f"""songs/{directory}/{'%(title)s'.replace('/','_').replace('|','_').replace("'",'_')}.%(ext)s""",
            "outtmpl": f"""songs/{'%(title)s'.replace('/','_').replace('|','_').replace("'",'"')}.%(ext)s""",
            "writethumbnail": True,
            "quiet": True,
            "playliststart": 1,
            "ignoreerrors": True
        }
        self.downloader = youtube_dl.YoutubeDL(self.ydlOptions)




    def downloadSingle(self):
        
        print("Collecting metadata...")
        self.info = self.downloader.extract_info(self.url, download=False)

        try:
            os.mkdir("songs")
        except FileExistsError:
            pass

        try:
            self.downloader.download([ self.url ])
            self.thumbnailAttacher(self.info["title"].replace("*","").replace(":"," -").replace('/','_').replace('|','_').replace('"',"'"))
        except Exception as e:
            print(e)
            
            
        print("Downloaded!")
        return self.info["title"].replace('/','_').replace("*","").replace('/','_').replace('|','_').replace('"',"'").replace(':'," -")




    def downloadPlaylist(self):
        i=1
        titleList = []

        print("Collecting metadata...")
        self.info = self.downloader.extract_info(self.url, download=False)
        
        i = 1
        for vid in self.info["entries"]:
            
            if type(vid) != type(None):
                try:
                    if type(vid["title"]) == type(None):
                        vid["title"] = str(i)
                    title = vid["title"].replace("*","").replace(":"," -").replace('/','_').replace('|','_').replace('"',"'")
                    print("Downloading ",vid["title"])
                    vidUrl = "https://www.youtube.com/watch?v="+vid["webpage_url_basename"]
                    
                    self.downloader.download([vidUrl])
                    titleList.append(title)
                    
                    self.thumbnailAttacher(title)
                except Exception as e:
                    self.errors.append(vid["title"])
                    print(e)
            i = i+1
        titleList.append(self.info["title"].replace("*","").replace(":"," -").replace('/','_').replace('|','_').replace('"',"'"))

        return titleList




    def thumbnailAttacher(self, title):

        print("Attaching ",title)
        audiofile = eyed3.load(os.path.join("songs", title.replace("/","_").replace('|','_').replace('"',"'"))+".mp3")
        
        if (audiofile.tag == None):
            audiofile.initTag()
        
        audiofile.tag.images.set(3, open(os.path.join("songs", title.replace("/","_").replace('|','_').replace('"',"'"))+".jpg",'rb').read(), 'image/jpeg')
        audiofile.tag.save()
        os.remove(f"""songs/{title.replace('/','_').replace('|','_').replace('"',"'")}.jpg""")

