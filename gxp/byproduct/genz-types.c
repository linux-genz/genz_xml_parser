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
#include "genz-types.h"

struct hardware_classes_meta hardware_classes[] = {
     {  "Reserved—shall not be used",                           "reserved_shall_not_be_used", RESERVED_SHALL_NOT_BE_USED },
     {  "Memory ( P2P 64 )",                                    "memory", MEMORY },
     {  "Memory (Explicit OpClass)",                            "memory", MEMORY },
     {  "Integrated Switch",                                    "switch", SWITCH },
     {  "Enclosure / Expansion Switch",                         "switch", SWITCH },
     {  "Fabric Switch",                                        "switch", SWITCH },
     {  "Processor (Bootable)",                                 "processor", PROCESSOR },
     {  "Processor (Non-boot)",                                 "processor", PROCESSOR },
     {  "Accelerator (Non-coherent, non-boot)",                 "accelerator", ACCELERATOR },
     {  "Accelerator (Coherent, non-boot)",                     "accelerator", ACCELERATOR },
     {  "Accelerator (Non-coherent, bootable)",                 "accelerator", ACCELERATOR },
     {  "Accelerator (Coherent, bootable)",                     "accelerator", ACCELERATOR },
     {  "I/O (Non-coherent, non-boot)",                         "io", IO },
     {  "I/O (Coherent, non-boot)",                             "io", IO },
     {  "I/O (Non-coherent, bootable)",                         "io", IO },
     {  "I/O (Coherent, bootable)",                             "io", IO },
     {  "Block Storage (Bootable)",                             "block_storage", BLOCK_STORAGE },
     {  "Block Storage (Non-boot)",                             "block_storage", BLOCK_STORAGE },
     {  "Transparent Router",                                   "transparent_router", TRANSPARENT_ROUTER },
     {  "Multi-class Component (see  Service UUID Structure )", "multiclass_component", MULTICLASS_COMPONENT },
     {  "Discrete Gen-Z Bridge",                                "bridge", BRIDGE },
     {  "Integrated Gen-Z Bridge",                              "bridge", BRIDGE },
     {  "Compliance Test Board",                                "compliance_test_board", COMPLIANCE_TEST_BOARD },
     {  "Logical PCIe Hierarchy (LPH)",                         "logical_pcie_hierarchy", LOGICAL_PCIE_HIERARCHY },
};

struct genz_control_structure_ptr core_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x48, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x4c, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x50, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x54, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x58, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x5c, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x60, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x64, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x68, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x6c, GENZ_CORE_LPD_BDF_TABLE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x70, GENZ_OPCODE_SET_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x74, GENZ_COMPONENT_C_ACCESS_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x78, GENZ_COMPONENT_DESTINATION_TABLE_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x7c, GENZ_INTERFACE_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x80, GENZ_COMPONENT_EXTENSION_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x84, GENZ_COMPONENT_ERROR_AND_SIGNAL_EVENT_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x130, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x134, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x138, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x13c, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_6_BYTE_POINTER, 0x140, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_6_BYTE_POINTER, 0x146, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x14c, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr opcode_set_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x18, GENZ_OPCODE_SET_UUID_TABLE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x1c, GENZ_OPCODE_SET_TABLE },
};

struct genz_control_structure_ptr interface_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x70, GENZ_INTERFACE_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x78, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x7c, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x80, GENZ_INTERFACE_PHY_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x84, GENZ_INTERFACE_STATISTICS_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x88, GENZ_COMPONENT_MECHANICAL_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x8c, GENZ_VENDOR_DEFINED_STRUCTURE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x90, GENZ_VCAT_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x94, GENZ_LPRT_MPRT_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x98, GENZ_LPRT_MPRT_TABLE },
};

struct genz_control_structure_ptr interface_phy_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x8, GENZ_INTERFACE_PHY_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0xc, GENZ_VENDOR_DEFINED_STRUCTURE },
};

struct genz_control_structure_ptr interface_statistics_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x8, GENZ_VENDOR_DEFINED_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0xc, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr component_error_and_signal_event_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x14, GENZ_ELOG_TABLE },
};

struct genz_control_structure_ptr component_media_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x4, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0xc, GENZ_COMPONENT_MEDIA_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x74, GENZ_BACKUP_MGMT_TABLE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x78, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x7c, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x80, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x84, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x88, GENZ_MEDIA_LOG_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x8c, GENZ_MEDIA_LOG_TABLE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x90, GENZ_OEM_DATA_TABLE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x94, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x98, GENZ_LABEL_DATA_TABLE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x9c, GENZ_LABEL_DATA_TABLE },
};

struct genz_control_structure_ptr component_switch_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x30, GENZ_MVCAT_TABLE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x34, GENZ_ROUTE_CONTROL_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x38, GENZ_MCPRT_MSMCPRT_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x3c, GENZ_MCPRT_MSMCPRT_TABLE },
};

struct genz_control_structure_ptr component_statistics_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x8, GENZ_COMPONENT_STATISTICS_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0xc, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr component_extension_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x4, GENZ_COMPONENT_EXTENSION_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x8, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0xc, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x10, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x14, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x18, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x1c, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x20, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x24, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x28, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_4_BYTE_POINTER, 0x2c, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_6_BYTE_POINTER, 0x30, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_STRUCTURE, GENZ_6_BYTE_POINTER, 0x38, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr component_multicast_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x1c, GENZ_UNRELIABLE_MULTICAST_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x20, GENZ_UNRELIABLE_MULTICAST_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x24, GENZ_RELIABLE_MULTICAST_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x28, GENZ_RELIABLE_MULTICAST_TABLE },
};

struct genz_control_structure_ptr component_security_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x18, GENZ_C_CERT_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x1c, GENZ_CERTIFICATE_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x20, GENZ_TIK_TABLE },
};

struct genz_control_structure_ptr component_tr_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x8, GENZ_COMPONENT_TR_TABLE },
};

struct genz_control_structure_ptr component_image_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_6_BYTE_POINTER, 0x10, GENZ_IMAGE_TABLE },
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x18, GENZ_COMPONENT_IMAGE_STRUCTURE },
};

struct genz_control_structure_ptr component_precision_time_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x1c, GENZ_COMPONENT_PRECISION_TIME_STRUCTURE },
};

struct genz_control_structure_ptr component_mechanical_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x1c, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
};

struct genz_control_structure_ptr component_destination_table_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x1c, GENZ_ROUTE_CONTROL_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x20, GENZ_SSDT_MSDT_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x24, GENZ_SSDT_MSDT_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x28, GENZ_REQUESTER_VCAT_TABLE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x2c, GENZ_RIT_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x30, GENZ_RESPONDER_VCAT_TABLE },
};

struct genz_control_structure_ptr service_uuid_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x8, GENZ_SERVICE_UUID_TABLE },
};

struct genz_control_structure_ptr component_c_access_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x4, GENZ_COMPONENT_C_ACCESS_STRUCTURE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x18, GENZ_C_ACCESS_R_KEY_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x1c, GENZ_C_ACCESS_L_P2P_TABLE },
};

struct genz_control_structure_ptr requester_p2p_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x38, GENZ_REQUESTER_P2P_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x3c, GENZ_VENDOR_DEFINED_STRUCTURE },
};

struct genz_control_structure_ptr component_pa_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x1c, GENZ_PA_TABLE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x20, GENZ_SSAP_MCAP_MSAP_AND_MSMCAP_TABLE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x24, GENZ_SSAP_MCAP_MSAP_AND_MSMCAP_TABLE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x28, GENZ_SSAP_MCAP_MSAP_AND_MSMCAP_TABLE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x2c, GENZ_SSAP_MCAP_MSAP_AND_MSMCAP_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x34, GENZ_SEC_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x48, GENZ_CERTIFICATE_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x4c, GENZ_TIK_TABLE },
};

struct genz_control_structure_ptr component_lpd_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x4, GENZ_COMPONENT_LPD_STRUCTURE },
};

struct genz_control_structure_ptr component_lpd_structure_array_ptrs[] = {
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x54, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr component_sod_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x14, GENZ_SSOD_TABLE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x18, GENZ_MSOD_TABLE },
};

struct genz_control_structure_ptr congestion_management_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x8, GENZ_VENDOR_DEFINED_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0xc, GENZ_RESOURCE_ARRAY_TABLE },
};

struct genz_control_structure_ptr component_pm_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x8, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr component_re_table_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_6_BYTE_POINTER, 0x10, GENZ_RE_TABLE },
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_6_BYTE_POINTER, 0x18, GENZ_COMPONENT_RE_TABLE_STRUCTURE },
};

struct genz_control_structure_ptr component_lph_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x4, GENZ_COMPONENT_LPH_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x54, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x60, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr component_page_grid_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x18, GENZ_PG_RESTRICTED_PG_TABLE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x1c, GENZ_PTE_RESTRICTED_PTE_TABLE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x20, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x24, GENZ_COMPONENT_PAGE_GRID_STRUCTURE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x28, GENZ_PG_RESTRICTED_PG_TABLE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x2c, GENZ_PTE_RESTRICTED_PTE_TABLE },
};

struct genz_control_structure_ptr component_page_table_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x4, GENZ_VENDOR_DEFINED_WITH_UUID_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x18, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x1c, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x34, GENZ_COMPONENT_PAGE_TABLE_STRUCTURE },
};

struct genz_control_structure_ptr component_interleave_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x4, GENZ_COMPONENT_INTERLEAVE_STRUCTURE },
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x20, GENZ_TYPE_1_INTERLEAVE_TABLE },
};

struct genz_control_structure_ptr component_firmware_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_ARRAY, GENZ_4_BYTE_POINTER, 0x8, GENZ_FIRMWARE_TABLE },
};

struct genz_control_structure_ptr component_sw_management_structure_ptrs[] = {
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x18, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr component_tr_table_array_ptrs[] = {
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x0, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x4, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_TABLE, GENZ_4_BYTE_POINTER, 0x10, GENZ_OPCODE_SET_STRUCTURE },
};

struct genz_control_structure_ptr c_cert_table_array_ptrs[] = {
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x0, GENZ_GENERIC_STRUCTURE },
    { GENZ_CONTROL_POINTER_NONE, GENZ_4_BYTE_POINTER, 0x4, GENZ_GENERIC_STRUCTURE },
};

struct genz_control_structure_ptr opcode_set_table_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x4, GENZ_OPCODE_SET_TABLE },
};

struct genz_control_structure_ptr elog_table_ptrs[] = {
    { GENZ_CONTROL_POINTER_CHAINED, GENZ_4_BYTE_POINTER, 0x4, GENZ_ELOG_TABLE },
};

struct genz_control_structure_ptr backup_mgmt_table_ptrs[] = {
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x68, GENZ_PM_BACKUP_TABLE },
    { GENZ_CONTROL_POINTER_TABLE_WITH_HEADER, GENZ_4_BYTE_POINTER, 0x6c, GENZ_SM_BACKUP_TABLE },
};


struct genz_control_ptr_info genz_struct_type_to_ptrs[] = {
     {  genz_core_structure, sizeof(genz_core_structure)/sizeof(genz_core_structure[0]), sizeof(struct genz_genz_core_structure), false, 0x1, "core" },
     {  genz_opcode_set_structure, sizeof(genz_opcode_set_structure)/sizeof(genz_opcode_set_structure[0]), sizeof(struct genz_genz_opcode_set_structure), false, 0x1, "opcode_set" },
     {  genz_interface_structure, sizeof(genz_interface_structure)/sizeof(genz_interface_structure[0]), sizeof(struct genz_genz_interface_structure), true, 0x1, "interface" },
     {  genz_interface_phy_structure, sizeof(genz_interface_phy_structure)/sizeof(genz_interface_phy_structure[0]), sizeof(struct genz_genz_interface_phy_structure), true, 0x1, "interface_phy" },
     {  genz_interface_statistics_structure, sizeof(genz_interface_statistics_structure)/sizeof(genz_interface_statistics_structure[0]), sizeof(struct genz_genz_interface_statistics_structure), false, 0x1, "interface_statistics" },
     {  genz_component_error_and_signal_event_structure, sizeof(genz_component_error_and_signal_event_structure)/sizeof(genz_component_error_and_signal_event_structure[0]), sizeof(struct genz_genz_component_error_and_signal_event_structure), false, 0x1, "component_error_and_signal_event" },
     {  genz_component_media_structure, sizeof(genz_component_media_structure)/sizeof(genz_component_media_structure[0]), sizeof(struct genz_genz_component_media_structure), true, 0x1, "component_media" },
     {  genz_component_switch_structure, sizeof(genz_component_switch_structure)/sizeof(genz_component_switch_structure[0]), sizeof(struct genz_genz_component_switch_structure), false, 0x1, "component_switch" },
     {  genz_component_statistics_structure, sizeof(genz_component_statistics_structure)/sizeof(genz_component_statistics_structure[0]), sizeof(struct genz_genz_component_statistics_structure), true, 0x1, "component_statistics" },
     {  genz_component_extension_structure, sizeof(genz_component_extension_structure)/sizeof(genz_component_extension_structure[0]), sizeof(struct genz_genz_component_extension_structure), true, 0x1, "component_extension" },
     {  genz_vendor_defined_structure, sizeof(genz_vendor_defined_structure)/sizeof(genz_vendor_defined_structure[0]), sizeof(struct genz_genz_vendor_defined_structure), false, 0x1, "vendor_defined" },
     {  genz_vendor_defined_with_uuid_structure, sizeof(genz_vendor_defined_with_uuid_structure)/sizeof(genz_vendor_defined_with_uuid_structure[0]), sizeof(struct genz_genz_vendor_defined_with_uuid_structure), false, 0x1, "vendor_defined_with_uuid" },
     {  genz_component_multicast_structure, sizeof(genz_component_multicast_structure)/sizeof(genz_component_multicast_structure[0]), sizeof(struct genz_genz_component_multicast_structure), false, 0x1, "component_multicast" },
     {  genz_component_security_structure, sizeof(genz_component_security_structure)/sizeof(genz_component_security_structure[0]), sizeof(struct genz_genz_component_security_structure), false, 0x1, "component_security" },
     {  genz_component_tr_structure, sizeof(genz_component_tr_structure)/sizeof(genz_component_tr_structure[0]), sizeof(struct genz_genz_component_tr_structure), false, 0x1, "component_tr" },
     {  genz_component_image_structure, sizeof(genz_component_image_structure)/sizeof(genz_component_image_structure[0]), sizeof(struct genz_genz_component_image_structure), true, 0x1, "component_image" },
     {  genz_component_precision_time_structure, sizeof(genz_component_precision_time_structure)/sizeof(genz_component_precision_time_structure[0]), sizeof(struct genz_genz_component_precision_time_structure), true, 0x1, "component_precision_time" },
     {  genz_component_mechanical_structure, sizeof(genz_component_mechanical_structure)/sizeof(genz_component_mechanical_structure[0]), sizeof(struct genz_genz_component_mechanical_structure), false, 0x1, "component_mechanical" },
     {  genz_component_destination_table_structure, sizeof(genz_component_destination_table_structure)/sizeof(genz_component_destination_table_structure[0]), sizeof(struct genz_genz_component_destination_table_structure), false, 0x1, "component_destination_table" },
     {  genz_service_uuid_structure, sizeof(genz_service_uuid_structure)/sizeof(genz_service_uuid_structure[0]), sizeof(struct genz_genz_service_uuid_structure), false, 0x1, "service_uuid" },
     {  genz_component_c_access_structure, sizeof(genz_component_c_access_structure)/sizeof(genz_component_c_access_structure[0]), sizeof(struct genz_genz_component_c_access_structure), true, 0x1, "component_c_access" },
     {  genz_requester_p2p_structure, sizeof(genz_requester_p2p_structure)/sizeof(genz_requester_p2p_structure[0]), sizeof(struct genz_genz_requester_p2p_structure), true, 0x1, "requester_p2p" },
     {  genz_component_pa_structure, sizeof(genz_component_pa_structure)/sizeof(genz_component_pa_structure[0]), sizeof(struct genz_genz_component_pa_structure), false, 0x1, "component_pa" },
     {  genz_component_event_structure, sizeof(genz_component_event_structure)/sizeof(genz_component_event_structure[0]), sizeof(struct genz_genz_component_event_structure), false, 0x1, "component_event" },
     {  genz_component_lpd_structure, sizeof(genz_component_lpd_structure)/sizeof(genz_component_lpd_structure[0]), sizeof(struct genz_genz_component_lpd_structure), true, 0x1, "component_lpd" },
     {  genz_component_sod_structure, sizeof(genz_component_sod_structure)/sizeof(genz_component_sod_structure[0]), sizeof(struct genz_genz_component_sod_structure), false, 0x1, "component_sod" },
     {  genz_congestion_management_structure, sizeof(genz_congestion_management_structure)/sizeof(genz_congestion_management_structure[0]), sizeof(struct genz_genz_congestion_management_structure), false, 0x1, "congestion_management" },
     {  genz_component_rkd_structure, sizeof(genz_component_rkd_structure)/sizeof(genz_component_rkd_structure[0]), sizeof(struct genz_genz_component_rkd_structure), false, 0x1, "component_rkd" },
     {  genz_component_pm_structure, sizeof(genz_component_pm_structure)/sizeof(genz_component_pm_structure[0]), sizeof(struct genz_genz_component_pm_structure), false, 0x1, "component_pm" },
     {  genz_component_atp_structure, sizeof(genz_component_atp_structure)/sizeof(genz_component_atp_structure[0]), sizeof(struct genz_genz_component_atp_structure), false, 0x1, "component_atp" },
     {  genz_component_re_table_structure, sizeof(genz_component_re_table_structure)/sizeof(genz_component_re_table_structure[0]), sizeof(struct genz_genz_component_re_table_structure), true, 0x1, "component_re_table" },
     {  genz_component_lph_structure, sizeof(genz_component_lph_structure)/sizeof(genz_component_lph_structure[0]), sizeof(struct genz_genz_component_lph_structure), true, 0x1, "component_lph" },
     {  genz_component_page_grid_structure, sizeof(genz_component_page_grid_structure)/sizeof(genz_component_page_grid_structure[0]), sizeof(struct genz_genz_component_page_grid_structure), true, 0x1, "component_page_grid" },
     {  genz_component_page_table_structure, sizeof(genz_component_page_table_structure)/sizeof(genz_component_page_table_structure[0]), sizeof(struct genz_genz_component_page_table_structure), true, 0x1, "component_page_table" },
     {  genz_component_interleave_structure, sizeof(genz_component_interleave_structure)/sizeof(genz_component_interleave_structure[0]), sizeof(struct genz_genz_component_interleave_structure), true, 0x1, "component_interleave" },
     {  genz_component_firmware_structure, sizeof(genz_component_firmware_structure)/sizeof(genz_component_firmware_structure[0]), sizeof(struct genz_genz_component_firmware_structure), false, 0x1, "component_firmware" },
     {  genz_component_sw_management_structure, sizeof(genz_component_sw_management_structure)/sizeof(genz_component_sw_management_structure[0]), sizeof(struct genz_genz_component_sw_management_structure), false, 0x1, "component_sw_management" },
};

struct genz_control_ptr_info genz_table_type_to_ptrs[] = {
     {  genz_pg_restricted_pg_table, sizeof(genz_pg_restricted_pg_table)/sizeof(genz_pg_restricted_pg_table[0]), sizeof(struct genz_genz_pg_restricted_pg_table), false, None, "pg_restricted_pg_table" },
     {  genz_pte_restricted_pte_table, sizeof(genz_pte_restricted_pte_table)/sizeof(genz_pte_restricted_pte_table[0]), sizeof(struct genz_genz_pte_restricted_pte_table), false, None, "pte_restricted_pte_table" },
     {  genz_event_record, sizeof(genz_event_record)/sizeof(genz_event_record[0]), sizeof(struct genz_genz_event_record), false, None, "vent_record" },
     {  genz_performance_log_record_0, sizeof(genz_performance_log_record_0)/sizeof(genz_performance_log_record_0[0]), sizeof(struct genz_genz_performance_log_record_0), false, None, "performance_log_record_0" },
     {  genz_performance_log_record_1, sizeof(genz_performance_log_record_1)/sizeof(genz_performance_log_record_1[0]), sizeof(struct genz_genz_performance_log_record_1), false, None, "performance_log_record_1" },
     {  genz_firmware_table, sizeof(genz_firmware_table)/sizeof(genz_firmware_table[0]), sizeof(struct genz_genz_firmware_table), false, None, "firmware_table" },
     {  genz_type_1_interleave_table, sizeof(genz_type_1_interleave_table)/sizeof(genz_type_1_interleave_table[0]), sizeof(struct genz_genz_type_1_interleave_table), false, None, "type_1_interleave_table" },
     {  genz_component_tr_table, sizeof(genz_component_tr_table)/sizeof(genz_component_tr_table[0]), sizeof(struct genz_genz_component_tr_table), false, None, "component_tr_table" },
     {  genz_image_header_0xc86ed8c24bed49bda5143dd11950de9d, sizeof(genz_image_header_0xc86ed8c24bed49bda5143dd11950de9d)/sizeof(genz_image_header_0xc86ed8c24bed49bda5143dd11950de9d[0]), sizeof(struct genz_genz_image_header_0xc86ed8c24bed49bda5143dd11950de9d), false, None, "image_header_0xc86ed8c24bed49bda5143dd11950de9d" },
     {  genz_image_table, sizeof(genz_image_table)/sizeof(genz_image_table[0]), sizeof(struct genz_genz_image_table), false, None, "image_table" },
     {  genz_service_uuid_table, sizeof(genz_service_uuid_table)/sizeof(genz_service_uuid_table[0]), sizeof(struct genz_genz_service_uuid_table), false, None, "service_uuid_table" },
     {  genz_resource_array_table, sizeof(genz_resource_array_table)/sizeof(genz_resource_array_table[0]), sizeof(struct genz_genz_resource_array_table), false, None, "resource_array_table" },
     {  genz_c_cert_table, sizeof(genz_c_cert_table)/sizeof(genz_c_cert_table[0]), sizeof(struct genz_genz_c_cert_table), false, None, "c_cert_table" },
     {  genz_certificate_table, sizeof(genz_certificate_table)/sizeof(genz_certificate_table[0]), sizeof(struct genz_genz_certificate_table), false, None, "certificate_table" },
     {  genz_tik_table, sizeof(genz_tik_table)/sizeof(genz_tik_table[0]), sizeof(struct genz_genz_tik_table), false, None, "tik_table" },
     {  genz_unreliable_multicast_table_entry_row, sizeof(genz_unreliable_multicast_table_entry_row)/sizeof(genz_unreliable_multicast_table_entry_row[0]), sizeof(struct genz_genz_unreliable_multicast_table_entry_row), false, None, "unreliable_multicast_table_entry_row" },
     {  genz_reliable_multicast_table_entry_row, sizeof(genz_reliable_multicast_table_entry_row)/sizeof(genz_reliable_multicast_table_entry_row[0]), sizeof(struct genz_genz_reliable_multicast_table_entry_row), false, None, "reliable_multicast_table_entry_row" },
     {  genz_reliable_multicast_responder_table, sizeof(genz_reliable_multicast_responder_table)/sizeof(genz_reliable_multicast_responder_table[0]), sizeof(struct genz_genz_reliable_multicast_responder_table), false, None, "reliable_multicast_responder_table" },
     {  genz_unreliable_multicast_table, sizeof(genz_unreliable_multicast_table)/sizeof(genz_unreliable_multicast_table[0]), sizeof(struct genz_genz_unreliable_multicast_table), false, None, "unreliable_multicast_table" },
     {  genz_reliable_multicast_table, sizeof(genz_reliable_multicast_table)/sizeof(genz_reliable_multicast_table[0]), sizeof(struct genz_genz_reliable_multicast_table), false, None, "reliable_multicast_table" },
     {  genz_core_lpd_bdf_table, sizeof(genz_core_lpd_bdf_table)/sizeof(genz_core_lpd_bdf_table[0]), sizeof(struct genz_genz_core_lpd_bdf_table), false, None, "core_lpd_bdf_table" },
     {  genz_opcode_set_table, sizeof(genz_opcode_set_table)/sizeof(genz_opcode_set_table[0]), sizeof(struct genz_genz_opcode_set_table), true, None, "opcode_set_table" },
     {  genz_opcode_set_uuid_table, sizeof(genz_opcode_set_uuid_table)/sizeof(genz_opcode_set_uuid_table[0]), sizeof(struct genz_genz_opcode_set_uuid_table), false, None, "opcode_set_uuid_table" },
     {  genz_component_error_elog_entry, sizeof(genz_component_error_elog_entry)/sizeof(genz_component_error_elog_entry[0]), sizeof(struct genz_genz_component_error_elog_entry), false, None, "component_error_elog_entry" },
     {  genz_interface_error_elog_entry, sizeof(genz_interface_error_elog_entry)/sizeof(genz_interface_error_elog_entry[0]), sizeof(struct genz_genz_interface_error_elog_entry), false, None, "interface_error_elog_entry" },
     {  genz_elog_table, sizeof(genz_elog_table)/sizeof(genz_elog_table[0]), sizeof(struct genz_genz_elog_table), true, None, "log_table" },
     {  genz_ssdt_msdt_table_entry_row, sizeof(genz_ssdt_msdt_table_entry_row)/sizeof(genz_ssdt_msdt_table_entry_row[0]), sizeof(struct genz_genz_ssdt_msdt_table_entry_row), false, None, "ssdt_msdt_table_entry_row" },
     {  genz_rit_table, sizeof(genz_rit_table)/sizeof(genz_rit_table[0]), sizeof(struct genz_genz_rit_table), false, None, "rit_table" },
     {  genz_ssdt_msdt_table, sizeof(genz_ssdt_msdt_table)/sizeof(genz_ssdt_msdt_table[0]), sizeof(struct genz_genz_ssdt_msdt_table), false, None, "ssdt_msdt_table" },
     {  genz_requester_vcat_table, sizeof(genz_requester_vcat_table)/sizeof(genz_requester_vcat_table[0]), sizeof(struct genz_genz_requester_vcat_table), false, None, "requester_vcat_table" },
     {  genz_responder_vcat_table, sizeof(genz_responder_vcat_table)/sizeof(genz_responder_vcat_table[0]), sizeof(struct genz_genz_responder_vcat_table), false, None, "responder_vcat_table" },
     {  genz_lprt_mprt_rows, sizeof(genz_lprt_mprt_rows)/sizeof(genz_lprt_mprt_rows[0]), sizeof(struct genz_genz_lprt_mprt_rows), false, None, "lprt_mprt_rows" },
     {  genz_lprt_route_entry_row, sizeof(genz_lprt_route_entry_row)/sizeof(genz_lprt_route_entry_row[0]), sizeof(struct genz_genz_lprt_route_entry_row), false, None, "lprt_route_entry_row" },
     {  genz_mcprt_msmcptr_row, sizeof(genz_mcprt_msmcptr_row)/sizeof(genz_mcprt_msmcptr_row[0]), sizeof(struct genz_genz_mcprt_msmcptr_row), false, None, "mcprt_msmcptr_row" },
     {  genz_mvcat_table, sizeof(genz_mvcat_table)/sizeof(genz_mvcat_table[0]), sizeof(struct genz_genz_mvcat_table), false, None, "mvcat_table" },
     {  genz_route_control_table, sizeof(genz_route_control_table)/sizeof(genz_route_control_table[0]), sizeof(struct genz_genz_route_control_table), false, None, "route_control_table" },
     {  genz_mcprt_msmcprt_table, sizeof(genz_mcprt_msmcprt_table)/sizeof(genz_mcprt_msmcprt_table[0]), sizeof(struct genz_genz_mcprt_msmcprt_table), false, None, "mcprt_msmcprt_table" },
     {  genz_vcat_table, sizeof(genz_vcat_table)/sizeof(genz_vcat_table[0]), sizeof(struct genz_genz_vcat_table), false, None, "vcat_table" },
     {  genz_lprt_mprt_table, sizeof(genz_lprt_mprt_table)/sizeof(genz_lprt_mprt_table[0]), sizeof(struct genz_genz_lprt_mprt_table), false, None, "lprt_mprt_table" },
     {  genz_pa_table, sizeof(genz_pa_table)/sizeof(genz_pa_table[0]), sizeof(struct genz_genz_pa_table), false, None, "pa_table" },
     {  genz_sec_table, sizeof(genz_sec_table)/sizeof(genz_sec_table[0]), sizeof(struct genz_genz_sec_table), false, None, "sec_table" },
     {  genz_ssap_mcap_msap_and_msmcap_table, sizeof(genz_ssap_mcap_msap_and_msmcap_table)/sizeof(genz_ssap_mcap_msap_and_msmcap_table[0]), sizeof(struct genz_genz_ssap_mcap_msap_and_msmcap_table), false, None, "ssap_mcap_msap_and_msmcap_table" },
     {  genz_c_access_r_key_table, sizeof(genz_c_access_r_key_table)/sizeof(genz_c_access_r_key_table[0]), sizeof(struct genz_genz_c_access_r_key_table), false, None, "c_access_r_key_table" },
     {  genz_c_access_l_p2p_table, sizeof(genz_c_access_l_p2p_table)/sizeof(genz_c_access_l_p2p_table[0]), sizeof(struct genz_genz_c_access_l_p2p_table), false, None, "c_access_l_p2p_table" },
     {  genz_backup_mgmt_table, sizeof(genz_backup_mgmt_table)/sizeof(genz_backup_mgmt_table[0]), sizeof(struct genz_genz_backup_mgmt_table), false, None, "backup_mgmt_table" },
     {  genz_pm_backup_table, sizeof(genz_pm_backup_table)/sizeof(genz_pm_backup_table[0]), sizeof(struct genz_genz_pm_backup_table), false, None, "pm_backup_table" },
     {  genz_sm_backup_table, sizeof(genz_sm_backup_table)/sizeof(genz_sm_backup_table[0]), sizeof(struct genz_genz_sm_backup_table), false, None, "sm_backup_table" },
     {  genz_media_log_table, sizeof(genz_media_log_table)/sizeof(genz_media_log_table[0]), sizeof(struct genz_genz_media_log_table), false, None, "media_log_table" },
     {  genz_oem_data_table, sizeof(genz_oem_data_table)/sizeof(genz_oem_data_table[0]), sizeof(struct genz_genz_oem_data_table), false, None, "oem_data_table" },
     {  genz_label_data_table, sizeof(genz_label_data_table)/sizeof(genz_label_data_table[0]), sizeof(struct genz_genz_label_data_table), false, None, "label_data_table" },
     {  genz_ssod_table, sizeof(genz_ssod_table)/sizeof(genz_ssod_table[0]), sizeof(struct genz_genz_ssod_table), false, None, "ssod_table" },
     {  genz_msod_table, sizeof(genz_msod_table)/sizeof(genz_msod_table[0]), sizeof(struct genz_genz_msod_table), false, None, "msod_table" },
     {  genz_re_table, sizeof(genz_re_table)/sizeof(genz_re_table[0]), sizeof(struct genz_genz_re_table), false, None, "re_table" },
};

EXPORT_SYMBOL(genz_control_structure_type_to_ptrs);

size_t genz_control_structure_type_to_ptrs_nelems =
    sizeof(genz_control_structure_type_to_ptrs) /
    sizeof(genz_control_structure_type_to_ptrs[0]);

EXPORT_SYMBOL(genz_control_structure_type_to_ptrs_nelems);