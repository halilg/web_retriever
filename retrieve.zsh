#!/usr/bin/env zsh

BASEDIR=/home/halil/work/web_retriever
LOGFILE=/dev/tty #/home/httpd/html/halil/logs/retriever.log
URLs=$BASEDIR/URLs.lst
RETDIR=$BASEDIR/retrieved

function wgets()
{
  local H='--header'
  /usr/bin/wget $H='Accept-Language: en-us,en;q=0.5' $H='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' $H='Connection: keep-alive' -U 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2' "$@";
}

touch $LOGFILE
echo `date` "Starting retriever" #>> $LOGFILE
NOW=$(date +"%Y-%m-%d")
cd $BASEDIR

for URLFile in *.ret; do
	echo `date` processing $URLFile #>> $LOGFILE
	OFILE=`echo $URLFile | cut -f1 -d'.'`
	OFILE="$RETDIR/${OFILE}_$NOW.rss"
	LOOP=0
	URL=`cat $URLFile`
	while [ $LOOP -eq 0 ]; do
	    rm -f $OFILE ${OFILE}.gz
	    wgets -q --output-document=$OFILE $URL #>> $LOGFILE 2>&1
	    echo `date` "wget exit code:" $? #>> $LOGFILE
	    if [ -s $OFILE ]; then #is it a regular file (size > 0)?
	      echo `date` File is good  #>> $LOGFILE
	      LOOP=1
	    else
	      echo file is not regular, will retry in 5 minutes  #>> $LOGFILE
	      sleep 300
	    fi
	done
	gzip $OFILE
	touch ${OFILE}.gz
	echo `date` done #>> $LOGFILE
done
