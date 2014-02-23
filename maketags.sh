#!/bin/bash
TAGS_FILE=ctags
DIRECTORIES='python cgi-bin'
[ -f $TAGS_FILE ] && rm $TAGS_FILE
for DIRECTORY in $DIRECTORIES; do
    for FILE in $(ls $DIRECTORY); do
        ctags $DIRECTORY/$FILE -a
    done
done 

