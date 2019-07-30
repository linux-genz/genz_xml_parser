#!/bin/bash

MOCK_DIR="$( cd "$(dirname "$0")" ; pwd -P )/mock/"
BYPRODUCT_DIR="$( cd "$(dirname "$0")" ; pwd -P )/../byproduct/"
EXPECTED_DIR="$( cd "$(dirname "$0")" ; pwd -P )/expected/"

if [ ! -d "$MOCK_DIR" ]; then
    echo "Mock dir at $MOCK_DIR not found!"
    exit -1
fi

if [ ! -d "$BYPRODUCT_DIR" ]; then
    echo "Byproduct dir at $BYPRODUCT_DIR not found!"
    exit -1
fi


echo_error() { printf "\n%s\n" "$*" 1>&2; }


target_names=(pointer_array_table pointer_array pointer_generic pointer_struct pointer_table_header pointer_table)
for name in ${target_names[*]}; do
    ./xml_to_header.py $MOCK_DIR/pointers/$name.xml -o $BYPRODUCT_DIR/$name.h -v 50
    ignore_in_diff=".Generated On."

    if [ -f "$EXPECTED_DIR/$name.h" ]; then
        h_diff=`diff -bB -I "$ignore_in_diff" $EXPECTED_DIR/$name.h $BYPRODUCT_DIR/$name.h`
        if [ ! -z "$h_diff" ]; then
            echo_error "Mismatch in $name.h!"
            echo_error "$h_diff"
        else
            continue
            # echo "!!! SUCCESS for $name.h !!!"
        fi
    fi

    if [ -f "$EXPECTED_DIR/$name.c" ]; then
        c_diff=`diff -bB -I "$ignore_in_diff" $EXPECTED_DIR/$name.c $BYPRODUCT_DIR/$name.c`
        if [ ! -z "$c_diff" ]; then
            echo_error "Mismatch in $name.c!"
            echo_error "$c_diff"
        else
            continue
            # echo "!!! SUCCESS for $name.c !!!"
        fi
    fi

    printf "\n*** END OF TEST ****\n\n"

done