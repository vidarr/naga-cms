#!/bin/bash 

ETC_DIR=etc
DUMMY_CFG_FILES=categories static
NO_OPERATIONAL=test TODO

function remove_non_operational () {
    for NON_OPS in $NON_OPERATIONAL_ITEMS; do
        rm -rf $NON_OPS
    done
}

function create_dummy_cfg_files () {
    for CFG_FILE in $DUMMY_CFG_FILES; do
        touch $CFG_FILE
        echo "Created $CFG_FILE - remember to fill it !"
    done
}




remove_non_operational ()
create_dummy_cfg_files ()

echo "Remember to set in python/naga_config.py:"
echo "   NAGA_ROOT"
echo "   COPYRIGHT"



