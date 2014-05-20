#!/usr/bin/env zsh
BASEDIR=/home/halil/work/web_retriever
echo `date` $0 starting

cd $BASEDIR
./retrieve.zsh
./remove_dupes.py retrieved
#./remove_dupes retrieved/hep-ph
#./remove_dupes retrieved/astro-ph
./make_all_html.zsh
#create html indices
./make_feed_indices.py arXiv/hep-ph
./make_feed_indices.py arXiv/hep-ex
./make_feed_indices.py arXiv/hep-th
./make_feed_indices.py arXiv/astro-ph
./make_feed_indices.py arXiv/gr-qc
