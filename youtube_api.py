import json

from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen


YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'



class YouTubeApi():
    comments = []
    replies = []
    def get_video_comments(self, videoURL):
        
       
            
        def load_comments(self):
            for item in mat["items"]:
                comment = item["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                self.comments = self.comments + [[author,text]]
            
                #print("Comment by {}: {}".format(author, text))
                if 'replies' in item.keys():
                    for reply in item['replies']['comments']:
                        rauthor = reply['snippet']['authorDisplayName']
                        
                        rtext = reply["snippet"]["textDisplay"]
                        self.replies = self.replies + [[comment,author,rauthor,rtext]]
                    

        

        try:
            video_id = urlparse(videoURL)
            q = parse_qs(video_id.query)
            vid = q["v"][0]

        except:
            print("Invalid YouTube URL")

        parms = {
                    'part': 'snippet,replies',
                    'videoId': vid,
                    'maxResults' : 100,
                    'textFormat': 'plainText',
                    'key': 'AIzaSyDebkmzGWsRarwqzTQNOqbZ2Mbcprk_wE8'
                }

        try:

            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            
            load_comments(self)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")            
                load_comments(self)

        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except Exception as e:
            print("Exception: ",e) 
    def openURL(self, url, parms):
        f = urlopen(url + '?' + urlencode(parms))
        data = f.read()
        f.close()
        matches = data.decode("utf-8")
        return matches


