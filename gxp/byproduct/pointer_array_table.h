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

/*
 * This file is automatically generated based of XML GenZ Specs:
 *     Version : 705896
 *     Date    : 2019-06-27 12:58:33
 *
 * Generator Script Meta:
 *     Version      : N/A
 *     Generated On : 08, Aug 2019
 *
 *
 * **************************************************************
 *
 * Struct        -----------------------------------  7
 * Struct entries(declared inside structs and enums)  48
 * Unions        -----------------------------------  0
 * Enums         -----------------------------------  0
 */
#ifndef __GENZH__
#define __GENZH__

#include <stdbool.h>

#ifndef __KERNEL__

#include <stdint.h>
#include <inttypes.h>

#define UUID_SIZE 16
typedef struct {
    unsigned char b[UUID_SIZE];
} uuid_t;

#else

#include <linux/uuid.h>

#endif

struct genz_control_structure_header {
    uint32_t type   : 12;
    uint32_t vers   : 4;
    uint32_t size   : 16;
};

#define TABLE_ENUM_START_INDEX 4096

enum genz_control_ptr_flags {
    GENZ_CONTROL_POINTER_NONE = 0,
    GENZ_CONTROL_POINTER_STRUCTURE = 1,
    GENZ_CONTROL_POINTER_CHAINED = 2,
    GENZ_CONTROL_POINTER_ARRAY = 3,
    GENZ_CONTROL_POINTER_TABLE = 4,
    GENZ_CONTROL_POINTER_TABLE_WITH_HEADER = 5
};

enum genz_pointer_size {
    GENZ_4_BYTE_POINTER = 4,
    GENZ_6_BYTE_POINTER = 6
};

struct genz_control_ptr_info {
    const struct genz_control_structure_ptr * const ptr;
    const size_t num_ptrs;
    const ssize_t struct_bytes;
    const bool chained;
    const uint8_t vers;
    const char * const name;
};

enum genz_control_structure_type {
    GENZ_GENERIC_STRUCTURE = -1,
    GENZ_COMPONENT_TR_STRUCTURE = 0x0,
    GENZ_OPCODE_SET_STRUCTURE = 0x1,
    GENZ_FAKE_STRUCT_FOR_TESTING = 0x2,
    GENZ_COMPONENT_ERROR_ELOG_ENTRY = TABLE_ENUM_START_INDEX,
    GENZ_FAKE_HEADER_TABLE = 0x1001,
    GENZ_OPCODE_SET_UUID_TABLE = 0x1002,
    GENZ_COMPONENT_TR_TABLE = 0x1003
};

struct genz_control_structure_ptr {
    const enum genz_control_ptr_flags ptr_type;
    const enum genz_pointer_size ptr_size;
    const uint32_t pointer_offset;
    const enum genz_control_structure_type struct_type;
};

extern struct genz_control_ptr_info genz_ctrl_struct_type_to_ptrs[];

extern size_t genz_ctrl_struct_type_to_ptrs_nelems;

struct genz_component_tr_table_array {
    uint64_t tr_zmmu : 32;
    uint64_t tr_rtr  : 32;
};

struct genz_opcode_set_uuid_table_array {
    uint64_t supported_vdo_opcode_set_1 : 64;
    uint64_t enabled_vdo_opcode_set_1   : 64;
};

struct genz_fake_header_table_array {
    uint64_t some_entry_1 : 32;
    uint64_t some_entry_2 : 32;
};

struct genz_component_tr_structure {
    uint64_t type         : 12;
    uint64_t vers         : 4;
    uint64_t tr_table_ptr : 32;
};

struct genz_opcode_set_structure {
    uint64_t type              : 12;
    uuid_t opcode_set_uuid_ptr;
};

struct genz_fake_struct_for_testing {
    uint64_t component_error_elog_entry_ptr : 32;
    uint64_t fake_header_table_ptr          : 32;
};

struct genz_component_error_elog_entry {
    uint64_t vers                : 2;
    uint64_t error_code          : 7;
    uint64_t error_specific_11_4 : 64;
};

struct genz_fake_header_table {
    uint64_t supported_p2p_vendor_defined_set                     : 64;
    uint64_t enabled_p2p_vendor_defined_set                       : 64;
    struct genz_fake_header_table_array fake_header_table_array[];
};

struct genz_opcode_set_uuid_table {
    uint64_t supported_p2p_vendor_defined_set                             : 64;
    uint64_t enabled_p2p_vendor_defined_set                               : 64;
    struct genz_opcode_set_uuid_table_array opcode_set_uuid_table_array[];
};


union genz_control_structure {
    struct genz_control_ptr_info control_ptr_info_ptr;
    struct genz_control_structure_ptr control_structure_ptr_ptr;
    struct genz_component_tr_table_array component_tr_table_array_ptr;
    struct genz_opcode_set_uuid_table_array opcode_set_uuid_table_array_ptr;
    struct genz_fake_header_table_array fake_header_table_array_ptr;
    struct genz_component_tr_structure component_tr_structure_ptr;
    struct genz_opcode_set_structure opcode_set_structure_ptr;
    struct genz_fake_struct_for_testing fake_struct_for_testing_ptr;
    struct genz_component_error_elog_entry component_error_elog_entry_ptr;
    struct genz_fake_header_table fake_header_table_ptr;
    struct genz_opcode_set_uuid_table opcode_set_uuid_table_ptr;
};
#endif