from smlib import __version__ as version, __author__ as author

from setuptools import setup, find_packages

setup(
    name="SMBEdit",
    version=version,
    description="StarMade Blueprint Editor",
    author=author,
    author_email="",
    url="https://github.com/p-hofmann/SMBEdit",
    packages=find_packages(exclude=["unittests", "__pycache__"]),
    py_modules=["smbedit", "smbeditGUI"],
    entry_points={
        "console_scripts": [
            "smbedit = smbedit:main",
            "smb = smlib.cli.smb:main",
            ],
        "gui_scripts": [
            "smbeditGUI = smbeditGUI:main",
            ],
        },
    )
