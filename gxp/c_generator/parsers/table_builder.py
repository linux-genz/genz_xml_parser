from abc import ABC, abstractmethod
from gxp.c_generator.parsers import FieldBuilderBase
import math
import logging

from gxp import CGenerator
from gxp.c_generator import fields
from gxp.c_generator.utils import get_name, trim_name, is_name_too_long


class TableBuilder(FieldBuilderBase):
    """
        Re-using CGenerator to generate (almost recursively).
        <structs> == <element>
        the rest is as-is
    """
    def __init__(self, root, **kwargs):
        self.elements_type = None
        self.parent = None
        super().__init__(root, **kwargs)


    def parse(self, root):
        """
         In the Root - find <array> element and parse it by the rules of a regular
        <struct> entry.
        """
        arrays = root.findall('array')
        if len(arrays) == 0:
            return

        if self._instance is None:
            self._instance = []

        for array in arrays:
            if self.elements_type is None:
                self.elements_type = array.get('elements')
            elements = array.findall('element')
            for element in elements:
                name_to_set = get_name(root)
                # if not name_to_set.lower().endswith('array'):
                name_to_set = '%s Array' % name_to_set
                element.set('name', name_to_set)

            cgen = CGenerator.CGenerator(root, parse_on_init=False, name='table: %s' % name_to_set)
            cgen.struct_tag_name = 'element'
            cgen.parse_xml(array)
            self._instance.append(cgen)