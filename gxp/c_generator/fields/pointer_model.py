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
import logging

from gxp.c_generator.fields.base_xmler import BaseXmler
from gxp.c_generator import fields
from gxp.c_generator.models import DataTypesModel


class CPointerEntry(BaseXmler):
    """
        Creates an array entry for a "pointers" array, e.g.:
        { GENZ_CONTROL_POINTER_GENERIC, GENZ_4_BYTE_POINTER, 0x48 },

        of

        struct control_structure_pointers core_structure_pointers[] = {
            { GENZ_CONTROL_POINTER_GENERIC, GENZ_4_BYTE_POINTER, 0x48 },
            { GENZ_CONTROL_POINTER_GENERIC, GENZ_4_BYTE_POINTER, 0x4C},
            ...
        };
    """

    def __init__(self, name, p_size : str, p_value : str, p_type=None, ptr_to=None, p_flag=None, **kwargs):
        """
        @param name: name for the field to be used. Trimmed by parent class.
        @param p_size <str>: pointer size. Either '4' or '6'
        @param p_value <str>: pointer hex value, e.g. 0.40.
        @param p_flag <str>: either generic, chained, array or link. Default is None,
                            which will make it figure out a type from name.
        @param p_type <str>: structure name that this pointer points to in the
                        "enum genz_control_structure_type" entry.
        """
        super().__init__(name, **kwargs)
        self.str_close_symbol = ','
        self.ptr_to = ptr_to

        self.p_flag = p_flag
        self.p_type = p_type
        self._p_size = str(p_size)
        self.p_value = str(p_value)
        self.ptr_to = ptr_to

        self._ptr_names = self.enum_model()
        self._ptr_sizes = self.enum_sizes_model()


    @staticmethod
    def enum_model():
        return DataTypesModel.pointer_types()


    @staticmethod
    def enum_sizes_model():
        return DataTypesModel.pointer_sizes()

    @property
    def p_size(self):
        if self._p_size in self._ptr_sizes:
            return self._ptr_sizes[self._p_size]

        logging.error('Unknown pointer size %s for pointer %s! Defaulting to size 4...' %
                (self._p_size, self.name))
        return self._ptr_sizes['4']


    def is_valid_value(self):
        if self.p_value.startswith('0x'): #is a hex base 0
            try:
                int(self.p_value, 0)
            except ValueError: # should NEVER happened.
                logging.error('Failed to parse hex str value into int: %s ' % self.p_value)
                return False
        else:
            try:
                int(self.p_value, 16) #some random base. Why not 16....
            except ValueError:
                logging.error('Pointer size value failed to cast to int: %s' % self.p_value)
                return False

        return True


    def pprint(self):
        """
        :return: formatted string suited for C type struct field:
                { GENZ_CONTROL_POINTER_GENERIC, GENZ_4_BYTE_POINTER, 0x48 },
        """
        if not self.is_valid_value():
            msg = 'incorrect hex value!'
            self.str_end = '%s //FIXME: %s' % (self.str_end, msg)

        entry = '{{ {p_flag}, {p_size}, {p_value}, {p_type} }}'.format(
                    p_flag=self.p_flag,
                    p_size=self.p_size.name,
                    p_value=self.p_value,
                    p_type=self.p_type,
        )
        msg = '{start}{left_space}{entry}{var_close_symbol}{end}'
        return msg.format(
                start=self.str_start, # could indicate a comment, e.g. '//'
                left_space=self.str_left_space,
                entry=entry,
                var_close_symbol=self.str_close_symbol,
                end=self.str_end) # could be a comment description of the entry


    def __eq__(self, other):
        return self.name == other.name and \
                self.p_value == other.p_value and \
                self.p_flag == other.p_flag



    def __str__(self):
        return self.pprint()