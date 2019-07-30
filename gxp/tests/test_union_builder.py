#!/usr/bin/python3
import os
import unittest
import xml.etree.ElementTree
from pdb import set_trace

from gxp import c_generator
from gxp.c_generator.parsers import union_builder


class TestUnionBuilder(unittest.TestCase):

    def test_generic_field(self):
        expected = """
union genz_c_status {
    uint64_t val;
    struct {
        uint64_t unsolicited_event_ue_packet_status : 1;
        uint64_t non_fatal_internal_error_detected  : 1;
        uint64_t padding                            : 62;
    };
};
        """.strip().strip('\n')
        xml_path = './mock/union.xml'
        root = xml.etree.ElementTree.parse(xml_path).getroot()
        xml_struct = root.find('struct')

        union = union_builder.UnionBuilder(struct=xml_struct)
        union.parse()

        inst = union.instance
        result = inst[0].pprint().strip().strip('\n')
        self.assertTrue(result == expected, '\nWant:\n%s\nGot:\n%s' % (expected, result))


    def test_union_multientry(self):
        expected_1 = """
union genz_rkd_cap_1 {
    uint16_t val;
    struct {
        uint16_t rkd_mechanism_table_type : 3;
        uint16_t reserved                 : 13;
//uint64_t padding                  : 0;
    };
};""".strip().strip('\n')

        expected_2 = """
union genz_rkd_control_1 {
    uint16_t val;
    struct {
        uint16_t rkd_validation_enable : 1;
        uint16_t trusted_thread_enable : 1;
        uint16_t rsvdp                 : 14;
//uint64_t padding               : 0;
    };
};""".strip().strip('\n')

        xml_path = './mock/union_b.xml'
        root = xml.etree.ElementTree.parse(xml_path).getroot()
        xml_struct = root.find('struct')

        union = union_builder.UnionBuilder(struct=xml_struct)
        union.parse()

        inst = union.instance
        self.assertTrue(len(inst) == 2)

        result = inst[0].pprint().strip().strip('\n').strip()
        self.assertTrue(result == expected_1,
            '\nWant:\n%s\nGot:\n%s' % (expected_1, result))

        result = inst[1].pprint().strip().strip('\n').strip()
        self.assertTrue(result == expected_2,
            '\nWant:\n%s\nGot:\n%s' % (expected_2, result))


if __name__ == '__main__':
    unittest.main()