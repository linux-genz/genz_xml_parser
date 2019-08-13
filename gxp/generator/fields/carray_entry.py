#!/usr/lib/python3
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
from .base_xmler import BaseXmler
from pdb import set_trace


class CArrayEntry(BaseXmler):
    def __init__(self, name, var_type, is_allow_empty=True):
        """
            @param name: name for the field to be used.
            @param var_type: array's type. Could be: 'struct control_structure_pointers'
        """
        super().__init__(name)
        self.str_entries_join = '\n'
        self.l_space = ''
        self.var_type = var_type
        self.is_allow_empty = is_allow_empty


    def append(self, entry : BaseXmler, is_no_duplicates=False):
        """
            Add entry to the list.

        @param entry <BaseXmler>: entry to add.
        @param is_no_duplicate <bool>: default=False. Set True for no duplicate entries.
        @return: True - unique addition. False - duplicate entry.
        """
        is_duplicate = entry in self.entries
        if is_duplicate and is_no_duplicates:
            return False

        self.entries.append(entry)
        return not is_duplicate


    @property
    def header_str(self):
        header = '{start}{left_space}{var_type} {name}[]'
        return header.format(
                 start=self.str_start, # could indicate a commented, e.g. '//'
                 left_space=self.l_space,
                 var_type=self.var_type,
                 name=self.name)


    def pprint(self):
        """
        :return: formatted string suited for C type struct field:
            struct control_structure_pointers core_structure_pointers[] = { entries }
        """

        if len(self.entries) > 0:
            entries_str = [val.pprint() for val in self.entries]
            entries_str = self.str_entries_join.join(entries_str)
            entries_str = '\n%s\n' % entries_str
        else:
            entries_str = ''

        msg = '{header} = {{{entries}{var_close_symbol}{end}'
        if not entries_str:
            if not self.is_allow_empty:
                msg = '{header};'

        return msg.format(
            header=self.header_str,
            entries=entries_str,
            var_close_symbol=self.close_bracket,
            end=self.str_end,
        )


    def __str__(self):
        return self.pprint()