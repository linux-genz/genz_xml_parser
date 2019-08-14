#!/usr/lib/python3
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
"""
from abc import ABC, abstractmethod


class BaseXmler(ABC):
    """ This is a base class/interface for the parsed XML entries or any other
    XML related activities. Its purpose is to provide common interfaces to be
    used by anything that interucts with this class.
    """

    def __init__(self, name, **kwargs):
        """
            @param entries: [optional] <list> of entries can be set during init.
            @param origin: [optional] <xml.etree.ElementTree> xml object this
                        entry generated from.
            @param tag: [optional] tag of the entry. If origin is set - its tag
                        can be used. Origin's tag can be overwritting by setting
                        this prop.
            @param
        """
        self.name = name
        self.entries: list = kwargs.get('entries', [])
        #XML element or whatever else used to parse it into an entry.
        self.origin = kwargs.get('origin', None)
        self._tag = kwargs.get('tag', None)

        self.parent = None # an xml object - a parent of the entry
        self.children = []
        self.str_start = kwargs.get('strat', '') # string to put in front of the entry (e.g. comments)
        self.str_end = kwargs.get('end', '') # string to put in the end of the entry
        self.open_bracket = kwargs.get('open_bracket', '{')
        self.close_bracket = kwargs.get('close_bracket', '};')
        self.l_space: int = kwargs.get('l_space', ' ' * 4)
        self.var_space: int = kwargs.get('var_space',' ' * 6)
        self.name_space: int = kwargs.get('name_space',' ' * 1)


    def append(self, entry):
        """
            @param entry: something to be added to the entries list. It could be
                        a string, or CStructEntry object.
            return: False if no entry was added; True - entry added to the list.
        """
        if entry in self.entries:
            return False

        self.entries.append(entry)
        return True


    def extend(self, entry_group):
        if not isinstance(entry_group, list):
            return self.append(entry_group)

        for entry in entry_group:
            self.append(entry)

        return True


    def is_empty(self):
        return len(self.entries) == 0


    def get(self, key, default=None):
        return self.__dict__.get(key, default)


    @property
    def tag(self):
        if self._tag is not None:
            return self._tag
        if self.origin is not None:
            return self.origin.tag
        return None


    @abstractmethod
    def pprint(self):
        """ Formats XML parsed entries into a 'proper' display format. """
        return 'There is nothing to pritify here. Forgot to override?'


    @property
    def fields(self):
        return self.__dict__


    def __eq__(self, other):
        return self.name == other.name