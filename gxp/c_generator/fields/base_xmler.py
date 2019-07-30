#!/usr/lib/python3
"""
(C) Copyright 2018 Hewlett Packard Enterprise Development LP” on your code

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
        self.name = name
        self.entries: list = []
        #XML element or whatever else used to parse it into an entry.
        self.origin = kwargs.get('origin', None)

        self.parent = None # an xml object - a parent of the entry
        self.children = []
        self.tag = None
        self.str_start = '' # string to put in front of the entry (e.g. comments)
        self.str_end = '' # string to put in the end of the entry
        self.open_bracket_str = '{'
        self.close_bracket_str = '};'
        self.str_left_space: int = kwargs.get('str_left_space', ' ' * 4)
        self.str_var_space: int = kwargs.get('str_var_space',' ' * 6)
        self.space_after_name: int = kwargs.get('space_after_name',' ' * 1)


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


    @abstractmethod
    def pprint(self):
        """ Formats XML parsed entries into a 'proper' display format. """
        return 'There is nothing to pritify here. Forgot to override?'


    @property
    def fields(self):
        return self.__dict__


    def __eq__(self, other):
        return self.name == other.name