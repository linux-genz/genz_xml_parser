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
from gxp.generator.utils import is_name_too_long


class CStructEntry(BaseXmler):
    """
        A class that builds a C struct's entry field, e.g:
            uint64_t size : 16;
    """

    def __init__(self, name, num_type: int=None, bitfield: int=None,
                no_scale_down=False, var_type=None, **kwargs):
        """
            @param name: name for the field to be used.
            @param num_type: numeric variable type value: uint<num_type>_t, (e.g. uint64_t)
            @param bitfield: number of bits if it is a bitfield entry (e.g. "uint64_t size : 16;").
                            Pass -1 or None to omit bitfield (e.g. "uint64_t size;").
            @param var_type <str>: sets the entry's variable type. This will overrides
                            the use of "uint<num_type>_t" type.
        """
        super().__init__(name, **kwargs)
        self.bitfield: int = None
        self.num_type: int = None
        self._value = kwargs.get('value', None)
        self.ignore_long_name_warning = kwargs.get('ignore_long_name_warning', False)

        if bitfield is not None:
            try:
                self.bitfield = int(bitfield)
            except (ValueError, TypeError) as err:
                self.bitfield = -1
                self.str_end = '//FIXME: error %s' % (err)

        if num_type is not None:
            try:
                self.num_type = int(num_type)
            except (ValueError, TypeError) as err:
                self.num_type = num_type
                self.str_start = '//'
                self.str_end = '//FIXME: num_type is not int for the %s struct entry' % name

            #A uintN_t cant be bigger than 64 bits. So don't allow overflow
            if no_scale_down is False:
                if self.num_type > 64:
                    self.num_type = 64

        self._var_type = var_type
        self.str_close_symbol: str = ';'
        # entry could be an enum or a struct or whatever. This is a "pointer" to
        # the definition object this entry refering to. If None - this is just a
        # primitive typed entry.
        self.definition = None
        self._pointers: list = []


    @property
    def var_type(self):
        if self._var_type is not None:
            return self._var_type

        # if 'uuid' in self.name:
        #     if self.definition is None:
        #         return 'uuid_t'
        if self.num_type is not None:
            return 'uint%s_t' % self.num_type

        return ''


    @var_type.setter
    def var_type(self, value):
        self._var_type = value


    @property
    def pointer_type(self):
        if not '_ptr' in self.name:
            return None

        splitted = self.name.split('_ptr')
        ptr_number = splitted[-1].strip() #either empty or a number
        if ptr_number.isdigit():
            return ''


    def pprint(self):
        """
        :return: formatted string suited for C type struct field:
                    uint<offset_bits>_t <var_name> : <bitfield>
        """
        # if 'uuid' in self.name and self.definition is None:
        #     return '%s%s %s;' % (self.l_space, self.var_type, self.name)

        colon_with_bits = '{var_space} : {bits_val}'\
            .format(var_space=self.var_space,
                    bits_val=self.bitfield)
        # when no num_bits are set, then entry will look like:
        # "var_type Name;"
        if (self.bitfield is not None):
            bits = int(self.bitfield)
        if (self.bitfield is None or bits < 0 or
            (self.num_type is not None and self.num_type == bits)):
            colon_with_bits = ''
        if self._value is not None:
            colon_with_bits = ' = %s' % self._value

        end_str = self.str_end
        length_comment = is_name_too_long(self.name)
        if length_comment:
            if not self.ignore_long_name_warning:
                end_str = '%s %s' % (self.str_end, length_comment)

        var_type = '' if not self.var_type else '%s ' % self.var_type
        msg = '{start}{left_space}{var_type}{name}{bits}{var_close_symbol}{end}'
        return msg.format(
                 start=self.str_start, # could indicate a commented, e.g. '//'
                 left_space=self.l_space,
                 var_type=var_type,
                 name=self.name,
                 bits=colon_with_bits,
                 var_close_symbol=self.str_close_symbol,
                 end=end_str) # could be a comment description of the entry


    def __str__(self):
        return self.pprint()
