import os
import tempfile
import zipfile
import shutil


__author__ = 'Peter Hofmann'


class Blueprint(object):
    """
    python smbedit.py \
    "test.sment" \
    -sm "~/starmade-launcher/StarMade" \
    -s -silent \
    -u \
    -d \
    -aw \
    -at \
    -ah \
    -ac \
    -et 0 \
    -ec 5 \
    -m 1,-1,-1 \
    -ma x \
    -rm 940,444 \
    -r 283:922 \
    -rh a:s \
    -o /tmp/tmp_blueprint.sment


    @type _blueprints: set[str]
    """

    def __init__(self, sment=True):
        self._tmp = tempfile.mkdtemp(prefix="blueprint_tests")
        self._blueprints = set()
        self._file_name = "meta.smbpm"
        directory_blueprints = os.path.join(".", "test_blueprints")
        self._blueprints = set()
        if sment:
            blueprints = self._find_blueprint_sment(directory_blueprints)
            for blueprint_path in blueprints:
                self.extract_sment(blueprint_path)
        else:
            self._find_blueprint_dirs(directory_blueprints)

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self._tmp)

    def __del__(self, type, value, traceback):
        shutil.rmtree(self._tmp)

    def __iter__(self):
        for directory in self._blueprints:
            yield directory

    def extract_sment(self, file_path):
        tmp = tempfile.mkdtemp(prefix="blueprint_tests", dir=self._tmp)
        with zipfile.ZipFile(file_path, "r") as read_handler:
            read_handler.extractall(tmp)
        new_path = os.path.join(tmp, os.listdir(tmp)[0])
        self._blueprints.add(new_path)
        return new_path

    def _find_blueprint_dirs(self, directory_blueprints):
        self._blueprints = set()
        list_of_stuff = os.listdir(directory_blueprints)
        for name in list_of_stuff:
            path = os.path.join(directory_blueprints, name)
            if not os.path.isdir(path):
                continue
            file_path = os.path.join(path, self._file_name)
            if not os.path.exists(file_path):
                continue
            self._blueprints.add(path)

    def _find_blueprint_sment(self, directory_blueprints):
        blueprints = set()
        list_of_stuff = os.listdir(directory_blueprints)
        for name in list_of_stuff:
            path = os.path.join(directory_blueprints, name)
            if os.path.isdir(path):
                continue
            if path.endswith(".sment"):
                blueprints.add(path)
        return blueprints

blueprint_handler = Blueprint()
