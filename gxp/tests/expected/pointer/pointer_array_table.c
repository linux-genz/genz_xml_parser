/*
 * Copyright (C) 2019 Hewlett Packard Enterprise Development LP.
 * All rights reserved.
 *
 * This software is available to you under a choice of one of two
 * licenses.  You may choose to be licensed under the terms of the GNU
 * General Public License (GPL) Version 2, available from the file
 * COPYING in the main directory of this source tree, or the
 * BSD license below:
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/or other materials provided
 *     with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
#include <linux/kernel.h>
#include "pointer_array_table.h"

struct genz_control_structure_ptr component_tr_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x8, GENZ_COMPONENT_TR_TABLE },
};

struct genz_control_structure_ptr opcode_set_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x18, GENZ_OPCODE_SET_UUID_TABLE },
};

struct genz_control_structure_ptr fake_struct_for_testing_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x18, GENZ_COMPONENT_ERROR_ELOG_ENTRY },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x18, GENZ_FAKE_HEADER_TABLE },
};


struct genz_control_ptr_info genz_struct_type_to_ptrs[] = {
    {},
     { opcode_set_structure_ptrs, sizeof(opcode_set_structure_ptrs)/sizeof(opcode_set_structure_ptrs[0]), sizeof(struct genz_opcode_set_structure), false, 0x1, "opcode_set" },
    {},
     { fake_struct_for_testing_ptrs, sizeof(fake_struct_for_testing_ptrs)/sizeof(fake_struct_for_testing_ptrs[0]), sizeof(struct genz_fake_struct_for_testing), false, 0x1, "fake_struct_for_testing_ptrs" },
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
     { component_tr_structure_ptrs, sizeof(component_tr_structure_ptrs)/sizeof(component_tr_structure_ptrs[0]), sizeof(struct genz_component_tr_structure), false, 0x1, "component_tr" },
};

struct genz_control_ptr_info genz_table_type_to_ptrs[] = {
    {},
    {},
    {},
    {},
};

EXPORT_SYMBOL(genz_struct_type_to_ptrs);

size_t genz_struct_type_to_ptrs_nelems = sizeof(genz_struct_type_to_ptrs) / sizeof(genz_struct_type_to_ptrs[0]);

EXPORT_SYMBOL(genz_struct_type_to_ptrs_nelems);

EXPORT_SYMBOL(genz_table_type_to_ptrs);

size_t genz_table_type_to_ptrs_nelems = sizeof(genz_table_type_to_ptrs) / sizeof(genz_table_type_to_ptrs[0]);

EXPORT_SYMBOL(genz_table_type_to_ptrs_nelems);
