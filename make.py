import sys
from cx_Freeze import setup, Executable
from smlib import __version__ as version

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=['smlib'], excludes=[])

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executable_files = [
    Executable('smbedit.py', 'Console'),
    Executable('smbeditGUI.py', base=base),
]

setup(
    name='SMBEdit',
    version=version,
    description='StarMade Blueprint Editor',
    author='Peter Hofmann',
    author_email='',
    url='https://github.com/p-hofmann/SMBEdit',
    packages=['smlib'],
    options=dict(build_exe=buildOptions),
    executables=executable_files
    )

# Some issue with TCL can occur on Windows 
#
# see https://github.com/ContinuumIO/anaconda-issues/issues/36
#
# set TCL_LIBRARY=C:\Anaconda\envs\<venvname>\tcl\tcl8.6
# set TK_LIBRARY=C:\Anaconda\envs\<venvname>\tcl\tk8.6
