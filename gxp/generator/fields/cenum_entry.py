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
from gxp import generator


class CEnumEntry(BaseXmler):
    """
    An Enum formated for the C language entry:
        enum <name> {
            estate_entry field,
        }
    """

    def __init__(self, name, **kwargs):
        """
            @param name: Name of the Enum definition.
        """
        super().__init__(name, **kwargs)
        self._longest_name: int = -1


    def pprint(self):
        """ Formats XML parsed entries into a 'proper' display format:

        enum genz_c_status_c_state { };
        """
        states = ''
        for index in range(len(self.entries)):
            entry = self.entries[index]
            states = '%s\n%s' % (states, entry.pprint())
        states = states.lstrip('\n')
        states = states.rstrip(',')

        return '{str_start}enum {name} {br_op}\n{enums}\n{br_cl}{str_end}'.format(
                        str_start=self.str_start,
                        br_op=self.open_bracket,
                        name=self.name,
                        enums=states,
                        br_cl=self.close_bracket,
                        str_end=self.str_end
                        )