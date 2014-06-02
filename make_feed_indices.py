#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import os, sys
from arXivRDF import arXivRDF


# http://cssfontstack.com
# http://copypastecharacter.com/arrows
version="0.8"
gtemplate="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<html>
<head>
<meta name="description" content="arXiv.org new abstracts feed cache ($FEED)">
<meta name="keywords" content="arxiv.org, $FEED, physics">
<meta name="author" content="Halil Gamsızkan, http://halilgamsizkan.home.anadolu.edu.tr">
<title>arXiv Updates ($FEED)</title>
<style type="text/css">
body {margin-left:50px;}
hr {color:sienna;}
p {margin-left:20px;}
body {font-family: font-family: Perpetua, Baskerville, "Big Caslon", "Palatino Linotype", Palatino, "URW Palladio L", "Nimbus Roman No9 L", serif;}
a:hover, a:visited, a:link, a:active {text-decoration: none;}
table.bottomBorder { border-collapse:collapse; }
table.bottomBorder td, table.bottomBorder th { border-bottom:1px dotted black;padding:5px; }
</style>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
  });
  
</script>
</head>
<body>
<div><h3>Feed: $FEED</h3></div>
<table width="800" class="bottomBorder">
<ul>
$HTMLFILES
</ul>
</table>
<br/><a href="../">&lt;&lt; Back to feeds index</a>
</body>
</html>
"""

atemplate='<li><a href="$HTMLFILE">$HTMLFILE</a></li><br/>'
    
def go(data):
    
    # fill in the global template
    feed=data["feed"]
    HTML=gtemplate
    HTML=HTML.replace("$FEED", feed)

    #the papers section
    feeds="" 
    for day in data["days"]:
        if feed not in day: continue # skip index.html and other irrelevant files (e.g. .DS_Store)
        daily=atemplate
        daily=daily.replace("$HTMLFILE",day)        
        feeds=feeds + daily
    
    HTML=HTML.replace("$HTMLFILES",feeds)
    return HTML

import xml, gzip
if __name__ == '__main__':
#    files=os.listdir(rssdir)
    if len(sys.argv) < 2:
        print "usage: ", sys.argv[0],"<directory>"
        sys.exit()
    idir=sys.argv[1]
    feed=os.path.basename(idir)
    ofile=os.path.join(idir,"index.html")
    data={}
    data["feed"]=feed
    data["days"]=sorted(os.listdir(idir))[::-1]
    html=go(data)
    f=file(ofile,"w")
    f.write(html)
    f.close()
    print "wrote",ofile
