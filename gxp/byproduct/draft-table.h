enum genz_control_structure_type {
 ...

 GENZ_ PG Table and PTE Table = 0x1000,
  GENZ_ Event Record = 0x1001,
}

enum RES {
    No additional ...
    Restricted Access
}

struct "PG Table and PTE Table_array" {  //<element>
    uint64_t R0 : 12;
    uint64_t PG Base Address 0 : 52

    uint64_t Page Size 0;

    enum RES res;

    uint64_t Page Count 0 : ;
    uint64_t Base PTE Index 0 : ;
}

struct "GENZ_ PG Table and PTE Table"  {
    uint64_t PTE Table : 64;
    struct "PG Table and PTE Table_array" field_name_pg_table..[]; //unknown size becasue elements="VARIABLE"
   // Another <array> field entries?
   //if more than one array, then all But the Last one MUST be FIxed size;
}


//If lknown size, then size goes to array definition -> field_name_pg_table..[SIZE];

//Structs representing the pointers in Tables will have a different pointer type vs a regular <Struct>


/*
* The overall table_type_to_pointers is an array indexed by
* the structure type enum (e.g. starting at 0x1000) to access the appropriate
* <name>_table_pointer array.
THIS IS EXACTLY LIKE THE struct genz_control_ptr_info genz_control_structure_type_to_ptrs[] in .C
WIll go to .C as well...
 */
//?????
struct genz_table_pointers table_type_to_pointers[] = {

    ...

};

/* --------------------- Out of tables arrays --------------------- */

struct "Vendor-Defined Structure_array" {
    uint "Vendor-Defined Data 0";
};


struct "genz_Vendor-Defined Structure" {
    type;
    vers;
    size;

    struct "Vendor-Defined Structure_array" "Vendor-Defined Structure"[];
}


struct "??_array" {
    uint "class 0";
    uint "max si 0";
    uint "class 1";
    uint "max si 1";
}

struct "Service UUID Structure" {
    struct "??"_array "??"[];
}


enum genz_control_pointer_flags {
    //Not used at all. can remove or not.
    GENZ_CONTROL_POINTER_NONE = 0,
    //look for word "generic structure" and set a "genz_control_structure_type" to an "-1" thingy.
    //if its pointing to a Struct, then keep following the pointer to find a enum value from that
    //big table of Struct names which is Second or whatever value in the C array entries.
    //Look up every pointer in the struct it points to. If none points to its own struct -
    //then it is a POINTER_STRUCTURE type.
    GENZ_CONTROL_POINTER_STRUCTURE = 1, /* Points to a structure. Use ptr_type to see if it is generic or a particular type.  */
    //Looked for a Struct or Table - look up the structure and look inside it and its pointers,
    //the First pointer is Start
    GENZ_CONTROL_POINTER_CHAIN_START = 6,
    //every next point (technically the last one referencing itself) is Chained.
    GENZ_CONTROL_POINTER_CHAINED = 2, /* e.g. Interface structures */
    //If points to a thing that is a Table and it has an array that is THE ONLY thing in the table.
    // then it is an array pointer.
    GENZ_CONTROL_POINTER_ARRAY = 3, /* Table of structures, e.g. C-Access R-Key table. */
    //look in the table and it just the offsets.
    //And if it DOES NOT has a "Variable" type <array>.
    GENZ_CONTROL_POINTER_TABLE = 4,
    //Looking at table ptr_to points to, it has some offsets and then a VARIABLE array.
    GENZ_CONTROL_POINTER_TABLE_WITH_HEADER = 5, /* Header followed by table of structures, e.g. ELog Table */
};

//OpCode Set PTR is a chain start
//Next OpCode Set PTR - is a chain