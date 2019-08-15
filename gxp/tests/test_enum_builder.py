#!/usr/bin/python3
import os
import unittest
import xml.etree.ElementTree
from pdb import set_trace

from gxp import generator
from gxp.generator.parsers import enum_builder


class TestEnumBuilder(unittest.TestCase):

    def setUp(self):
        self.this_file = os.path.abspath(__file__)
        self.this_file = os.path.dirname(self.this_file)


    def test_simple(self):
        expected = """
enum genz_c_status_c_state {
    C_STATUS_C_STATE_C_DOWN = 0x0,
    C_STATUS_C_STATE_C_CFG = 0x1,
    C_STATUS_C_STATE_C_UP = 0x2,
    C_STATUS_C_STATE_C_LP = 0x3,
    C_STATUS_C_STATE_C_DLP = 0x4
};""".strip().strip('\n')

        xml_path = os.path.join(self.this_file, 'mock/union/union.xml')
        root = xml.etree.ElementTree.parse(xml_path).getroot()
        xml_struct = root.find('struct')

        enum = enum_builder.EnumBuilder(xml_struct)
        inst = enum.instance
        self.assertTrue(len(inst) == 2, '\n--- Built enum list is not 2, but %s! ---' % len(inst))

        result = inst[0].pprint().strip().strip('\n')

        self.assertTrue(result == expected, '\nWant:\n%s\nGot:\n%s' % (expected, result))


if __name__ == '__main__':
    unittest.main()