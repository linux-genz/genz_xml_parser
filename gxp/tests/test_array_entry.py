#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

from gxp.generator import fields
from gxp.generator import utils


class TestArrayEntry(unittest.TestCase):


    def test_entry_empty(self):
        """
        struct control_structure_pointers core_structure_pointers[]
        """
        name = 'core_structure_pointers'
        var_type = 'struct control_structure_pointers'
        array_entry = fields.CArrayEntry(name, var_type)
        array_entry.l_space = ''
        expected = 'struct control_structure_pointers core_structure_pointers[]'
        result = array_entry.header_str
        self.assertEqual(expected, result)

        expected = 'struct control_structure_pointers core_structure_pointers[] = {};'
        result = array_entry.pprint()
        self.assertEqual(expected, result)


    def test_with_entries(self):
        """
        struct control_structure_pointers core_structure_pointers[]
        """
        name = 'Core Structure PTR 1'
        p_value = '0x48'
        expected = '{ None, GENZ_4_BYTE_POINTER, 0x48, None },'
        var_type = 'struct control_structure_pointers'
        name = name.split('PTR')[0].strip() + '_pointers'
        name = utils.trim_name(name)
        array_entry = fields.CArrayEntry(name, var_type)
        array_entry.l_space = ''

        pModel = fields.CPointerEntry(name, '4', p_value=p_value)
        array_entry.append(pModel)
        expected = 'struct control_structure_pointers core_structure_pointers[] = {\n    %s\n};' % expected
        result = array_entry.pprint()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()