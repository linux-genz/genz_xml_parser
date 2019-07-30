from abc import ABC, abstractmethod
import logging


class FieldBuilderBase(ABC):

    def __init__(self, root, **kwargs):
        """
            @param field: <xml> field entry.
            @param hierarchy: <list> parent structure. The higher in the list the
                    higher the "relatives" are. E.g.:
                    [ first parent, parent of prev, parent of parent of prev ...]
            @param expected_tag: default=None; Tag name to expect to parse the root.
        """
        self.root = root
        self.expected_tag = kwargs.get('expected_tag', None)
        self._instance = None #can be anything. A parent will set it itself.
        self.parse(self.root)


    @abstractmethod
    def parse(self, root):
        """
            @param root: xml root tree to start parsing from.
        """
        raise NotImplementedError('"parse()" function not implemented in "%s"!' % (__name__))


    @property
    def instance(self):
        return self._instance