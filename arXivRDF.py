#!/usr/bin/env python2.6
import os, sys

from HTMLParser import HTMLParser
class hrefParser(HTMLParser):
    url=""
    text=""
    
    def get_data(self):
        return (self.text, self.url)
    
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
                   self.url=value
                   
    def handle_data(self, data):
        self.text=data
        

"""
This class receives an arXiv.org RSS feed as text. The feed is expected to be in XML/RDF format.
Class produces a python object which contains the available data in the feed.

Data structure of the RDF object:
data is in rdf (dict) object, which has the following keys:
   title: Name of the feed (eg hep-ph)
    date: rdf publish date
  papers: List of paper objects in current feed

paper (dict) objects have the following keys:
          id: Unique arXiv.org preprint identifier (eg. 1311.2453v2)
       title: Title of the paper
     creator: List of author objects
        link: URL of the paper on arXiv.org
 description: Abstract of the paper

author (dict) objects have author names as keys and an URL as value.
The URL link points to the page on arXiv.org listing the author's all papers.
"""
import re, xml.etree.ElementTree as ET
class arXivRDF:
    version="0.8"
    rdf={"title":"", "date":"", "papers":[]}
    verbose=0
    NS=[ "#}",
     "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
     "http://purl.org/rss/1.0/",
     "http://purl.org/rss/1.0/modules/content/",
     "http://purl.org/rss/1.0/modules/taxonomy/",
     "http://purl.org/dc/elements/1.1/",
     "http://purl.org/rss/1.0/modules/syndication/",
     "http://webns.net/mvcb/",
    ]
    
    
    def removeNS0(self, txt):
        return txt.split("}")[1]
    

    def printPaper(self, paper):
        print "\n----"
        print "("+paper["id"]+") Title:", '"'+paper["title"]+'"', "("+paper["link"]+")"
        #print "Authors:\n", "\n".join(paper["creator"])
        
        print "\nAuthor(s):",", ".join(paper["creator"].keys())
        print "\nDescription:", paper["description"].replace("<p>","").replace("</p>",""),"\n"


    def go(self, rdfdata):
    
        items=[]
        root = ET.fromstring(rdfdata)
        NOPAR=re.compile(r'\(.*?\)')
        #loop over the elements at the root of rdf file
        for element in root:
            rtag=self.removeNS0(element.tag)
            
            # papers
            if rtag=="item":
                items.append(element)
                
            # global metadata
            elif rtag=="channel":
                for element1 in element:
                    rtag=self.removeNS0(element1.tag)
                    if rtag=="title":
                        self.rdf["title"]=element1.text.split(" ")[0].strip()
                    elif rtag=="date":
                        self.rdf["date"]=element1.text.strip()
            else:
                pass #if (self.verbose): print rtag
    
        if (self.verbose): print "Date:",self.rdf["date"],", feed:", self.rdf["title"]
        # analyze papers data
        parser = hrefParser() # to extract url from author text
        for item in items:
            paper={}
            #printXMLTree(paper)
            for meta in item:
                tag=self.removeNS0(meta.tag)
                if tag=="creator":
                    paper[tag]=NOPAR.sub('', meta.text) # remove all text in paranthesis
                    paper[tag]=paper[tag].replace("</a> ,","</a>,").split("</a>,")
                    authors={}
                    for author in paper["creator"]:
                        author=author.strip()
                        parser.feed(author)
                        a, url=parser.get_data()
                        a=author.replace("</a>","")
                        a=a.split(">")[-1]
                        authors[a]=url
                    paper["creator"]=authors
                elif tag=="title":
                    temp=meta.text.split("(arXiv:")
                    
                    paper["title"]=temp[0].strip()
                    paper["id"]=temp[1].split(" ")[0].strip()
                else:
                    paper[tag]=meta.text
            
            # one final touch
            paper["description"]=paper["description"].replace("<p>","").replace("</p>","").replace("\n"," ").replace("\r"," ").replace("  "," ")
            
            # we're done with this paper. pack the data to global papers list
            self.rdf["papers"].append(paper)
            
            # optionally print the paper data to terminal
            #if (self.verbose): self.printPaper(paper)
        
        # Number of papers we found:    
        if (self.verbose): print "Papers in file:",len (items)

if __name__ == '__main__':
#    files=os.listdir(rssdir)
    rssfile="test1.rss"
    f=file(rssfile)
    rdf=f.read()
    a2j=arXivRDF()
    a2j.verbose=0
    a2j.go(rdf)
