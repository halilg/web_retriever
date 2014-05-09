#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import os, sys
from arXivRDF import arXivRDF


# mathjax information
# http://docs.mathjax.org/en/latest/start.html

class arXivHTML:
    # http://cssfontstack.com
    # http://copypastecharacter.com/arrows
    version="0.8"
    gtemplate="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<html>
<head>
<title>arXiv Updates ($FEED): $DATE</title>
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
<script type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
</head>
<body>
<script language="JavaScript">
<!-- 
function hide(which) {
var hide = new Array();
hide = document.getElementsByName(which);
for (i=0; i<hide.length; i++) {
  if (hide[i].style.display == 'none'){
     hide[i].style.display = 'inline';}
  else{
      hide[i].style.display = 'none';};
}
}
-->
</script>
<div style="color:#FF4500"><h4>$DATE ($FEED)</h4></div>
<table width="800" class="bottomBorder">
$PAPERS
</table>
</body>
</html>
"""
    ptemplate="""
<TR onMouseOver="this.bgColor='#FAFAFA'" onMouseOut="this.bgColor='#FFFFFF'" bgColor=#FFFFFF>
<TD>
<div onclick="javascript:hide('$ID');">
    <h4>$TITLE <a href="$LINK" target="_blank">⍓</a></h4>
    $CREATOR<br/>
</div>
<div name="$ID" style = "display:none">
    <br/>$ABSTRACT
</div>
</TD>
</TR>
"""
    atemplate="<i>$AUTHOR</i>"
    
    def go(self, rdf):
        
        # fill in the global template
        HTML=self.gtemplate
        HTML=HTML.replace("$FEED", rdf["title"])
        HTML=HTML.replace("$DATETIME",rdf["date"])
        HTML=HTML.replace("$DATE",rdf["date"].split("T")[0])
        HTML=HTML.replace("$NPAPERS", str(len(rdf["papers"])))

        #the papers section
        papers="" 
        for preprint in rdf["papers"]:
            paper=self.ptemplate
            paper=paper.replace("$ID",preprint["id"])
            paper=paper.replace("$TITLE",preprint["title"])
            paper=paper.replace("$LINK",preprint["link"])
            paper=paper.replace("$ABSTRACT",preprint["description"])
            
            authors=[]
            for author in preprint["creator"].keys():
                tauthor=self.atemplate.replace("$AUTHOR",author)
                authors.append(tauthor)
            paper=paper.replace("$CREATOR", ", ".join(authors))
            
            papers=papers + paper
        
        HTML=HTML.replace("$PAPERS",papers)
        return HTML

import xml, gzip
if __name__ == '__main__':
#    files=os.listdir(rssdir)
    if len(sys.argv) < 2:
        print "usage: ", sys.argv[0],"<input file> [output file]"
        sys.exit()
    ifile=sys.argv[1]
    if "." in ifile:
        ofile=sys.argv[1].split(".").pop(0)+".html"
    else:
        ofile=ifile+".html"
    
    if len(sys.argv)>2:
        ofile=sys.argv[2]
    rssfile=ifile
    try:
        if ifile[-3:]==".gz": #gzip file
            f = gzip.open(ifile, 'rb')
        else: #regular file        
            f=file(rssfile)
    except IOError:
        print "No such file or directory: ",ifile
        sys.exit()

    rdf=f.read()
    f.close()
    r2p=arXivRDF()
    r2p.verbose=0
    try:
        r2p.go(rdf)
    except xml.parsers.expat.ExpatError:
        print "There was a problem reading file:",ifile,": File is not well-formed (invalid token)"
        sys.exit(1)
    rdfdata=r2p.rdf
    #print rdfdata.keys()
    htmlMaker=arXivHTML()
    html=htmlMaker.go(rdfdata)
    f=file(ofile,"w")
    f.write(html)
    f.close()
    print "wrote",ofile
