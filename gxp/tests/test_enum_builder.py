#!/usr/bin/python3
import os
import unittest
import xml.etree.ElementTree
from pdb import set_trace

from gxp import c_generator
from gxp.c_generator.parsers import enum_builder


class TestEnumBuilder(unittest.TestCase):

    def test_simple(self):
        expected = """
enum genz_c_status_c_state {
    C_STATUS_C_STATE_C_DOWN = 0x0,
    C_STATUS_C_STATE_C_CFG = 0x1,
    C_STATUS_C_STATE_C_UP = 0x2,
    C_STATUS_C_STATE_C_LP = 0x3,
    C_STATUS_C_STATE_C_DLP = 0x4
};""".strip().strip('\n')

        xml_path = './mock/union.xml'
        root = xml.etree.ElementTree.parse(xml_path).getroot()
        xml_struct = root.find('struct')

        enum = enum_builder.EnumBuilder(struct=xml_struct)
        enum.parse()
        inst = enum.instance
        self.assertTrue(len(inst) == 1, '\n--- Built enum list is not 1, but %s! ---' % len(inst))

        result = inst[0].pprint().strip().strip('\n')

        self.assertTrue(result == expected, '\nWant:\n%s\nGot:\n%s' % (expected, result))


    def test_multientry(self):
        expected = [
"""
enum genz_component_cap_1_c_state_power_control_support {
    COMPONENT_CAP_1_C_STATE_POWER_CONTROL_SUPPORT_NOTIFICATION_ONLY = 0x0,
    COMPONENT_CAP_1_C_STATE_POWER_CONTROL_SUPPORT_NOTIFICATION_AND_TRANSITION_REQUESTS = 0x1
};""".strip().strip('\n'),

"""
enum genz_component_cap_1_the_name {
    COMPONENT_CAP_1_THE_NAME_1_0 = 0x0,
    COMPONENT_CAP_1_THE_NAME_0_1 = 0x1,
    COMPONENT_CAP_1_THE_NAME_0_01 = 0x2
};""".strip().strip('\n'),
        ] #list of expected entries

        xml_path = './mock/enum_wacky.xml'
        root = xml.etree.ElementTree.parse(xml_path).getroot()
        xml_struct = root.find('struct')

        enum = enum_builder.EnumBuilder(struct=xml_struct)
        enum.parse()
        inst = enum.instance
        self.assertTrue(len(inst) == 2, '\n--- Built enum list is not 2, but %s ---' % len(inst))
        result = inst[0].pprint().strip().strip('\n')
        self.assertTrue(result == expected[0], '\nWant:\n%s\nGot:\n%s' % (expected[0], result))

        result = inst[1].pprint().strip().strip('\n')
        self.assertTrue(result == expected[1], '\nWant:\n%s\nGot:\n%s' % (expected[1], result))


if __name__ == '__main__':
    unittest.main()