import logging
from gxp.generator import fields
from gxp.generator.parsers import FieldBuilderBase
from gxp.generator.utils import get_name, trim_name


class UnionBuilder(FieldBuilderBase):

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)


    def parse(self, root):
        """
            Union instance is construced from the <subfield> tag that is a child
        of <field>. Union's instance name is the <name> of the <subfield> <field>.
        However, ignore any subfield that has <value> children! Each struct's entry
        is a <name> of the <subfield>. Entry's bit is <subfield> "num_bits" attribute
        value. Entry var type is a "num_bits" of a <field> but scaled up to the
        closest uint<int>_t value. Thus, targeted field are:
            <offset> -> <field> -> <subfield> -> <name>

        """
        if self._instance is None:
            self._instance = []

        offsets = root.findall('offset')
        for xml_offset in offsets:
            for xml_field in xml_offset.findall('field'):
                union_instance = self._create_entry(xml_field)
                if union_instance is not None:
                    self._instance.append(union_instance)


    def _create_entry(self, field):
        """
            Look at self.parse for full documentation.
        This looks at <subfield> fields of the <field> to create the union entries.

        @param field: xml field to extract <subfield> from.
        @return: CSubunion instance with all the added entries. Or None if failed.
        """
        xml_subfields = field.findall('subfield')

        name = get_name(field)
        field_name = trim_name(name)
        field_bits = field.get('num_bits', -1)

        try:
            int(field_bits)
        except Exception:
            logging.error('%s failed to parse bits to int: %s' % (name, field_bits))
            return

        union_instance = None
        for xml_subfield in xml_subfields:
            subfield_name: str = get_name(xml_subfield)
            subfield_name = trim_name(subfield_name)
            if xml_subfield.find('value') is not None:
                continue

            if union_instance is None:
                union_instance = fields.CSubunion('genz_%s' % field_name, field_bits)

            sub_bits = xml_subfield.get('num_bits', -1)
            union_instance.add(subfield_name, sub_bits, field_bits)

        return union_instance