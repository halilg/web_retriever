#!/usr/bin/env zsh

for dir in $(ls ./arXiv); do
	echo $dir
	rm arXiv/$dir/*.html 
done 
