#!/bin/bash 

ETC_DIR=etc
DIRECTORIES_TO_CREATE="log content"
DUMMY_CFG_FILES="categories static"
NON_OPERATIONAL="test TODO"

function remove_non_operational () {
    for NON_OPS in $NON_OPERATIONAL_ITEMS; do
        rm -rf $NON_OPS
    done
}

function create_dummy_cfg_files () {
    mkdir $ETC_DIR
    for CFG_FILE in $DUMMY_CFG_FILES; do
        touch $ETC_DIR/$CFG_FILE
        echo "Created $CFG_FILE - remember to fill it !"
    done
}

function create_directories () {
    for DIRECTORY in $DIRECTORIES_TO_CREATE; do
        mkdir $DIRECTORY;
    done
}



remove_non_operational
create_dummy_cfg_files
create_directories

echo "Remember to set in python/naga_config.py:"
echo "   NAGA_ROOT"
echo "   NAGA_ABS_ROOT"
echo "   COPYRIGHT"



