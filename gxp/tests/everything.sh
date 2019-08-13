#!/bin/bash

test_files=$(find . -name 'test_*.py')

for i in $test_files; do
  $i
done