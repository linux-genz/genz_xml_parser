#!/usr/bin/python3
"""
(C) Copyright 2018 Hewlett Packard Enterprise Development LP” on your code

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
import pprint

def read(path):
    content = []
    with open(path, 'r') as file_obj:
        content = file_obj.read().split('\n')

    return content


def remove_quotes(err_text):
    first = err_text.find('‘')
    second = err_text.find('’')

    if first == -1 or second == -1:
        return ['', '']

    var_name = err_text[first+1:second]
    trimmed = err_text.replace(err_text[first:second + 1], '<VAR_NAME>')
    trimmed = trimmed.strip(' ')

    return [trimmed, var_name]


def group(content):
    result = {}
    for line in content:
        error = line.split('error')[-1]

        try:
            #try extracting Line number where error occures.
            err_line = line.split(':')[1]
        except IndexError:
            err_line = None

        error = error.strip(':').strip(' ')
        error, var_name = remove_quotes(error)

        if err_line is not None:
            var_name = '%s -> line: %s' % (var_name, err_line)

        if not error:
            continue
        if error not in result:
            result[error] = []

        if var_name not in result[error]:
            result[error].append(var_name)

    return result


def main(cmd_args):
    content = read(cmd_args['path'])
    grouped = group(content)

    pp = pprint.PrettyPrinter(width=120)
    pp.pprint(grouped)

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XML parser parameters')
    parser.add_argument('path',
                        help='Path to an XML file to parse into .h')


    args = parser.parse_args()
    main(vars(args))