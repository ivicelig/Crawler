import json

from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen


YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'



class YouTubeApi():
    comments = []
    replies = []
    def get_video_comments(self, videoURL):
        
       
        #Fill comments and replies arrays with data from API json response
        def load_comments(self):
            for item in mat["items"]:
                comment = item["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                #Save values in comment array
                self.comments = self.comments + [[author,text]]
            
                
                if 'replies' in item.keys():
                    for reply in item['replies']['comments']:
                        rauthor = reply['snippet']['authorDisplayName']
                        
                        rtext = reply["snippet"]["textDisplay"]
                        #Save values in replies array
                        self.replies = self.replies + [[comment,author,rauthor,rtext]]
                    

        
        #Check validity of URL
        try:
            video_id = urlparse(videoURL)
            q = parse_qs(video_id.query)
            vid = q["v"][0]

        except:
            print("Invalid YouTube URL")
        #Set parameters for URL; e.g. https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyDebkmzGWsRarwqzTQNOqbZ2Mbcprk_wE8&textFormat=plainText&part=snippet&videoId=kffacxfA7G4&maxResults=50 
        parms = {
                    'part': 'snippet,replies',
                    'videoId': vid,
                    'maxResults' : 100,
                    'textFormat': 'plainText',
                    'key': 'AIzaSyDebkmzGWsRarwqzTQNOqbZ2Mbcprk_wE8'
                }

        try:
            #Test if there is next page in comment section and get nextPageToken; call load_comments first time
            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            load_comments(self)
            
            #While there is another page in comment section, parse JSON object in array and 
            #call load_comments function which fills comment and replies arrays with values
            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")            
                load_comments(self)
                
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except Exception as e:
            print("YT Exception: ",e) 
    #Open URL and get raw data from web service in JSON type
    def openURL(self, url, parms):
        f = urlopen(url + '?' + urlencode(parms))
        data = f.read()
        f.close()
        matches = data.decode("utf-8")
        return matches


