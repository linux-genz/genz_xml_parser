from gxp.c_generator import fields


class DataTypesModel:

    # ptr_flags_enum_name = 'genz_control_ptr_type'
    # ptr_size_enum_name = 'genz_pointer_size'

    ctrl_ptr_struct_name = 'genz_control_structure_ptr'
    ctrl_struct_type_enum_name = 'genz_control_structure_type'
    ctrl_ptr_flags_name = 'genz_control_ptr_flags'
    ptr_size_enum_name = 'genz_pointer_size'
    ctr_ptr_info_struct_name = 'genz_control_ptr_info'
    all_structs_union_name = 'genz_control_structure'


    def build_enum(self, name: str, model: dict):
        """
            Creates an enum entry that is needed to for pointer and pointer size
        fields.

        @param name: name for the enum to build the model of.
        @param model: a model to build a enum entries of. It is probably one of
                    the pointer_model.CPointerEntry @staticmethod one.
        """
        enum = fields.CEnumEntry(name)
        for key in model:
            enum.append(model[key])
        return enum


    @classmethod
    def build_ptr_flags_enum(cls):
        """
        enum genz_control_ptr_flags {
            GENZ_CONTROL_POINTER_NONE = 0,
            ...
        };
        """
        return cls.build_enum(cls, cls.ctrl_ptr_flags_name, DataTypesModel.pointer_types())


    @classmethod
    def build_ptr_sizes_enum(cls):
        """
        enum genz_pointer_size {
            GENZ_4_BYTE_POINTER = 4,
            GENZ_6_BYTE_POINTER = 6
        };
        """
        return cls.build_enum(cls, cls.ptr_size_enum_name, DataTypesModel.pointer_sizes())


    @classmethod
    def build_ctrl_struct_ptr_struct(cls):
        """
        struct genz_control_structure_ptr {
            enum genz_control_ptr_flags ptr_type;
            enum genz_pointer_size ptr_size;
            uint32_t pointer_offset;
            enum genz_control_structure_type struct_type;
        };
        """
        struct = fields.CStruct(cls.ctrl_ptr_struct_name)

        entries = [
            fields.CStructEntry('ptr_type', var_type='const enum %s' % cls.ctrl_ptr_flags_name),
            fields.CStructEntry('ptr_size', var_type='const enum %s' % cls.ptr_size_enum_name),
            fields.CStructEntry('pointer_offset', var_type='const uint32_t'),
            fields.CStructEntry('struct_type', var_type='const enum %s' % cls.ctrl_struct_type_enum_name),
        ]

        struct.extend(entries)
        return struct


    @classmethod
    def build_ctrl_ptr_info_struct(cls):
        """
        struct genz_control_ptr_info {
            struct genz_control_structure_ptr *ptr;
            size_t num_ptrs;
            ssize_t struct_bytes;
            uint8_t vers;
            char *name;
        };
        """
        struct = fields.CStruct(cls.ctr_ptr_info_struct_name)

        entries = [
            fields.CStructEntry('* const ptr', var_type='const struct %s' % cls.ctrl_ptr_struct_name),
            fields.CStructEntry('num_ptrs', var_type='const size_t'),
            fields.CStructEntry('struct_bytes', var_type='const ssize_t'),
            fields.CStructEntry('chained', var_type='const bool'), #structure contains chained ptr
            fields.CStructEntry('vers', var_type='const uint8_t'),
            fields.CStructEntry('name', var_type='const char * const'),
        ]

        struct.extend(entries)
        return struct


    @classmethod
    def build_ctrl_struct_type_enum(cls, structs: list, start_index=0):
        """
        enum genz_control_structure_type {
            genz_core_structure = 0,
            genz_opcode_set_structure = 1,
            genz_interface_structure = 2,
            ....
        """
        struct = fields.CEnumEntry(cls.ctrl_struct_type_enum_name)
        generic_entry = fields.EStateEntry('GENZ_GENERIC_STRUCTURE', -1)
        struct.append(generic_entry)

        table_index = 1000
        for index in range(len(structs)):
            s = structs[index]
            value = start_index
            #FIXME: this is stupid! Need to index Table entries to start from 1000
            # while the struct entries index from 0 to whatever.
            if s.tag == 'table':
                value = table_index
                table_index += 1
            else:
                value += index

            entry = fields.EStateEntry(s.name.upper(), value)
            struct.append(entry)
        return struct


    @staticmethod
    def pointer_types():
        return {
            'none' : fields.EStateEntry('GENZ_CONTROL_POINTER_NONE', 0),
            'generic' : fields.EStateEntry('GENZ_CONTROL_POINTER_STRUCTURE', 1),
            'chained' : fields.EStateEntry('GENZ_CONTROL_POINTER_CHAINED', 2),
            'array' : fields.EStateEntry('GENZ_CONTROL_POINTER_ARRAY', 3),
            'table' : fields.EStateEntry('GENZ_CONTROL_POINTER_TABLE', 4),
            'tbl_w_hdr' : fields.EStateEntry('GENZ_CONTROL_POINTER_TABLE_WITH_HEADER', 5),
        }


    @staticmethod
    def pointer_sizes():
        return {
            '4' : fields.EStateEntry('GENZ_4_BYTE_POINTER', 4),
            '6' : fields.EStateEntry('GENZ_6_BYTE_POINTER', 6),
        }


    @classmethod
    def build_externs(cls):
        name = 'genz_ctrl_struct_type_to_ptrs'
        array_type = 'extern struct %s' % cls.ctr_ptr_info_struct_name
        return [
            fields.CArrayEntry(name, array_type, is_allow_empty=False),
            fields.CStructEntry('%s_nelems' % name, var_type='extern size_t', str_left_space='')
        ]