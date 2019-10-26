import tornado
import tornado.web
from tornado import gen
from modules.Downloader import Downloader
import os
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor

class DownloadManeger(tornado.web.RequestHandler):
        
    @gen.coroutine
    def get(self):
        executer = ThreadPoolExecutor(max_workers=10)
        url = self.get_query_argument("url", "")
        
        if "youtube" not in url or not url:
            self.finish()
            return
        

        playlist = True if "playlist" in url else False
        

        if not playlist:
            title = yield executer.submit(Downloader(url).downloadSingle)
            yield self.sendData(title, playlist)            
        else:
            titleList = yield executer.submit(Downloader(url).downloadPlaylist)

            with ZipFile(os.path.join("songs", f"""{str(titleList[-1])}.zip"""), "w") as zip:
                for title in titleList[:-1]:
                    yield zip.write(os.path.join("songs", title + ".mp3"))
            yield self.sendData(str(titleList[-1]), playlist)


    def sendData(self, title, playlist):
        extension = ".zip" if playlist else ".mp3"
        self.set_header('Content-Type', 'audio/wav')
        self.set_header('Content-Disposition', f'''attachment; filename={''.join([i if ord(i) < 128 else ' ' for i in title])+extension}''')
        self.flush()

        audioByteArray = bytearray(os.path.getsize(os.path.join("songs", title+extension)))
        
        with open(os.path.join("songs", title+extension), "rb") as f:
            f.readinto(audioByteArray)
            print("writing " + title)
            self.write(bytes(audioByteArray))

            self.flush()
        print("flushed " + title)
