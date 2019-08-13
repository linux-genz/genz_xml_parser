from abc import ABC, abstractmethod
import difflib
import math
import logging


from gxp.generator.parsers import FieldBuilderBase
from gxp.generator import fields
from gxp.generator.utils import get_name, trim_name, is_name_too_long


class ClassParser(FieldBuilderBase):
    """
        <classes>
            <class value="0">Reserved—shall not be used</class>
            <class value="1">Memory ( P2P 64 )</class>
            ...
    """

    def __init__(self, root, **kwargs):
        self.enum_name = kwargs.get('enum_name', 'hardware_types')
        self.enum = fields.CEnumEntry(self.enum_name)

        self.struct_name = kwargs.get('struct_name', 'hardware_classes_meta')
        self.name = kwargs.get('name', 'hardware_classes')

        super().__init__(root, **kwargs)


    def parse(self, root):
        """
            Generate a struct array of "meta" structs describing a Class. Refere
        to "struct_meta" property for documentation on the meta values.

            @param root: xml root tree to start parsing from.
        """
        if root is None:
            return

        if self._instance is None:
            self._instance = fields.CArrayEntry(self.name, 'struct %s' % self.struct_name)

        list_of_names = []
        longest_name_length = self._get_longest_name_length(root)

        for class_elem in root:
            value = class_elem.get('value', -1)
            raw_name = get_name(class_elem)

            trimmed_name = raw_name.lower().split('(')[0].strip()

            name = trim_name(trimmed_name, replaceable=' —[:](),=.\n', removable='\'|!<>@#$%^&*+–’-/')
            if 'switch' in name:
                name = 'switch'
            if 'bridge' in trimmed_name:
                name = 'bridge'

            if name not in list_of_names:
                list_of_names.append(name)

            enum_index =  len(self.enum.entries)
            estate = fields.EStateEntry(name.upper(), enum_index)
            spaces = ' ' * (longest_name_length - len(raw_name))
            # { raw_name, condenced_name, condenced_enum_value }
            name = '"%s", %s"%s", %s' % (raw_name, spaces, name, estate.name)
            struct_entry = fields.CStructEntry(name, ignore_long_name_warning=True)

            struct_entry.l_space = '%s { ' % struct_entry.l_space
            struct_entry.str_close_symbol = ' },'

            self._instance.append(struct_entry)
            self.enum.append(estate)

        return self.instance


    def _get_longest_name_length(self, root):
        """
            Used for plain silly prettification for the array entries. Helps to
        align the condensed names in a one column for better readability.
        """
        value = -1
        for class_elem in root:
            raw_name = get_name(class_elem)
            if len(raw_name) > value:
                value = len(raw_name)
        return value


    @property
    def struct_meta(self):
        """
            A meta struct describing a <class> field.
        "raw_name" - is a name of the class as it appears in the xml file.
        "condensed_name" - is a trimmed class' name.
        "value" - a 'condensed' indexed ('hardware_types' enum defined in __init__).
        """
        entries = [
            fields.CStructEntry('raw_name', var_type='const char * const'),
            fields.CStructEntry('condensed_name', var_type='const char * const'),
            fields.CStructEntry('value', var_type='const enum %s' % self.enum.name), #name of the enum
        ]
        struct_instance = fields.CStruct(self.struct_name, entries=entries)
        return struct_instance