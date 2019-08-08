#!/usr/bin/python3
import os
import glob
import unittest
from pdb import set_trace

class TestRaw(unittest.TestCase):


    def test_entry_empty(self):
        """
        struct control_structure_pointers core_structure_pointers[]
        """
        this_file = os.path.realpath(__file__)
        this_dir = os.path.dirname(this_file)
        to_search = os.path.join(this_dir, 'mock/') + '*.xml'

        mockfiles = glob.glob(to_search, recursive=True)
        self.assertTrue(len(mockfiles) > 0)


if __name__ == '__main__':
    unittest.main()