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
#include "classes.h"

struct hardware_classes_meta hardware_classes[] = {
     { "Reserved—shall not be used",                          "reserved_shall_not_be_used", RESERVED_SHALL_NOT_BE_USED },
     { "Memory ( P2P 64 )",                                   "memory", MEMORY },
     { "Memory (Explicit OpClass)",                           "memory", MEMORY },
     { "Integrated Switch",                                   "switch", SWITCH },
     { "Enclosure / Expansion Switch",                        "switch", SWITCH },
     { "Fabric Switch",                                       "switch", SWITCH },
     { "Processor (Bootable)",                                "processor", PROCESSOR },
     { "Processor (Non-boot)",                                "processor", PROCESSOR },
     { "Accelerator (Non-coherent, non-boot)",                "accelerator", ACCELERATOR },
     { "Accelerator (Coherent, non-boot)",                    "accelerator", ACCELERATOR },
     { "Accelerator (Non-coherent, bootable)",                "accelerator", ACCELERATOR },
     { "Accelerator (Coherent, bootable)",                    "accelerator", ACCELERATOR },
     { "I/O (Non-coherent, non-boot)",                        "io", IO },
     { "I/O (Coherent, non-boot)",                            "io", IO },
     { "I/O (Non-coherent, bootable)",                        "io", IO },
     { "I/O (Coherent, bootable)",                            "io", IO },
     { "Block Storage (Bootable)",                            "block_storage", BLOCK_STORAGE },
     { "Block Storage (Non-boot)",                            "block_storage", BLOCK_STORAGE },
     { "Transparent Router",                                  "transparent_router", TRANSPARENT_ROUTER },
     { "Multi-class Component (see Service UUID Structure )", "multiclass_component", MULTICLASS_COMPONENT },
     { "Discrete Gen-Z Bridge",                               "bridge", BRIDGE },
     { "Integrated Gen-Z Bridge",                             "bridge", BRIDGE },
     { "Compliance Test Board",                               "compliance_test_board", COMPLIANCE_TEST_BOARD },
     { "Logical PCIe Hierarchy (LPH)",                        "logical_pcie_hierarchy", LOGICAL_PCIE_HIERARCHY },
};



struct genz_control_ptr_info genz_struct_type_to_ptrs[] = {};

struct genz_control_ptr_info genz_table_type_to_ptrs[] = {};

EXPORT_SYMBOL(genz_struct_type_to_ptrs);

size_t genz_struct_type_to_ptrs_nelems = sizeof(genz_struct_type_to_ptrs) / sizeof(genz_struct_type_to_ptrs[0]);

EXPORT_SYMBOL(genz_struct_type_to_ptrs_nelems);

EXPORT_SYMBOL(genz_table_type_to_ptrs);

size_t genz_table_type_to_ptrs_nelems = sizeof(genz_table_type_to_ptrs) / sizeof(genz_table_type_to_ptrs[0]);

EXPORT_SYMBOL(genz_table_type_to_ptrs_nelems);
