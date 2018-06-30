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
        
class CrawlerThread(threading.Thread):     
    def __init__(self, binarySemaphore,url,word,maxPages):
         self.binarySemaphore = binarySemaphore
         self.url = url
         self.word = word
         self.maxPages = maxPages
         threading.Thread.__init__(self)
    def run(self):
        print("Thread started!")
        pagesToVisit = [self.url]
        numberVisited = 0
    
        while numberVisited<self.maxPages and pagesToVisit != []:
            
            numberVisited = numberVisited + 1
            url = pagesToVisit[0]
            pagesToVisit = pagesToVisit[1:]
            try:
            
                parser = LinkParser()
                print(url)
                data, links = parser.getLinks(url)
                if data.find(self.word)>-1:
                    self.binarySemaphore.acquire()
                    print("The word", self.word, "was found at", url)
            
                pagesToVisit = pagesToVisit + links
                print("Success!")
                self.binarySemaphore.release()
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                    print ("Exception: "+ str(e))
                    
    
binarySemaphore = threading.Semaphore(1)            
thread1 = CrawlerThread(binarySemaphore,"http://www.bankofamerica.com","google",20)
thread2 = CrawlerThread(binarySemaphore,"http://www.bankofamerica.com","bank",20)
thread1.start()
thread2.start()
