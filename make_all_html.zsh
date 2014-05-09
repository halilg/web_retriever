#!/usr/bin/env zsh

RSSDIR=/home/halil/html/halil/RSS
HTMLDIR=/home/halil/html/halil/arXiv

for xml in $RSSDIR/*; do
    htmlfile=$HTMLDIR/`basename $xml`.html
    if [ -s $htmlfile ]; then
        #echo "skipping" $htmlfile
    else
        ./arXivHTML.py $xml $htmlfile
    fi
done
