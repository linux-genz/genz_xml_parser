import logging

from gxp.generator import fields
from gxp.generator.models import DataTypesModel
from gxp.generator.parsers import FieldBuilderBase
from gxp.generator.utils import get_name, trim_name


class PointerBuilder(FieldBuilderBase):

    def __init__(self, root, **kwargs):
        self.type_name = 'struct genz_control_structure_ptr'
        super().__init__(root, **kwargs)
        self.DataTypes = kwargs.get('data_types', DataTypesModel)


    def parse(self, root):
        struct_name = get_name(root)
        struct_name = trim_name(struct_name)
        entry_name = '%s_ptrs' % struct_name

        if self._instance is None:
            self._instance = fields.CArrayEntry(entry_name, self.type_name)
            self._instance.parent = self.root

        offsets = root.findall('offset')
        for offset in offsets:
            p_value = offset.get('value', -1)
            for field in offset.findall('field'):
                if field.get('ptr_to', None) is None:
                    continue

                entry = self._create_entry(field=field, p_value=p_value)
                if entry is not None:
                    self._instance.append(entry)

        if len(self._instance.entries) == 0:
            self._instance = None


    def _create_entry(self, field, p_value):
        """
         TODO

        @param field
        @param entry_name <str>: name of the pointer (not the Type name).
        @param type_name <str>: entry type name.

        @return: created/parsed entry on success. None - nothing happened.
        """
        field_name = get_name(field)
        field_name = trim_name(field_name)

        field_num_bits = field.get('num_bits')
        ptr_to = field.get('ptr_to', None)
        if ptr_to is None:
            return None

        try:
            field_min_bits = int(field.get('min_bit'))
        except ValueError:
            # in a perfect world - this should never happened.
            logging.warning('Field %s min_bits is not int?' % field_name)
            field_min_bits = -1

        p_size = '4' if field_num_bits == '32' else '6'
        if field_min_bits > 0:
            try:
                p_value = int((field_min_bits / 8) + int(p_value, 0))
                p_value = hex(p_value)
            except ValueError:
                p_value = '-1'

        pointer_entry = fields.CPointerEntry(field_name, p_size, p_value, ptr_to=ptr_to)
        pointer_entry.parent = self.root

        return pointer_entry