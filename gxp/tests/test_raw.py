#!/usr/bin/python3
import os
import sys
import glob
import shutil
import unittest
from pdb import set_trace

from gxp import xml_to_header

class TestRaw(unittest.TestCase):

    byproduct_dir = '/tmp/gxp_test/'


    def test_entry_empty(self):
        """
        struct control_structure_pointers core_structure_pointers[]
        """
        self.assertTrue(self.byproduct_dir.startswith('/tmp'), 'destination is not in tmp?!')

        this_file = os.path.realpath(__file__)
        this_dir = os.path.dirname(this_file)
        to_search = os.path.join(this_dir, 'mock/*/') + '*.xml'

        mockfiles = glob.glob(to_search, recursive=True)
        self.assertTrue(len(mockfiles) > 0)

        sys.argv.extend([' ', ' '])

        for target in mockfiles:
            xml_name = os.path.basename(target).split('.xml')[0]
            dest = os.path.join(self.byproduct_dir, xml_name)

            sys.argv[1] = target
            sys.argv[2] = '-o %s' % dest
            args = xml_to_header.parse_args()
            xml_to_header.main(vars(args))

            header_created = os.path.exists('%s.h' % dest)
            c_created = os.path.exists('%s.c' % dest)

            self.assertTrue(header_created)
            self.assertTrue(c_created)


    @classmethod
    def tearDownClass(cls):
        if not os.path.exists(cls.byproduct_dir):
            return
        if not cls.byproduct_dir.startswith('/tmp'):
            return

        shutil.rmtree(cls.byproduct_dir)


if __name__ == '__main__':
    unittest.main()