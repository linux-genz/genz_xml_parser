from abc import ABC, abstractmethod
from gxp.c_generator.parsers import FieldBuilderBase
import math
import logging

from gxp.c_generator import fields
from gxp.c_generator.utils import get_name, trim_name, is_name_too_long


class StructBuilder(FieldBuilderBase):
    """
        <struct name="">
            <offset num_bits="">
                <field num_bits="">
                    <name>
    """

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)


    def parse(self, root):
        """
            @param root: xml root tree to start parsing from.
        """
        # if self.expected_tag is not None and root.tag is not self.expected_tag:
        #     return

        if self._instance is None:
            self._instance = self.build_struct_instance(root)

        offsets = root.findall('offset')

        for xml_offset in offsets:
            bits = xml_offset.get('num_bits', -1)
            for xml_field in xml_offset:
                entry = self.create_entry(xml_field, bits)
                if entry is None:
                    continue

                if isinstance(entry, list):
                    self._instance.extend(entry)
                else:
                    self._instance.append(entry)


    def build_struct_instance(self, field):
        """
            TODO
        """
        if not isinstance(field, str):
            name = get_name(field)
        else:
            name = field

        name = trim_name(name)

        struct = fields.CStruct('genz_%s' % name, origin=field)
        struct.vers = field.get('vers', None)
        struct.index = field.get('type', 0)

        # struct.tag = self.root.tag
        length_comment = is_name_too_long(struct.name)
        if length_comment:
            struct.open_bracket_str = '%s %s' % (struct.open_bracket_str, length_comment)
        return struct


    def create_entry(self, field, bits):
        """
            TODO
        """
        if field is None:
            logging.error('Failed parsing field (is None)! Root: %s' % self.root)
            return

        s_entry = None
        name = get_name(field)
        field_name = trim_name(name)

        # If a field has <value> entries - it is an Enum, not a struct entry.
        if (len(field.findall('value')) > 0):
            logging.info('A "%s" field is an Enum...' % field_name)
            if (len(field.findall('subfield')) > 0):
                msg = 'Both <value> and <subfield> in the "%s" field!'
                msg += ' What is it? Struct entry or Enum?'
                logging.error(msg % (field_name))
            return

        props = field.attrib
        is_no_name = False

        if name is None:
            name = str(field.attrib)
            is_no_name = True

        if props.get('offset_bits', None) is None:
            props['offset_bits'] = bits

        var_type = None
        bitfield = props['num_bits']
        if 'uuid' in field_name:
            var_type = 'uuid_t'
            bitfield = -1

        s_entry = fields.CStructEntry(name=field_name,
                                    num_type=props['offset_bits'],
                                    bitfield=bitfield,
                                    var_type=var_type)

        s_entry.parent = self.root
        if is_no_name:
            s_entry.str_start = '//'
            s_entry.str_end = ' //FIXME: entry had no name'

        #FIXME: we are ignoring ... entries for now, but will be fixed later
        if s_entry.name == '...':
            s_entry.str_start = '//'
            s_entry.str_end = ' //FIXME: name "..." entry'

        #FIXME: write this to a file, but comment it out to know which entries
        # we can't parse.
        if s_entry.bitfield == 0 or s_entry.num_type == 0:
            s_entry.str_start = '//'
            s_entry.str_end = ' //FIXME: 0 bits.'
            return s_entry

        if name.lower() == 'unknown':
            s_entry.str_start = '//'
            s_entry.str_end = ' //FIXME: UNKNOWN in name'

        if 'rsvd' in name.lower():
            s_entry.str_start = '//'
            s_entry.str_end = ' //FIXME: skipping rsvd(X) fields for now'

        if s_entry.bitfield > s_entry.num_type:
            try:
                s_entry = self.split_entry(s_entry)
            except Exception as err:
                s_entry.str_start = '//'
                s_entry.str_end =' //FIXME: !!Error!!: %s' % err

        return s_entry


    def split_entry(self, entry: fields.CStructEntry):
        """
            When struct entry bits exceeding offset_bits, the entry needs to be
        splitted in chunks.

        @param: dict or CStructEntry object to be splitted.
        """
        if entry.num_type == -1 or entry.bitfield == None or entry.bitfield == -1:
            #this is not a bitfield entry, so skip it.
            return []

        result = []
        num_of_splits = entry.bitfield / entry.num_type

        num_of_splits = math.ceil(num_of_splits)
        num_of_splits = int(num_of_splits)
        bits_left = entry.num_type
        for index in range(num_of_splits):
            name = entry.fields.get('name')
            splited_entry = fields.CStructEntry(name=name,
                                                num_type=entry.num_type,
                                                bitfield=entry.bitfield)

            splited_entry.name = '%s_%s' % (splited_entry.name, index + 1)
            splited_entry.definition = entry.definition
            splited_entry.bitfield = bits_left
            splited_entry.str_end = ' //NOTE: splitted bit'

            bits_left = entry.bitfield - ((index + 1) * entry.num_type)
            result.append(splited_entry)

        return result