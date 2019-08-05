#!/usr/lib/python3
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

def trim_name(name, replaceable=' —-/[:](),=.\n', removable='|!<>@#$%^&*+–’'):
    """
        Replace garbage with the '_' character.
    :param name: a field name to be trimmed from garbage chars not allowed by
                C compiler.
    :return: trimmed name.
    """
    split_spaces = name.split(' ')
    if split_spaces[0].isnumeric():
        split_spaces.append(split_spaces.pop(0))
        name = ' '.join(split_spaces)
        name = name.replace('µs', 'us') # - µs = us - microseconds

    name = name.replace('µs', 'us') # - µs = us - microseconds

    for to_replace in replaceable:
        name = name.replace(to_replace, '_')

    for to_remove in removable:
        name = name.replace(to_remove, '')

    #make every '_' an empty str in the splitted list
    no_underscore = name.split('_')
    #remove empty str from the list which used to be '_'
    no_underscore = [word for word in no_underscore if word]
    #join words with '_'
    name = '_'.join(no_underscore)

    name = name.lower()
    name = name.replace('</sub>', '')
    name = name.replace('<sub>', '_SUB_')

    if name[0].isdigit():
        name = '_%s' % name

    return name


def get_name(field):
    """
        The <struct> field will have a "name" property. Otherwise:

        Each <field> or <subfield> is expected to have a child field <name>
    containing the name for that field. This function extracts that.
    """
    name_field = field.find('name')
    if name_field is not None:
        name_field = name_field.text

    if name_field is None:
        name_field = field.get('name', None)

    if name_field is None:
        name_field = field.text.strip().strip('\n')

    return name_field


def is_name_too_long(name):
    """
        Check entry's name length and shorten it to 20 max char with a comment
    note.
    Also, check if length was cut in the middle of the word and left less than 5
    characters. Its a "bold" assumption, but we assume one can guess a shorted
    word if given at least 5 first characters of it
        @param entry: struct or structentry object.
        return:
    """
    max_length = 50
    if len(name) <= 50:
        return None

    return '//FIXME: name too long.'