import os


__author__ = 'Peter Hofmann'


class Blueprint(object):
    """
    @type _blueprints: set[str]
    """

    def __init__(self):
        self._blueprints = set()
        self._file_name = "meta.smbpm"
        directory_blueprints = "./"
        self._find_blueprints(directory_blueprints)

    def __iter__(self):
        for directory in self._blueprints:
            yield directory

    def _find_blueprints(self, directory_blueprints):
        list_of_stuff = os.listdir(directory_blueprints)
        for name in list_of_stuff:
            path = os.path.join(directory_blueprints, name)
            if not os.path.isdir(path):
                continue
            file_path = os.path.join(path, self._file_name)
            if not os.path.exists(file_path):
                continue
            self._blueprints.add(path)
