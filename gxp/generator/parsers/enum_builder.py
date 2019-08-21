import logging
from gxp.generator import fields
from gxp.generator.parsers import FieldBuilderBase
from gxp.generator.utils import get_name, trim_name


class EnumBuilder(FieldBuilderBase):

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)


    def parse(self, root):
        """
            Enum instance is construced from the <value> tag, a child of <subfield>
        that is a child of <field>. Enum's instance name is the <name> of the <subfield>.
        Each entry is a <name> of the <value>. Entry's value of that enum is the
        "val" attribute of that <value> field.

        @param struct: <optional>. If not set - constructor's struct is used.
                xml <struct> entry that has <offset><field><subfield> structure.
        """
        if self._instance is None:
            self._instance = []
        offsets = root.findall('offset')
        for xml_offset in offsets:
            for xml_field in xml_offset.findall('field'):
                self._create_entry(xml_field)


    def _create_entry(self, field):
        """
            Look at self.parse for full documentation.
        This looks at <subfield> fields of the <field> to create the union entries.
        """
        xml_subfields = field.findall('subfield')
        xml_subfields.append(field) #Weird, but true. <value> can be in <field> too.

        name = get_name(field)
        field_name = trim_name(name)
        field_bits = field.get('num_bits', -1)

        try:
            int(field_bits)
        except Exception:
            logging.error('%s failed to parse bits to int: %s' % (name, field_bits))
            return None

        enum_instance = None
        for xml_subfield in xml_subfields:
            xml_values = xml_subfield.findall('value')
            if xml_values is None or len(xml_values) == 0: # No value - not an enum
                continue

            if xml_subfield != field:
                subfield_name: str = get_name(xml_subfield)
                subfield_name = trim_name(subfield_name)
            else:
                subfield_name = ''

            inst_name = 'genz_%s_%s' % (field_name, subfield_name)
            #empty subfield_name produces trailing '_'. Thus - clean it up.
            inst_name = inst_name.strip('_')

            enum_instance = fields.CEnumEntry(inst_name)

            for xml_value in xml_values:
                entry_name = get_name(xml_value)
                entry_name = trim_name(entry_name)
                if entry_name == 'reserved':
                    continue

                entry_name = '%s_%s_%s' % (field_name, subfield_name, entry_name)
                entry_name = trim_name(entry_name)
                entry_name = entry_name.upper()

                val = xml_value.get('val', -1)
                entry = fields.EStateEntry(entry_name, val)
                enum_instance.append(entry)

            self._instance.append(enum_instance)