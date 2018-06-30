# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:41:42 2018

@author: Ivica
"""
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import sys
import threading
import time
import youtube_api
class LinkParser(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for(key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    
                    self.links = self.links + [newUrl]
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response  = urlopen(url)
        
        if response.getheader('Content-Type').startswith('text/html'):
            htmlBytes = response.read()
            htmlString  = htmlBytes.decode("utf-8")
            
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]
class YTCommentCheck(threading.Thread):
    def __init__(self,URL,word,binarySemaphore):
        self.binarySemaphore = binarySemaphore
        self.url = URL
        self.word = word
        threading.Thread.__init__(self)
    def run(self):
        ytApi = youtube_api.YouTubeApi()
        ytApi.get_video_comments(self.url)
        comments = ytApi.comments
        replies = ytApi.replies
        
        for i in comments:
            if i[0].find(self.word)>-1 or i[1].find(self.word)>-1:
                self.binarySemaphore.acquire()
                print("YT: The word", self.word, "was found at", self.url," Autor:",i[0]," Comment:",i[1])
                self.binarySemaphore.release()
        for i in replies:
            if i[2].find(self.word)>-1 or i[3].find(self.word)>-1:
                self.binarySemaphore.acquire()
                print("YT: The word", self.word, "was found at", self.url," Reply autor:",i[2]," Reply comment:",i[3])
                self.binarySemaphore.release()
class CrawlerThread(threading.Thread):     
    base_video_url_ssh = 'https://www.youtube.com/watch?v='
    base_video_url = 'http://www.youtube.com/watch?v='
    def __init__(self, binarySemaphore,url,word):
         self.binarySemaphore = binarySemaphore
         self.url = url
         self.word = word
         
         threading.Thread.__init__(self)
    def run(self):
            ytThreads = []
            print("Thread started!")
            pagesToVisit = [self.url]
            numberVisited = 0
            
            while pagesToVisit != [] and not run_event.is_set():
            
                numberVisited = numberVisited + 1
                url = pagesToVisit[0]
                pagesToVisit = pagesToVisit[1:]
                try:
            
                    parser = LinkParser()
                    print(url)
                    data, links = parser.getLinks(url)
                    if(url.startswith(self.base_video_url) or url.startswith(self.base_video_url_ssh)):
                        ytThread = YTCommentCheck(url,self.word,self.binarySemaphore)   
                        ytThread.start()
                        ytThreads.append(ytThread)
                    elif data.find(self.word)>-1:
                        self.binarySemaphore.acquire()
                        print("The word", self.word, "was found at", url)
            
                    #print(set(pagesToVisit + links))
                    pagesToVisit = list(set(pagesToVisit + links))
                    print("Success!")
                    self.binarySemaphore.release()
            
                except Exception as e:
                        print ("Exception: "+ str(e))
            for i in ytThreads:
                i.join()
                
run_event = threading.Event()

binarySemaphore = threading.Semaphore(1)    
#ytThread = YTCommentCheck("https://www.youtube.com/watch?v=tQ6PRUgtCuM","amazed",binarySemaphore)   
#ytThread.start()
#ytThread.join() 
thread1 = CrawlerThread(binarySemaphore,"https://www.youtube.com/watch?v=8xpbuSZGA4c","only")
thread2 = CrawlerThread(binarySemaphore,"http://www.facebook.com","bank")
thread1.start()
thread2.start()

try:
    while (1):
        time.sleep(1)
except KeyboardInterrupt:
    run_event.set()
    thread1.join()
    thread2.join()
    print("Stoping threads!")
    
