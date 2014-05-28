#!/usr/bin/env zsh

# -R flag forces recreation of HTML files

RSSDIR=./RSS
HTMLDIR=./arXiv
mkdir -p $HTMLDIR
OPT=$1

for xml in $RSSDIR/*; do
    xmlname=$(basename $xml)
    feed=("${(s/_/)xmlname}")
    feed=$feed[1]
    targetdir=$HTMLDIR/$feed
    htmlfile=$targetdir/`basename $xml`.html
    htmlfile=`echo $htmlfile | sed s/.rss.gz//`
    if [[ -s $htmlfile && $OPT != -R ]]; then
        echo "skipping" $htmlfile
    else
        mkdir -p $targetdir
        ./arXivHTML.py $xml $htmlfile
    fi
done
