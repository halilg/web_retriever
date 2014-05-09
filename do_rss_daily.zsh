#!/usr/bin/env zsh
BASEDIR=/home/halil/work/web_retriever
echo `date` $0 starting

cd $BASEDIR
./retrieve.zsh
./make_all_html.zsh