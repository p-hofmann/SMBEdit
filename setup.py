from smlib import __version__ as version

from setuptools import setup, find_packages

setup(
    name="SMBEdit",
    version=version,
    description="StarMade Blueprint Editor",
    author="Peter Hofmann",
    author_email="",
    url="https://github.com/p-hofmann/SMBEdit",
    packages=find_packages(exclude=["unittests", "__pycache__"]),
    py_modules=["smbedit", "smbeditGUI"],
    entry_points={
        "console_scripts": [
            "smbedit = smbedit:main",
            ],
        "gui_scripts": [
            "smbeditGUI = smbeditGUI:main",
            ],
        },
    )
