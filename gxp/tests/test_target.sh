#!/bin/bash

MOCK_DIR="$( cd "$(dirname "$0")" ; pwd -P )/mock/"
# BYPRODUCT_DIR="$( cd "$(dirname "$0")" ; pwd -P )/../byproduct/"
BYPRODUCT_DIR="/tmp/gxp_byproduct/"
EXPECTED_DIR="$( cd "$(dirname "$0")" ; pwd -P )/expected/"
RUN_FILE="$( cd "$(dirname "$0")" ; pwd -P )/../xml_to_header.py"
TARGET=
IS_CLEAN=false
OUTPUT_DIR_CREATED=false

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    
    -o|--output)
    BYPRODUCT_DIR="$2"
    shift # past argument
    shift # past value
    ;;
    -s|--searchpath)
    SEARCHPATH="$2"
    shift # past argument
    shift # past value
    ;;
    -c|--clean)
    IS_CLEAN=true
    shift # past argument
    shift # past value
    ;;
    *)
    if [ -z $TARGET ]; then TARGET=$1; fi
    shift
    ;;
esac
done


if [ -z $TARGET ]; then
    echo "Positional argument 1 not set! Its a Target dir name of the mock/ folder to run test for."
    exit 1
fi

if [[ $BYPRODUCT_DIR == /tmp/* ]]; then
    if [ ! -d "$BYPRODUCT_DIR" ]; then
        OUTPUT_DIR_CREATED=true
        mkdir -p $BYPRODUCT_DIR
        echo 'Output dir created at: %BYPRODUCT_DIR'
    fi
else
    echo "Output dir at $BYPRODUCT_DIR is not in /tmp/*!"
    exit 1
fi


if [ ! -d "$MOCK_DIR/$TARGET" ]; then
    echo "Mock dir for test target at $MOCK_DIR/$TARGET not found!"
    exit 1
fi

echo_error() { printf "\n%s\n" "$*" 1>&2; }

diff_target() {
    expected=$1
    received=$2
    if [ -f "$expected" ]; then
        h_diff=`diff -bB -I "$ignore_in_diff" $expected $received`
        if [ ! -z "$h_diff" ]; then
            echo_error "-- Mismatch in $(basename $received)! --"
            echo_error "$h_diff"
            return 1
        else
            echo ''
            echo "-- Success for $(basename $received)! --"
            return 0
        fi
    else
        echo "-- ERROR -- No expected file found at: $expected"
        return 1
    fi

    return 0
}


# target_names=(pointer_array_table pointer_array pointer_generic pointer_struct pointer_table_header pointer_table)
target_names=$(find $MOCK_DIR/$TARGET/ -name '*.xml')
failed_targets=()

for mock_file in ${target_names[*]}; do
    file_name=$(basename $mock_file)
    file_name=${file_name%".xml"} #remove .xml from mockfile
    expected_file=$EXPECTED_DIR/$TARGET/$file_name

    if [ -f "$name" ]; then
        echo "Mock file at $mock_file does not exist?!"
        continue
    fi

    $RUN_FILE $mock_file -o $BYPRODUCT_DIR/$file_name.h -v 20
    ignore_in_diff=".Generated On."

    diff_target $expected_file.h $BYPRODUCT_DIR/$file_name.h
    has_failed=$?
    echo "--> $has_failed"
    if [ has_failed = -1 ]; then failed_targets += "$file_name.h"; fi

    diff_target $expected_file.c $BYPRODUCT_DIR/$file_name.c
    has_failed=$?
    echo "--> $has_failed"
    if [ has_failed = -1 ]; then failed_targets += "$file_name.c"; fi

    printf "\n*** END OF TEST ****\n\n"
done


for failed in ${failed_targets[*]}; do
    echo " -- Failed: $failed"
done


if [ "$IS_CLEAN" = true ]; then
    if [ "$OUTPUT_DIR_CREATED" = false ]; then exit 0; fi #byproduct dir was already there when ran the test. Do nothing.

    if [[ $BYPRODUCT_DIR == /tmp/* ]]; then
        echo "--- Cleaning up $BYPRODUCT_DIR ---"
        rm -r $BYPRODUCT_DIR
    else
        echo "Trying to remove byproduct at '$BYPRODUCT_DIR' which is not in '/tmp/'?"
    fi
fi