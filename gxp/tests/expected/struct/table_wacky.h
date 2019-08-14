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
 *     Generated On : 14, Aug 2019
 *
 *
 * **************************************************************
 *
 * Struct        -----------------------------------  3
 * Struct entries(declared inside structs and enums)  31
 * Unions        -----------------------------------  1
 * Enums         -----------------------------------  1
 */
#ifndef __GENZH__
#define __GENZH__


#ifndef __KERNEL__

#include <stdbool.h>
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

#define TABLE_ENUM_START_INDEX 0x1000

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
    GENZ_COMPONENT_LPD_STRUCTURE = 0x0,
    GENZ_SSDT_MSDT_TABLE = TABLE_ENUM_START_INDEX,
    GENZ_SSDT_MSDT_TABLE_ENTRY_ROW = TABLE_ENUM_START_INDEX + 1
};

struct genz_control_structure_ptr {
    const enum genz_control_ptr_flags ptr_type;
    const enum genz_pointer_size ptr_size;
    const uint32_t pointer_offset;
    const enum genz_control_structure_type struct_type;
};

extern struct genz_control_ptr_info genz_struct_type_to_ptrs[];

extern size_t genz_struct_type_to_ptrs_nelems;

extern struct genz_control_ptr_info genz_table_type_to_ptrs[];

extern size_t genz_table_type_to_ptrs_nelems;


union genz_f_ctl {
    uint16_t val;
    struct {
        uint16_t hwinit_write_enable        : 1;
        uint16_t request_traffic_class      : 4;
        uint16_t r_key_non_interrupt_enable : 1;
        uint16_t pco_enable                 : 1;
        uint16_t lpd_field_type_0_enable    : 1;
        uint16_t lpd_field_type_3_enable    : 1;
        uint16_t lpd_field_type_4_enable    : 1;
        uint16_t rsvdp                      : 5;
        uint64_t padding                    : 1;
    };
};

enum genz_f_ctl_interrupt_r_key_enable {
    F_CTL_INTERRUPT_R_KEY_ENABLE_NO_R_KEY_PRESENT = 0x0,
    F_CTL_INTERRUPT_R_KEY_ENABLE_R_KEY_PRESENT = 0x1
};

struct genz_component_lpd_structure_array {
    uint64_t f_ctl             : 16;
    uint64_t bdf_table_index   : 6;
    uint64_t r3                : 2;
    uint64_t lpd_df_number     : 8;
    uint64_t function_ptr      : 32;
    uint64_t function_ro_r_key : 32;
    uint64_t function_rw_r_key : 32;
};

struct genz_ssdt_msdt_table_array_array { //FIXME: empty struct.

};

struct genz_ssdt_msdt_table_entry_row { //FIXME: empty struct.

};


union genz_control_structure {
    struct genz_control_ptr_info control_ptr_info_ptr;
    struct genz_control_structure_ptr control_structure_ptr_ptr;
    struct genz_component_lpd_structure_array component_lpd_structure_array_ptr;
    struct genz_ssdt_msdt_table_array_array ssdt_msdt_table_array_array_ptr;
    struct genz_ssdt_msdt_table_entry_row ssdt_msdt_table_entry_row_ptr;
};
#endif