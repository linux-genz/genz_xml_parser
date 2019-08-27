"""
TODO: real docs here
"""

import datetime
import math
import os
import xml.etree.ElementTree
import jinja2
import logging

from pdb import set_trace

from gxp.generator import parsers
from gxp.generator import fields
from gxp.generator.models import DataTypesModel
from gxp.generator.utils import get_name, is_name_too_long, trim_name


class CGenerator:
    """
        Loops through the XML fields of a specific format:
        <structs> -> <struct> -> <offset> -> <field> -> <subfield [optionl]>.
        Look for example inside this project/mock/ folder.
    """

    def __init__(self, root: list, parse_on_init=True, tags: dict={}, name=None, **kwargs):
        self.context = root
        self.name = name

        self.structs = []
        self.pointers = []
        self.enums = []
        self.unions = []
        self.struct_arrays = []

        self.DataTypes = kwargs.get('model', DataTypesModel)
        self.struct_type_start_index = kwargs.get('struct_type_start_index', 0)
        self.root_tag_name = tags.get('root', 'structs')
        self.struct_tag_name = tags.get('struct', 'struct')
        self.struct_type_to_ptrs_name = 'genz_struct_type_to_ptrs'
        self.table_type_to_ptrs_name = 'genz_table_type_to_ptrs'

        root_structs = root.find(self.root_tag_name)
        if parse_on_init:
            self.parse_xml(root_structs)


    def parse_xml(self, context):
        """
        @param context: xml tree. A root to start iterating through subfields of.
        @param subfields: fields to loop through, where each next element in this
                        list is a child of the previous.  Default: [ 'offest',
                        'field', 'subfield']-> 'field' searched in the 'offset'.
        """
        if context is None:
            return

        xml_structs = context.findall(self.struct_tag_name)
        self._parse_structs(xml_structs)


    def _parse_structs(self, xml_structs):
        for struct_elem in xml_structs:
            struct_parser = parsers.StructBuilder(struct_elem)
            if struct_parser.instance not in self.structs: #duplicates check
                self.structs.append(struct_parser.instance)

            union_builder = parsers.UnionBuilder(struct_elem)
            if union_builder is not None and union_builder.instance is not None:
                self.unions.extend(union_builder.instance)

            enum_builder = parsers.EnumBuilder(struct_elem)
            if enum_builder.instance is not None and len(enum_builder.instance) > 0:
                for enum in enum_builder.instance: #duplicates check
                    if enum not in self.enums:
                        self.enums.append(enum)

            pointer_parser = parsers.PointerBuilder(struct_elem, data_types=self.DataTypes)
            if pointer_parser.instance is not None:
                if pointer_parser.instance not in self.pointers:
                    pointer_parser.instance.origin = struct_parser.instance
                    if pointer_parser.instance not in self.pointers: #duplicates check
                        self.pointers.append(pointer_parser.instance)
                struct_parser.instance.child_pointers.extend(pointer_parser.instance.entries)

            #Parsing a table is almost a recursive process. Each <table> or
            #<array> entry has almost the same structure as <struct> entry.
            table_parser = parsers.TableBuilder(struct_elem)
            if table_parser.instance is not None:
                for cgen in table_parser.instance:
                    for t_struct in cgen.structs:
                        table_entry_name = 'struct %s' % t_struct.name
                        struct_entry = fields.CStructEntry(
                                            cgen.structs[0].name.lstrip('genz_') + '[]',
                                            var_type=table_entry_name)

                        #Adding created Table entry to the current struct_parser
                        #entries list
                        if not struct_entry in struct_parser.instance.entries:
                            struct_parser.instance.append(struct_entry)

                        #loop through table's structs and only add those that are
                        #not already in the main structs list.
                        # These are the struct generated from <array> fields.
                        target = []
                        target.extend(cgen.structs)
                        for ms in target:
                            if ms not in self.struct_arrays:
                                self.struct_arrays.insert(0, ms)

                        struct_parser.instance.child_arrays.extend(cgen.structs)

                        self._add_to_list(cgen.unions, self.unions)
                        self._add_to_list(cgen.enums, self.enums)
                        self._add_to_list(cgen.pointers, self.pointers)
                        self._add_to_list(cgen.struct_arrays, self.struct_arrays, is_push_front=True)


    def merge(self, generator):
        """
            Merge each entry types (EXCEPT "structs") from other CGenerator object
        into this one. Ignoring "structs" merging, because it is more often than not
        doesn't mean what you think it means. For example, in one case "self.structs"
        are the collection of <struct> entries, in other - its <table>.

        @param generator: a CGenerator kind of object to merge entries from.
        """
        self._add_to_list(generator.unions, self.unions)
        self._add_to_list(generator.enums, self.enums)
        self._add_to_list(generator.pointers, self.pointers)
        self._add_to_list(generator.struct_arrays, self.struct_arrays)
        # self._add_to_list(generator.structs, self.structs)


    def _add_to_list(self, what_to_add, list_to_add_to, is_push_front=False):
        target = []
        target.extend(what_to_add)
        for t in target:
            if t not in list_to_add_to:
                if not is_push_front:
                    list_to_add_to.append(t)
                else:
                    list_to_add_to.insert(0,t)


    def update_pointers(self):
        """
            After every field of the xml is parsed, we need to figure out each
        pointers' (xml fields with "ptr_to" attr) type (generic, chained, table
        and etc. Refer to models.py).
        """
        ptr_types = self.DataTypes.pointer_types()
        result = []
        struct_ptr_enum = self.structs_enum
        for pointer_array in self.pointers:
            for pointer in pointer_array.entries:
                if pointer in result:
                    continue
                if pointer.ptr_to is None:
                    continue

                if pointer.ptr_to.lower() == 'generic structure':
                    pointer.p_type = struct_ptr_enum.entries[0].name
                    pointer.p_flag = ptr_types['generic'].name
                else:
                    #Handle none generic flag
                    is_chained = self._handle_ptr_chain(pointer)
                    if not is_chained:
                        self._handle_ptr_tables(pointer)

                #Find and set a stuct's ENUM type for the pointer
                p_type = self.find_struct_enum_by_name(pointer.ptr_to)
                if p_type is None:  #PARANOIA
                    logging.warning('Ptr "%s" -- ptr_to --> "%s" found no enum struct!' %\
                                (pointer.name, pointer.ptr_to))
                    p_type = struct_ptr_enum.entries[0]
                pointer.p_type = p_type.name

                if pointer.p_flag is None:
                    pointer.p_flag = ptr_types['none'].name

                    msg = '%s pointer flag type not set! Defaulting to %s'
                    logging.warning(msg % (pointer.name, pointer.p_flag))

                if pointer.p_type is None:
                    pointer.p_type = struct_ptr_enum.entries[0].name

                if pointer not in result:
                    result.append(pointer)
        return result


    def _handle_ptr_chain(self, pointer):
        """
        If its pointing to a Struct, then keep following the pointer to find a enum
        value from that big table of Struct names which is Second or whatever value
        in the C array entries. Look up every pointer in the struct it points to.
        If none points to its own struct - then it is a POINTER_STRUCTURE type.

        Looked for a Struct or Table - look up the structure and look inside it
        and its pointers, the First pointer is Start.

        Every next point (technically the last one referencing itself) is Chained.
        """
        logging.debug('%s -> _handle_ptr_chain:\n pointer "%s" arrived.' % \
                        (os.path.basename(__file__), pointer.name))

        ptr_types = self.DataTypes.pointer_types()
        ptr_name = 'genz_%s' % trim_name(pointer.ptr_to)
        struct = self.find_struct_by_name(ptr_name)
        if struct is None:
            return False

        p_flag_to_set = None

        for struct_ptr in struct.child_pointers:
            ptr_to_name = 'genz_%s' % trim_name(struct_ptr.ptr_to)
            if struct.name == ptr_to_name:
                p_flag_to_set = ptr_types['generic'].name
            if struct_ptr == pointer:
                p_flag_to_set = ptr_types['chained'].name
                struct.is_chained = True

        if p_flag_to_set is not None:
            pointer.p_flag = p_flag_to_set

        logging.debug('%s is a %s\n-----\n' % (pointer.name, p_flag_to_set))
        return p_flag_to_set is not None


    def _handle_ptr_tables(self, pointer) -> bool:
        """
        "GENZ_CONTROL_POINTER_ARRAY" - "ptr_to" points to a thing that is a Table
        and it has an array that is THE ONLY thing in the table.

        "GENZ_CONTROL_POINTER_TABLE" - points to a table and it just the offsets
        or offsets with arrays that are not "Variable" type. (e.g 'elements' attr
        of the array is not "Variable").

        "GENZ_CONTROL_POINTER_TABLE_WITH_HEADER" - points to a table that has offsets
        with the array of type "Variable".
        """
        logging.debug('%s -> _handle_ptr_tables:\n pointer "%s" arrived.' % \
                (os.path.basename(__file__), pointer.name))
        ptr_flags = self.DataTypes.pointer_types()
        ptr_name = 'genz_%s' % trim_name(pointer.ptr_to)
        struct = self.find_struct_by_name(ptr_name)
        if struct is None:
            return False

        if struct.origin is None:
            return False

        ptr_flag_to_set = None

        arrays = struct.origin.findall('array')
        offsets = struct.origin.findall('offset')
        # probably a GENZ_CONTROL_POINTER_ARRAY, as long as the only element is
        # an <array> and nothing else
        if arrays is not None and len(arrays) > 0:
            if len(struct.origin) == 1:
                ptr_flag_to_set = ptr_flags['array']

        if len(offsets) > 0:
            #GENZ_CONTROL_POINTER_TABLE if not a "Variable" array
            if not self._has_variable_array(arrays):
                ptr_flag_to_set = ptr_flags['table']
            else:
                # GENZ_CONTROL_POINTER_TABLE_WITH_HEADER
                if len(arrays) > 0:
                    ptr_flag_to_set = ptr_flags['tbl_w_hdr']

        if ptr_flag_to_set is not None:
            pointer.p_flag = ptr_flag_to_set.name

        return ptr_flag_to_set is not None


    def _has_variable_array(self, arrays) -> bool:
        """
            Return True if at least one array in the list has "Elements"="Variable".
        Return False otherwise.

            @param arrays: list of xml field <array>.
        """
        for array in arrays:
            if array.get('elements', '').lower() == 'variable':
                return True
        return False


    def find_struct_by_name(self, target_name, target_struct=None):
        if target_struct is None:
            target_struct = self.structs
        for struct in target_struct:
            if struct.name == target_name:
                return struct
        return None


    def find_struct_enum_by_name(self, target_name):
        struct_ptr_enum = self.structs_enum
        target_name = trim_name('genz_%s' % target_name.lower())
        for enum_entry in struct_ptr_enum.entries:
            if enum_entry.name.lower() == target_name:
                return enum_entry
        return None


    def find_enum_value_by_name(self, target_name, enum_obj):
        for entry in enum_obj.entries:
            if target_name == entry.name:
                return entry
        return None


    def find_highest_struct_index(self, tag='struct'):
        """
            Loop through self.structs and return its highest .index value.

            @param tag: the tag names to search for the index of.
        """
        hIndex = -1
        for struct in self.structs:
            if struct.tag not in tag:
                continue
            index = struct.index
            if index is None or index == -1:
                index = hIndex + 1
            if isinstance(index, str):
                index = int(index, 0)
            if index > hIndex:
                hIndex = index
        return hIndex


    def build_control_ptr_info_array(self):
        """
         This is a list of all the <struct>.
         Index by <struct> "type" number. There could be "gaps" in the type index -
        so add "null" entry and move on.

        Same thing should be created for <table>, except no need to have gaps.
        Assign index as you go.
        """
        array_type = self.DataTypes.ctr_ptr_info_struct_name
        array_name = 'genz_struct_type_to_ptrs'
        table_name = 'genz_table_type_to_ptrs'
        struct_array = fields.CArrayEntry(array_name, 'struct %s' % array_type)
        table_array = fields.CArrayEntry(table_name, 'struct %s' % array_type)
        pointers_count = len(self.pointers)

        #Need to know how big the pointers list is going to be, based of the
        #struct's highest "type" attribut's value which indicates its position
        #in the array that is built here.
        hIndex_struct = self.find_highest_struct_index()
        hIndex_tbl = self.find_highest_struct_index(tag='table')
        for _ in range(hIndex_struct + 1):
            null_entry = fields.NullEntry(close_bracket=',')
            struct_array.append(null_entry)

        struct_enum = self.structs_enum
        for _ in range(hIndex_tbl + 1):
            null_entry = fields.NullEntry(close_bracket=',')
            table_array.append(null_entry)

        for index in range(pointers_count):
            ptr = self.pointers[index]
            struct = ptr.origin
            if struct.tag not in ['struct', 'table']:
                continue

            if struct.index is None:
                msg = 'NOOOOOOO!! No "type" attr in struct -> %s' % struct.name
                logging.critical(msg)

            if not isinstance(struct, fields.cstruct.CStruct):
                msg = 'Pointer "%s" origin is not of type CStruct!' % ptr.name
                logging.critical(msg)
                continue

            if struct.origin is None:
                logging.critical('Pointer "%s" struct "%s" origin is None?!' %\
                                (ptr.name, struct.name))
                continue

            name_no_ptr = ptr.name.split('_ptrs')[0]
            name_no_genz = ptr.name.lstrip('genz_').split('_structure')[0]

            ptr_size = 'sizeof({name})/sizeof({name}[0])'.format(name=ptr.name)
            ptr_offset = 'sizeof(struct genz_{name})'.format(name=name_no_ptr)

            name = '{ptype}, {size}, {offset}, {chained}, {vers}, "{stype}"'.format(
                ptype=ptr.name,
                size=ptr_size,
                offset=ptr_offset,
                vers=struct.vers if struct.vers is not None else '0x0',
                stype=name_no_genz,
                chained='true' if struct.is_chained else 'false'
            )
            struct_entry = fields.CStructEntry(name, ignore_long_name_warning=True)
            struct_entry.l_space = '%s { ' % struct_entry.l_space
            struct_entry.str_close_symbol = ' },'

            if struct.tag == 'struct':
                struct_array.entries[int(struct.index, 0)] = struct_entry
            elif struct.tag == 'table':
                enum = self.find_enum_value_by_name(struct.name.upper(),
                                                    struct_enum)
                enum_val = enum.value.split('+')[-1].strip()
                if enum_val.isdigit(): enum_val = int(enum_val, 0)
                else: enum_val = 0
                table_array.entries[enum_val] = struct_entry

        return struct_array, table_array


    def build_export_symbol(self, name):
        """
            EXPORT_SYMBOL(genz_struct_type_to_ptrs);

            size_t genz_struct_type_to_ptrs_nelems =
                sizeof(genz_struct_type_to_ptrs) /
                sizeof(genz_struct_type_to_ptrs[0]);

            EXPORT_SYMBOL(genz_struct_type_to_ptrs);
        """
        export_symbol = 'EXPORT_SYMBOL(%s)'
        value = 'sizeof({name}) / sizeof({name}[0])'.format(name=name)
        return [
            fields.CStructEntry(export_symbol % name, var_type='', l_space=''),
            fields.EStateEntry('size_t %s_nelems' % name, value, l_space='', close_bracket=';'),
            fields.CStructEntry(export_symbol % (name + '_nelems'), var_type='', l_space=''),
        ]


    @property
    def export_symbol_struct(self):
        return self.build_export_symbol(self.struct_type_to_ptrs_name)


    @property
    def export_symbol_table(self):
        return self.build_export_symbol(self.table_type_to_ptrs_name)


    @property
    def structs_enum(self):
        return self.DataTypes.build_ctrl_struct_type_enum(self.structs,
                                                    self.struct_type_start_index)


    @property
    def structs_enum(self):
        """
            Build and return an Enum of all the struct names as entries.
        """
        #Note to self: this is awful! I don't like the "dynamic" building of this,
        #cause it has to loop through each struct entry every time this property
        #is called. Madeness. By convenient...
        return self.DataTypes.build_ctrl_struct_type_enum(self.structs,
                                                    self.struct_type_start_index)


    @property
    def table_structs(self):
        """
            Return a list of <table> type struct entries from the self.structs
        collection.
        """
        result = []
        for entry in self.structs:
            if entry.tag is None:
                continue
            if entry.tag == 'table':
                result.append(entry)
        return result


    @property
    def entries(self):
        result = []
        result.append(self.DataTypes.table_index_define())

        ctrl_ptr_flags = self.DataTypes.build_ptr_flags_enum()
        ptr_sizes = self.DataTypes.build_ptr_sizes_enum()
        ctrl_ptr_struct = self.DataTypes.build_ctrl_struct_ptr_struct()
        ctrl_ptr_info_struct = self.DataTypes.build_ctrl_ptr_info_struct()
        externs = self.DataTypes.build_externs(self.struct_type_to_ptrs_name)
        externs.extend(self.DataTypes.build_externs(self.table_type_to_ptrs_name))


        result.append(ctrl_ptr_flags)
        result.append(ptr_sizes)
        result.append(ctrl_ptr_info_struct)
        result.append(self.structs_enum)
        result.append(ctrl_ptr_struct)
        result.extend(externs)

        # Order of adding things Matters for C file to compile.
        for union in self.unions:
            result.append(union)

        for enum in self.enums:
            if len(enum.entries) > 1:
                result.append(enum)

        structs = []
        structs.extend(self.struct_arrays)
        structs.extend(self.structs)
        for struct in structs:
            if len(struct.entries) == 1:
                if '[]' in struct.entries[0].name:
                    continue
            result.append(struct)

        return result