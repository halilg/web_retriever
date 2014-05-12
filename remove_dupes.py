#!/usr/bin/env python

# simple script to remove duplicate rss files
# Duplicates exist because arxiv RSS feed is the friday's feed on weekends, whench I keep retrieving (just in case)

import os, sys, gzip
def readfile(ifile):
    try:
        if ifile[-3:]==".gz": #gzip file
            f = gzip.open(ifile, 'rb')
        else: #regular file        
            f=file(ifile)
    except IOError:
        print "No such file or directory: ",ifile
        return None
    return f.read()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage:", os.path.basename(sys.argv[0]),"<directory>"
        sys.exit()
    
    rssdir=sys.argv[1]
    remove=[]
    files=sorted(os.listdir(rssdir))
    files=files[::-1]
    print "found",len(files),"files in directory:",'"'+rssdir+'"'
    for i in range(len(files)-1):
        rss1=readfile(os.path.join(rssdir,files[i]))
        rss2=readfile(os.path.join(rssdir,files[i+1])) 
        identical = rss1 == rss2 
        if identical:
            remove.append(files[i])
    
    nremove=len(remove)
    if nremove == 0:
        print "nothing to do"
        sys.exit()
    elif nremove > 1: print len(remove),"files will be removed"
   
    for dupe in remove:
        fpath=os.path.join(rssdir,dupe)
        os.remove(fpath)
        print "deleted",fpath
    
