#!/usr/bin/env zsh

RSSDIR=./RSS
HTMLDIR=./arXiv
mkdir -p $HTMLDIR

for xml in $RSSDIR/*; do
    xmlname=$(basename $xml)
    feed=("${(s/_/)xmlname}")
    feed=$feed[1]
    targetdir=$HTMLDIR/$feed
    htmlfile=$targetdir/`basename $xml`.html
    htmlfile=`echo $htmlfile | sed s/.rss.gz//`
    if [ -s $htmlfile ]; then
        #echo "skipping" $htmlfile
    else
        mkdir -p $targetdir
        ./arXivHTML.py $xml $htmlfile
    fi
done
