#!/bin/bash
ARCHIVE_PREFIX=naga
ARCHIVE_SUFFIX=tar.gz
DESTINATION=$1
RELEASE_NO_FILE=release-no

if [ -z $DESTINATION ]; then
    echo " Usage: "
    echo "    $0 DESTINATION"
    echo 
    echo " DESTINATION must be some destination specification that rsync understands"
    exit $STATUS_FAILURE
fi

function get_new_release_no () {
    if [ ! -f $RELEASE_NO_FILE ]; then
        RELEASE_NO=0
        touch $RELEASE_NO_FILE
        git add $RELEASE_NO_FILE
    else
        RELEASE_NO=$(cat $RELEASE_NO_FILE)
    fi
    RELEASE_NO=$(expr $RELEASE_NO + 1)
    echo "Release number is $RELEASE_NO"
    echo $RELEASE_NO > $RELEASE_NO_FILE
}

get_new_release_no
ARCHIVE_FILE="${ARCHIVE_PREFIX}-release${RELEASE_NO}.${ARCHIVE_SUFFIX}"
GIT_TAG="release-$RELEASE_NO"
git commit $RELEASE_NO_FILE -m "RELEASE $RELEASE_NO"
git tag $GIT_TAG
git archive $GIT_TAG --format=${ARCHIVE_SUFFIX} -o $ARCHIVE_FILE
rsync -azv $ARCHIVE_FILE $DESTINATION

