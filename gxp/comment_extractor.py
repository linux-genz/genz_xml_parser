#!/usr/bin/python3
"""
(C) Copyright 2019 Hewlett Packard Enterprise Development LP” on your code

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import argparse
import os


def extract_lines(input_file, to_find):
    if not os.path.exists(input_file):
        print('Input file not found: %s' % input_file)
        return None

    content = ''
    result = []
    with open(input_file, 'r') as file_obj:
        content = file_obj.read().split('\n')

    for line in content:
        if to_find in line:
            result.append(line)

    return result


def main(args):
    input_file = args['input_file']
    output_file = args['output']
    to_find = args['find']
    print(to_find)
    lines = extract_lines(input_file, to_find)
    if not lines:
        print('Nothing to write?')
        return

    with open(output_file, 'w+') as file_obj:
        print('Writing to %s' % output_file)
        file_obj.write('\n'.join(lines))


def parse_args():
    this_file = os.path.realpath(__file__)
    this_dir = os.path.dirname(this_file)
    parser = argparse.ArgumentParser(description='XML parser parameters')

    parser.add_argument('input_file',
                        help='Input file to extract lines from.')

    parser.add_argument('--output', '-o',
                        help='Where to save output to.',
                        required=True)

    parser.add_argument('--find', '-f',
                        help='String pattern to find.',
                        required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(vars(args))