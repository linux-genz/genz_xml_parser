#!/usr/bin/python3
"""
(C) Copyright 2019 Hewlett Packard Enterprise Development LP” on your code

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

********************************************************************************

    Transforms XML entries into the .h struct format:

struct genz_core {
    uint64_t type        : 12;
    uint64_t vers        : 4;
    uint64_t size        : 16;
    uint64_t r0           : 32;
    ....
"""
import argparse
import collections
import datetime
import os
import math
import xml.etree.ElementTree
import jinja2
import logging

from pdb import set_trace
from gxp.generator import fields
from gxp.generator.models import DataTypesModel
from gxp.CGenerator import CGenerator
from gxp.generator.parsers import ClassParser


def render_template_str(template_path: str, props: dict):
    """
        Renders an output string from the template file and the props.

    @param template_path: path to a template file with the matchiing to "props" values.
    @param props: properties of the template_path jinja template.

    @return: a rendered string from the jinja template.
    """
    template_str = None
    with open(template_path, 'r') as file_obj:
        template_str = file_obj.read()

    header_template = jinja2.Template(template_str)

    return header_template.render(props)


def get_xml_from_url(url: str):
    """
        Read XML file from Url link and saves into /tmp/.

    @param url: url path to xml file.
    @return: path to a downloaded xml file.
    """
    # importing here, not globally, saves half a second when not using url path
    import requests
    file_name = url.split('/')[-1]
    save_dest = os.path.join('/tmp/', file_name)

    req = requests.get(url)
    with open(save_dest, 'w+') as file_obj:
        file_obj.write(req.content.decode("utf-8"))

    return save_dest


def meta_from_filename(filename: str):
    """
        Get a Version and a Date from a filename of the parsed XML specs.
    :param filename: name of the file that was parsed.
    :return: <dict> {
                        'xml_version': 'N/A',
                        'xml_date': 'N/A'
                    }
    """
    result = {
        'xml_version': 'N/A',
        'xml_date': 'N/A'
    }

    filename = filename.strip('.xml')  # v1.0a-20181207.xml -> v1.0a-20181207
    splitted = filename.split('-')  # v1.0a-20181207 -> [v1.0a, 20181207]

    if len(splitted) < 2:
        return result

    if 'v' in splitted[0]:
        result['xml_version'] = splitted[0]

    try:
        date = datetime.datetime.strptime(splitted[-1], '%Y%m%d')
        result['xml_date'] = date.strftime('%d, %b %Y')
    except ValueError:
        result['xml_date'] = 'unknown'
    return result


def this_build_version(version_file: str='./VERSION'):
    """
        VERSION file should be at the top dir of the project. It should have only
    one line: "VERSION='1.0'". On any error should occure - 'n/a' will be returned.
    :param version_file: path to a VERSION
    :return:
    """
    if not os.path.exists(version_file):
        return 'N/A'

    file_content = ''
    with open(version_file, 'r') as file_obj:
        file_content = file_obj.read()

    try:
        return file_content.split('=')[-1].strip('\'')
    except IndexError:
        return 'N/A'


def extract_xml_meta(xml_data):
    """
        XML file should have a "generated" property in its root(genz entry).
    Extract that value of format "2019-02-04 17:17:24.050242", but split by '.'
    and assume left side being Date and right side being Version (for whatever reason).
    """
    meta: dict = {}
    generated = xml_data.get('generated', 'N/A')
    meta['date'] =  generated.split('.')[0]
    meta['version'] = generated.split('.')[-1]

    return meta


def entries_to_str(entries: list) -> dict:
    """
        Parse parsed entries of the xml file into a readable/printable string chunk.
        Each entry is a <FieldParser> object that is converted so string in the
    exact order it appears in the list.

    @param entries: List of <FieldParser> objects.
    @return: <dict> { 'data', 'total_fields' }. 'data' is a writable to a file string.
    """
    to_write = []
    enum_count = 0
    total_fields = 0

    newline_multiplier = 1
    # filler_string = '/* ' + ('*' * 75) + ' */' + ('\n' * newline_multiplier)
    # to_write.append(filler_string)
    for entry in entries:
        # Ignore empty structs to the .h file.
        if entry.is_empty():
            struct_comment = entry.fields.get('open_bracket', None)
            if struct_comment:
                msg = '//FIXME: empty struct.'
                entry.open_bracket = '%s %s' % (struct_comment, msg)

        # Enums of size 1 are no needed in the header - so skip them
        if isinstance(entry, fields.CEnumEntry):
            if len(entry.entries) < 1:
                continue

        if isinstance(entry, fields.CEnumEntry):
            enum_count += 1

        to_write.append(entry.pprint() + ('\n' * newline_multiplier))
        # to_write.append(filler_string)
        total_fields += len(entry.entries)

    return { 'data' : to_write,
            'total_fields' : total_fields }


def build_control_structure_types(structs: list, start_index=0):
    result = []
    for index in range(len(structs)):
        s = structs[index]
        entry = {
            'name' : s.name,
            'index' : start_index + index,
          }
        result.append(entry)
    return result


def default_args(self) -> dict:
    return


def main(cmd_args: dict):
    """
        Look at __name__ argparse arguments for expected parameters.
    """
    logging.getLogger().setLevel(cmd_args.get('verbose', 10))
    path: str = cmd_args['xml_path']
    dest: str = cmd_args['output'].strip()
    is_no_c_file: bool = cmd_args.get('no_c', False)
    c_dest: str = ''
    if '.h' not in dest:
        dest = '%s.h' % dest
    c_dest = dest.replace('.h', '.c')

    # context = None  # xml root
    is_clean_tmp: bool = False  # url file downloaded and to be removed in the end
    xml_meta: dict = {}
    template_props: dict = {}

    # if the path is URL, download a file and save it into /tmp/. It will be
    # cleaned up in the end.
    if 'http://' in path or 'https://' in path:
        path = get_xml_from_url(path)
        is_clean_tmp = True

    # Parsing XML file into an stringable object
    xml_root = xml.etree.ElementTree.parse(path).getroot()
    # context = xml_root.find('structs')
    xml_meta = extract_xml_meta(xml_root)
    generator = CGenerator(xml_root)
    table_generator = CGenerator(xml_root, tags={'struct' : 'table'})
    generator.merge(table_generator)

    #.merge ignores structs. Thus, need to add table structs manually
    generator._add_to_list(table_generator.structs, generator.structs)
    pointers = generator.update_pointers()

    struct_info_array, table_info_array = generator.build_control_ptr_info_array()

    class_parser = ClassParser(xml_root.find('classes'))
    if class_parser is not None and class_parser.instance is not None:
        generator.enums.append(class_parser.enum)
        generator.structs.insert(0, class_parser.struct_meta)

    entries = generator.entries

    write_props = entries_to_str(entries)

    date_now = datetime.datetime.now()
    date_now = date_now.strftime('%d, %b %Y')

    # Template Props fields are matching the ./templates/header.template formate.
    template_props = meta_from_filename(os.path.basename(path))
    template_props['xml_date'] = xml_meta['date']
    template_props['xml_version'] = xml_meta['version']

    template_props['generated_on'] = date_now
    template_props['struct_count'] = len(generator.structs)
    template_props['enum_count'] = len(generator.enums)
    template_props['fields_count'] = write_props['total_fields']
    template_props['union_count'] = len(generator.unions)
    template_props['script_version'] = this_build_version()

    # Not all things that are in .structs are actually rendered. Thus, need to
    # loop through the .entries instead and add <struct> types to the Union list
    # of all the structs rendered to the header file.
    rendered_structs = []
    for s_entry in entries:
        if isinstance(s_entry, fields.CStruct):
            rendered_structs.append(s_entry)
    template_props['all_structs'] = rendered_structs

    # template_props['struct_ptr_names'] = ['%s' % p.name for p in generator.pointers]
    template_props['body'] = '\n'.join(write_props['data'])

    pointer_entries = entries_to_str([ptr for ptr in generator.pointers])
    export_symbols = generator.export_symbol_struct
    export_symbols.extend(generator.export_symbol_table)
    export_symbols = entries_to_str(export_symbols)

    c_template_props = {
        'body': '\n'.join(pointer_entries['data']),
        'export_symbols': '\n'.join(export_symbols['data']),
        'header_file': os.path.basename(dest),
        'pointers': pointers,
        'type_name': DataTypesModel.ctr_ptr_info_struct_name
    }

    if class_parser is not None and class_parser.instance is not None:
        c_template_props['body'] = '%s\n\n%s' % (class_parser.instance.pprint(), c_template_props['body'])

    c_template_props['body'] = '%s\n\n%s' % \
            (c_template_props['body'], struct_info_array)
    c_template_props['body'] = '%s\n\n%s' % \
            (c_template_props['body'], table_info_array)

    header = render_template_str(cmd_args['header_template'], template_props)
    c_file = render_template_str(cmd_args['c_template'], c_template_props)

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    with open(dest, 'w+') as file_obj:
        file_obj.write(header)

    if not is_no_c_file:
        with open(c_dest, 'w+') as file_obj:
            file_obj.write(c_file)

    if is_clean_tmp:
        if os.path.exists(path):
            os.remove(path)

    logging.info('%s\nHeader "%s" has been generated!' % ('-' * 20, dest))
    if not is_no_c_file:
        logging.info('C file "%s" has been generated!' % c_dest)

    return 0

def parse_args():
    this_file = os.path.realpath(__file__)
    this_dir = os.path.dirname(this_file)
    parser = argparse.ArgumentParser(description='XML parser parameters')
    parser.add_argument('xml_path',
                        help='Path or URL to a XML file to parse into .h')

    parser.add_argument('--output', '-o',
                        help='Output where to save the .h file. '\
                            'Note, .c generated from output name. '\
                            'E.g. output=header.h -> header.c will be created.',
                        required=True)

    parser.add_argument('--no-c', action='store_true',
                        help="Disable creation of .c file.")

    parser.add_argument('--header-template',
                        default=os.path.join(this_dir, 'templates/header.template'),
                        help='(optional) Header string to go into .h file.')

    parser.add_argument('--c-template',
                    default=os.path.join(this_dir, 'templates/c.template'),
                    help='(optional) C file template path.')

    parser.add_argument('--verbose', '-v',
                    type=int,
                    default=30,
                    help='Use: 10=debug, 20=info, 30=warning, 40=error or 50=critical. Ref to python3 logging docs.')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(vars(args))
