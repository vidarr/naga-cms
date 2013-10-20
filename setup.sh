#!/bin/bash 

source ./setup.cfg

ETC_DIR=etc
DIRECTORIES_TO_CREATE="log content"
DUMMY_CFG_FILES="categories static"
NON_OPERATIONAL="test TODO"
FILES_TO_SET_WRITABLE="log content"
FILES_TO_SET_ROOT_ONLY="tools"

function ensure_cfg_params_set () {
    if [ -z $APACHE_USER -o -z $APACHE_GROUP ]; then
        echo "Please open ./setup.cfg and activate APACHE_USER and APACHE_CONFIG
        with appropriate values"
        exit
    fi
}

function remove_non_operational () {
    for NON_OPS in $NON_OPERATIONAL_ITEMS; do
        rm -rf $NON_OPS
    done
}

function create_dummy_cfg_files () {
    [ ! -d $ETC_DIR ] && mkdir $ETC_DIR
    for CFG_FILE in $DUMMY_CFG_FILES; do
        touch $ETC_DIR/$CFG_FILE
        echo "Created $CFG_FILE - remember to fill it !"
    done
}

function create_directories () {
    for DIRECTORY in $DIRECTORIES_TO_CREATE; do
        [ ! -d $DIRECTOY ] && mkdir $DIRECTORY;
    done
}

function set_permissions () {
    chown $APACHE_USER:$APACHE_GROUP * -R
    chmod 500 * -R
    for FILE in $FILES_TO_SET_WRITABLE; do
        chmod 700  $FILE
    done
    for FILE in $FILES_TO_SET_ROOT_ONLY; do
        chown root $FILE
        chmod 700  $FILE
    done
}



ensure_cfg_params_set
remove_non_operational
create_dummy_cfg_files
create_directories
set_permissions

echo "Remember to set in python/naga_config.py:"
echo "   NAGA_ROOT"
echo "   NAGA_ABS_ROOT"
echo "   COPYRIGHT"

