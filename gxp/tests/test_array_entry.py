#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

from genz_specs_parser import datastruct


class TestArrayEntry(unittest.TestCase):


    def test_entry_empty(self):
        """
        struct control_structure_pointers core_structure_pointers[]
        """
        name = 'core_structure_pointers'
        var_type = 'struct control_structure_pointers'
        array_entry = datastruct.CArrayEntry(name, var_type)
        array_entry.str_left_space = ''
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
        expected = '{ GENZ_CONTROL_POINTER_GENERIC, GENZ_4_BYTE_POINTER, 0x48 },'
        var_type = 'struct control_structure_pointers'
        array_entry = datastruct.CArrayEntry(name.split('PTR')[0] + '_pointers', var_type)
        array_entry.str_left_space = ''

        pModel = datastruct.CPointerEntry(name, '4', p_value)
        array_entry.append(pModel)
        expected = 'struct control_structure_pointers core_structure_pointers[] = {\n    { GENZ_CONTROL_POINTER_GENERIC, GENZ_4_BYTE_POINTER, 0x48 },\n};'
        result = array_entry.pprint()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()