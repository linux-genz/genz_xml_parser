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
from gxp.c_generator.fields.base_xmler import BaseXmler
from gxp.c_generator.utils import is_name_too_long


class CDefineEntry(BaseXmler):
    def __init__(self, name, value, **kwargs):
        """
        #define GENZ_MIN_STRUCTURE					(0x0)

            @param name: name for the field to be used.
        """
        super().__init__(name, **kwargs)
        self.value = value
        self.str_left_space = kwargs.get('str_left_space', '')


    def pprint(self):
        """
        :return: formatted string suited for C type struct field:
                    uint<offset_bits>_t <var_name> : <num_bits>
        """
        length_comment = is_name_too_long(self.name)
        if length_comment:
            end_str = '%s %s' % (self.str_end, length_comment)
        else:
            end_str = self.str_end

        msg = '{start}{left_space}#define {name}{name_space}{bits}{end}'
        return msg.format(
                 start=self.str_start, # could indicate a commented, e.g. '//'
                 left_space=self.str_left_space,
                 name=self.name.upper(),
                 name_space=self.space_after_name,
                 bits=self.value,
                 end=end_str) # could be a comment description of the entry


    def __str__(self):
        return self.pprint()