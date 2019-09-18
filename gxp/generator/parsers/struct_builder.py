from abc import ABC, abstractmethod
from gxp.generator import parsers
import math
import logging

from gxp.generator import fields
from gxp.generator.utils import get_name, trim_name, is_name_too_long


class StructBuilder(parsers.FieldBuilderBase):
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
                    enum_builder = parsers.EnumBuilder(xml_field)
                    enums = enum_builder._create_entry(xml_field)
                    enum_builder._instance.extend(enums)
                    entry = enum_builder.as_bitfield

                    if entry is None or len(entry) == 0:
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
        struct.index = field.get('type', -1)

        # struct.tag = self.root.tag
        length_comment = is_name_too_long(struct.name)
        if length_comment:
            struct.open_bracket = '%s %s' % (struct.open_bracket, length_comment)
        return struct


    def create_entry(self, field, bits):
        """
            @param field: the xml field to create a struct entry from.
            @param bits: the 'num_bits' attr of the <offset> field (e.g. parent of field).
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
        if 'uuid' in field_name and not field_name.endswith('ptr'):
            var_type = 'uuid_t'
            bitfield = -1

        s_entry = fields.CStructEntry(name=field_name,
                                    num_type=props['offset_bits'],
                                    bitfield=bitfield,
                                    var_type=var_type)

        s_entry.origin = field
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

        s_entry = self.split_entry(s_entry)

        return s_entry


    def split_entry(self, entry: fields.CStructEntry, splitbit=64):
        """
            When struct entry bits exceeding offset_bits, the entry needs to be
        splitted in chunks.

        @param: dict or CStructEntry object to be splitted.
        """
        if entry.num_type == -1 or entry.bitfield == None or entry.bitfield == -1:
            #this is not a bitfield entry, so skip it.
            return []
        max_bit = entry.origin.get('max_bit', -1)
        max_bit = int(max_bit)

        min_bit = entry.origin.get('min_bit', -1)
        min_bit = int(min_bit)

        result = []
        bit_overflow = min_bit + entry.bitfield
        if not (min_bit < splitbit and bit_overflow > splitbit):
            return [entry]

        split_bits = []
        split_bits.append(abs(splitbit - entry.bitfield))
        split_bits.append(entry.bitfield - split_bits[0])
        for index in range(len(split_bits)):
            bitfield = split_bits[index]
            name = entry.fields.get('name')
            entry_split = fields.CStructEntry(name=name,
                                                num_type=entry.num_type,
                                                bitfield=entry.bitfield)
            entry_split.name = '%s_%s' % (entry_split.name, index + 1)
            entry_split.definition = entry.definition
            entry_split.bitfield = bitfield
            entry_split.str_end = ' //NOTE: split bit'
            result.append(entry_split)

        return result