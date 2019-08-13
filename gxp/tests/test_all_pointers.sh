#!/bin/bash

MOCK_DIR="$( cd "$(dirname "$0")" ; pwd -P )/mock/"
# BYPRODUCT_DIR="$( cd "$(dirname "$0")" ; pwd -P )/../byproduct/"
BYPRODUCT_DIR="/tmp/gxp_byproduct/"
EXPECTED_DIR="$( cd "$(dirname "$0")" ; pwd -P )/expected/"
RUN_FILE="$( cd "$(dirname "$0")" ; pwd -P )/../xml_to_header.py"
TARGET=
IS_CLEAN=False

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
    IS_CLEAN=True
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
    exit -1
fi

if [[ $BYPRODUCT_DIR == /tmp/* ]]; then
    if [ ! -d "$BYPRODUCT_DIR" ]; then
        mkdir -p $BYPRODUCT_DIR
        echo 'Output dir created at: %BYPRODUCT_DIR'
    fi
else
    echo "Output dir at $BYPRODUCT_DIR is not in /tmp/*!"
    exit -1
fi


if [ ! -d "$MOCK_DIR/$TARGET" ]; then
    echo "Mock dir for test target at $MOCK_DIR/$TARGET not found!"
    exit -1
fi

echo_error() { printf "\n%s\n" "$*" 1>&2; }


# target_names=(pointer_array_table pointer_array pointer_generic pointer_struct pointer_table_header pointer_table)
target_names=$(find $MOCK/$TARGET/ -name '*.xml')

for mock_file in ${target_names[*]}; do
    file_name=$(basename $mock_file)
    file_name=$(file_name%".xml") #remove .xml from mockfile
    expected_file=$EXPECTED_DIR/$TARGET/$file_name

    if [ -f "$name" ]; then
        echo "Mock file at $mock_file does not exist?!"
        continue
    fi

    $RUN_FILE $mock_file -o $BYPRODUCT_DIR/$file_name.h -v 20
    ignore_in_diff=".Generated On."

    if [ -f "$expected.h" ]; then
        h_diff=`diff -bB -I "$ignore_in_diff" $EXPECTED_DIR/$file_name.h $BYPRODUCT_DIR/$file_name.h`
        if [ ! -z "$h_diff" ]; then
            echo_error "Mismatch in $file_name.h!"
            echo_error "$h_diff"
        else
            continue
            # echo "!!! SUCCESS for $name.h !!!"
        fi
    fi

    if [ -f "$expected.c" ]; then
        c_diff=`diff -bB -I "$ignore_in_diff" $expected.c $BYPRODUCT_DIR/$file_name.c`
        if [ ! -z "$c_diff" ]; then
            echo_error "Mismatch in $file_name.c!"
            echo_error "$c_diff"
        else
            continue
            # echo "!!! SUCCESS for $name.c !!!"
        fi
    fi

    printf "\n*** END OF TEST ****\n\n"
done

if [ IS_CLEAN == True ]; then
    if [[ $BYPRODUCT_DIR == /tmp/* ]]; then
        rm -r $BYPRODUCT_DIR
    else
        echo "Trying to remove byproduct at '$BYPRODUCT_DIR' which is not in '/tmp/'?"
    fi
fi