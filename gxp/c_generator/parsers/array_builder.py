import logging
from gxp.c_generator import fields
from gxp.c_generator.parsers import FieldBuilderBase
from gxp.c_generator.utils import get_name, trim_name


class ArrayBuilder(FieldBuilderBase):
    """
        <array> field indicates an Array entry.
        <field><name> array's entry field. It follows the same as for parsing
        regular fields of <struct>.
    """

    def __init__(self, root, **kwargs):
        self.type_name = 'struct genz_control_structure_ptr'
        super().__init__(root, **kwargs)


    def parse(self, root=None):
        """
            @param root: xml root tree to start parsing from.
        """
        root_name = get_name(root)
        arrays = root.findall('array')
        is_indexed = False
        if len(arrays) > 1:
            logging.warn('More than one <array> in "%s"... not bad, but not good either.' % root_name)
            is_indexed = True

        #use indexed loop to asign index to the name when(if) more than one array
        for index in range(len(arrays)):
            array_xml = arrays[index]
            elements = array_xml.findall('element')
            array_offset = array_xml.get('offset', -1)
            if len(elements) > 1:
                logging.warn('More than one <element> in "%s" with "%s" array offset... only first will get parsed.' %
                            (root_name, array_offset))
            if len(elements) == 0:
                logging.warn('No <element> in array of "%s"! Skipping...' % root_name)
                continue

            element = elements[0] #only One element in the <array> makes sense here.
