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
from gxp.generator.fields.base_xmler import BaseXmler


class EStateEntry(BaseXmler):
    """
        An entry for the Enum instance.
    """

    def __init__(self, name, value, **kwargs):
        """
            @param name: name of the enum state.
            @param value: Value of the state.
        """
        super().__init__(name, **kwargs)
        #FIXME: hack. Few entries has those values that python crashes on.
        if value == '0b':
            value = '0x0'
        if value == '1b':
            value = '0x1'

        self.value = value
        self.close_bracket: str = kwargs.get('close_bracket', ',')



    def pprint(self):
        """ Formats XML parsed entries into a 'proper' display format.

        ENTRY_NAME = 0x0,
        """
        start_str = self.str_start
        str_end = self.str_end

        if not self.value and self.value != 0:
            start_str = '//%s' % start_str
            str_end = '/* FIXME: value not set! */ %s' % str_end

        return '{str_start}{left_space}{name} = {value}{close_symbol}{str_end}'.format(
                        str_start=start_str,
                        left_space=self.l_space,
                        name=self.name,
                        value=self.value,
                        close_symbol=self.close_bracket,
                        str_end=str_end)