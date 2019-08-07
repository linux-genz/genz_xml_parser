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


class CSubfield(BaseXmler):
    """
    """

    def __init__(self, name, field_name, sub_name, bits):
        """
            @param name: parent struct name (<struct> -> name)
            @param field_name: field name that this subfield belongs to (<field> -> name)
            @param sub_name: subfield name (<subfield> -> name)
            @param bits: dict
                        num_bits: offset's num_bits (<field> -> num_bits)
                        min_bit: subfield min_bit
                        max_bit: subfield max_bit
        """
        super().__init__(name)
        self.field_name = field_name
        self.sub_name = sub_name
        self.num_bits = int(bits['num_bits'])
        self.min_bit = int(bits['min_bit'])
        self.max_bit = int(bits['max_bit'])


    """ ---- 'STATIC INLINE' functions handlers ---- """

    @property
    def func_read(self) -> str:
        tmplt = """
static inline uint{num_bits}_t read_{func_name}
                                    (uint{field_bits}_t {field_name}) {{
    return(({field_name} & {mask_var}) >> {shift_var});
}}"""
        return tmplt.format(
            num_bits=self.num_bits,
            func_name=self.func_name,
            field_bits=self.num_bits,
            field_name=self.field_name,
            mask_var=self.mask_var_name,
            shift_var=self.shift_var_name
        )


    @property
    def func_write(self) -> str:
        tmplt = """
static inline void write_{func_name}
                                    (uint64_t *ptr, uint64_t val) {{
        {bit_check_func}
       *ptr = ((*ptr & ~{mask_var}) |
                            (val & {mask_var}) << {shift_var});
}}"""
        return tmplt.format(
            func_name=self.func_name,
            bit_check_func=self.bit_check_func_call,
            mask_var=self.mask_var_name,
            shift_var=self.shift_var_name,
        )


    @property
    def func_name(self) -> str:
        return '{struct_name}_{field_name}_{entry_name}'.format(
            struct_name=self.name,
            field_name=self.field_name,
            entry_name=self.sub_name
        )


    @property
    def bit_check_func_call(self) -> str:
        return 'validate_bit_range(val, {min}, {max}, {mask});'.format(
            min=self.min_bit,
            max=self.max_bit,
            mask=self.mask_var_name
        )

    """ ---- '#define' variable handlers ---- """

    @property
    def _var_prefix_name(self) -> str:
        return '{struct_name}_{field_name}_{entry_name}_'.format(
            struct_name=self.name.upper(),
            field_name=self.field_name.upper(),
            entry_name=self.sub_name.upper(),
        )


    @property
    def mask_var_name(self) -> str:
        return self._var_prefix_name + 'MASK'


    @property
    def shift_var_name(self) -> str:
        return self._var_prefix_name + 'SHIFT'


    @property
    def mask_var_entry(self) -> str:
        return '#define {name} {value}'.format(
            name=self.mask_var_name,
            value=hex(self.create_mask(self.min_bit, self.max_bit))
        )


    @property
    def shift_var_entry(self) -> str:
        return '#define {name} {value}'.format(
            name=self.shift_var_name,
            value=self.min_bit
        )

    """ ---- ----------------------------- ---- """

    def create_mask(self, min, max):
        return ~(~0 << min) << max


    def pprint(self):
        return self.mask_var_entry + '\n' +\
                self.shift_var_entry +'\n' +\
                self.func_read + '\n' +\
                self.func_write