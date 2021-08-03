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

from .base_xmler import BaseXmler
from . import CStructEntry
from . import CStruct


class CSubunion(BaseXmler):
    """
        Construct a C union instance. "padding" is added to indicate the "empty"
    space of the struct. If all the entries are less than the targeted max size,
    then a padding "difference" is indicated. E.g. fields total bits = 2, then
    padding is 62. Example:

union genz_pg_zmmu_cap_1 {
    uint32_t val;
    struct {
        uint32_t pg_zmmu_cap_1_zmmu_type                                 : 1;
        uint32_t pg_zmmu_cap_1_lpd_responder_zmmu_no_bypass_support      : 1;
        uint64_t padding                                                 : 62;
    };
};
    """

    def __init__(self, name, bits):
        super().__init__(name)
        self.struct = CStruct(None)
        self.struct.close_bracket = '%s%s' % (' ' * 4, self.struct.close_bracket)
        self.uint_bits: int = bits
        self.rv_count: int = 0


    @property
    def union_entry(self):
        rsrvd_entry = self.rsrvd_field
        #do not add rsrvd entry with 0 padding bits.
        if rsrvd_entry is not None:
            if rsrvd_entry not in self.struct.entries:
                self.struct.append(rsrvd_entry)

        return """
union {name} {{
    uint{bits}_t val;
    {struct}
}};""".format(
            bits=self.bit_scalar(self.uint_bits),
            name=self.name,
            struct=self.struct.pprint())


    @property
    def next_rv_count(self):
        rv_count = self.rv_count
        self.rv_count += 1
        return rv_count


    @property
    def rsrvd_field(self):
        """
            Calculate the padding bits (the leftover bits of the whole struct).

        @return: CStructEntry for the padding entry with the paddign bits. Or None
                if padding is <= 0.
        """
        total: int = 0 #total bits value of all fields in the union
        max: int = int(self.uint_bits) #bits limit
        comments = '' #when things go wrong, this is a field's comment
        padding = ' ' * 8 #space on the left

        # Calculate sum of all bits in the union
        for field in self.struct.entries:
            total += int(field.bitfield)

        bits_left: int = max - total #how much bits left for reserved

        # no bits left - no rsrvd field. But still have it commented...
        if bits_left == 0:
            return None
            padding = '//'

        # This should not happened, but things went wrong. Bits overflow here.
        if bits_left < 0:
            comments = ' //FIXME: bits overflow = %s' % (bits_left)
            logging.critical('%s union overflows with bits: %s!' % (self.name, bits_left))

        # Creating an field entry for the struct
        # props = {
        #     'num_bits' : bits_left,
        #     'offset_bits' : 64,
        #     }
        result = CStructEntry('padding',
                            num_type=self.bit_scalar(self.uint_bits),
                            bitfield=bits_left)
        result.l_space = padding
        result.str_end = comments

        return result


    def add(self, name, bits, var_bit_type):
        """
            Add a field to a struct entry of this union.

        @param name: field name to show up as union's entry
        @param bits: bit field value
        @param var_bit_type: utin<var_bit_type>_t
        """
        # props = {
        #     'num_bits' : bits,
        #     'offset_bits' : self.bit_scalar(var_bit_type),
        #     }
        entry = CStructEntry(name,
                            num_type=self.bit_scalar(var_bit_type),
                            bitfield=bits)
        entry.l_space *= 2
        self.struct.append(entry)


    def add_entry(self, entry):
        if entry is None:
            return
        self.struct.append(entry)


    def bit_scalar(self, input_bit):
        input_bit = int(input_bit)
        if input_bit < 8:
            return 8
        elif input_bit > 8 and input_bit < 16:
            return 16
        elif input_bit > 16 and input_bit < 32:
            return 32
        elif input_bit > 32 and input_bit < 64:
            return 64
        return input_bit


    def pprint(self):
        return self.union_entry
