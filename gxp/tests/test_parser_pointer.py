#!/usr/bin/python3
import os
import unittest
import xml.etree.ElementTree
from pdb import set_trace

from gxp.c_generator.parsers import pointers


class TestParserPtr(unittest.TestCase):

    def setUp(self):
        self.XML_PATH = './mock/pointers.xml'
        self.xml = xml.etree.ElementTree.parse(self.XML_PATH).getroot()


    def test_single_line(self):
        entry_name = 'core_structure_ptrs'
        type_name='struct some_struct_name'
        expected = '%s %s[]' % (type_name, entry_name)

        for struct in self.xml:
            # ptrs.struct
            ptrs = pointers.PointerParser(struct=struct)
            ptrs.type_name = type_name
            ptrs.super_parse()
            # for offset in struct:
            #     ptrs.offset = offset
            #     for field in offset:
            #         ptrs.parse(field=field,
            #                 entry_name='entry_name_array',
            #                 type_name='struct some_struct_name')

        entry = ptrs.array

        self.assertIsNotNone(ptrs.array)
        self.assertTrue(len(ptrs.array.entries) == 2)
        self.assertTrue(entry.header_str.startswith(expected),
                        '\nexp: %s\ngot: %s' % (expected, entry.header_str))


if __name__ == '__main__':
    unittest.main()