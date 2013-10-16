#!/bin/bash 

ETC_DIR=etc
LOG_DIR=log
DUMMY_CFG_FILES="categories static"
NO_OPERATIONAL="test TODO"

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

function create_log_directory () {
    mkdir $LOG_DIR
}



remove_non_operational
create_dummy_cfg_files
create_log_directory

echo "Remember to set in python/naga_config.py:"
echo "   NAGA_ROOT"
echo "   COPYRIGHT"



