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
from gxp.c_generator import fields
from gxp.c_generator.fields.base_xmler import BaseXmler
from gxp.c_generator.utils import trim_name

from pdb import set_trace

class NullEntry(BaseXmler):
    """
        Object that holds all the StructEntry entries to be part of That struct in
    the resulted .h file.
    """

    def __init__(self, name='NULL', **kwargs):
        super().__init__(name, **kwargs)
        self.close_bracket_str = kwargs.get('close_bracket_str', '')


    def pprint(self):
        msg = '{start_str}{left_space}{name}{var_close_symbol}{end_str}'
        return msg.format(
                        start_str=self.str_start,
                        left_space=self.str_left_space,
                        name=self.name,
                        var_close_symbol=self.close_bracket_str,
                        end_str=self.str_end)