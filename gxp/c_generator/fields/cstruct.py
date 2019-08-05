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
from gxp.c_generator import fields
from gxp.c_generator.fields.base_xmler import BaseXmler
from gxp.c_generator.utils import trim_name

from pdb import set_trace

class CStruct(BaseXmler):
    """
        Object that holds all the StructEntry entries to be part of That struct in
    the resulted .h file.
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        if name is not None:
            self.name = trim_name(name)
        else:
            self.name = ''

        self.datatype_str = 'struct'
        self.longest_var_str = -1
        self._commented_entries = 0
        self.child_pointers = [] #CPointerEntry collection updated by CGenerator
        self.child_arrays = []
        self.vers = kwargs.get('vers', 0)
        self.index = kwargs.get('index', -1)
        #a flag set to True if there is a chained pointer in this struct.
        self.is_chained = False


    def append(self, entry):
        """
            @param entry: StructEntry object to add to the list
        """
        # if entry in self.entries:
        #     return

        hasAdded: bool = super().append(entry)
        if not hasAdded:
            return False

        var_length = len(entry.var_type) + len(entry.name)
        if var_length > self.longest_var_str:
            self.longest_var_str = var_length

        if '//' in entry.str_start:
            self._commented_entries += 1

        return True


    def pprint(self):
        entries = []
        # Calculate spacing between var name and bits, e.g. uuint VAR '<spacing>' 5 : 5;
        # Traverse through all the entries based of the longest var_type + var_name
        # string, the spacing is calculated to align every entry in the struct.
        for entry in self.entries:
            if '//' in entry.str_start:
                entries.append(str(entry))
                continue;

            offset = self.longest_var_str - (len(entry.name) + len(entry.var_type))
            entry.str_var_space = ' ' * offset
            entries.append(str(entry))

        msg = '{start_str}{datatype}{name}{op_bracket}\n{entries}\n{cl_bracket}{end_str}'
        return msg.format(
                        start_str=self.str_start,
                        datatype=self.datatype_str,
                        op_bracket=self.open_bracket_str,
                        cl_bracket=self.close_bracket_str,
                        name=' ' + self.name + ' ' if self.name else ' ',
                        entries='\n'.join(entries),
                        end_str=self.str_end)


    def is_empty(self):
        is_empty_entries = super().is_empty()
        if is_empty_entries:
            return True

        return self._commented_entries == len(self.entries)


    def __str__(self):
        return self.pprint()


    def __eq__(self, other):
        return self.name == other.name
