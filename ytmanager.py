from __future__ import unicode_literals
from pickle import FALSE, TRUE
# import youtube_dl
import yt_dlp as youtube_dl
import json
from pathlib import Path
from custompp import CustomPP
class YtManager:
    def __init__(self,current_download_url):
        #load config
        path = Path(__file__).parent.absolute()
        configpath = '{}/config.json'.format(path)
        with open(configpath) as file:
            config = json.load(file)
        self.savepath =  config['savepath']

        #param
        self.current_download_url_id = ""
        self.current_download_url = current_download_url

    # 
    # get url basename from playlist
    # 
    def getUrlBasename(self,playlist_url):
        ydl = youtube_dl.YoutubeDL({
            'dump_single_json': True,
            'ignoreerrors': True,
            'extract_flat' : True,
            'flat-playlist':True
        })

        with ydl:
            result = ydl.extract_info(playlist_url,False)

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries']
            return video
        else:
            return false
    
    # 
    # download video as mp3
    # 
    def download(self):
        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)


        def my_hook(d):
            if d['status'] == 'finished':
                print('Done downloading, now converting ...')

            if d['status'] == 'downloading':
                print(d['filename'], d['_percent_str'], d['_eta_str'])


        ydl_opts = {
            'outtmpl': self.savepath+'%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'ignoreerrors': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.cache.remove()
                ydl.add_post_processor(CustomPP(None))
                ydl.download([self.current_download_url])
            except youtube_dl.DownloadError as error:
                raise Exception()
                # pass
