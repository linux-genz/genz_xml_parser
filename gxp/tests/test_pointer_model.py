#!/usr/bin/python3
import os
import unittest
from pdb import set_trace

from gxp import c_generator


class TestPointerModel(unittest.TestCase):

    def test_generic_field(self):
        name = 'Control Structure PTR 1'
        p_value = '0x48'
        expected = '{ GENZ_CONTROL_POINTER_GENERIC, GENZ_4_BYTE_POINTER, 0x48 },'

        pModel = c_generator.CPointerEntry(name, '4', p_value)
        result = pModel.pprint().strip()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()