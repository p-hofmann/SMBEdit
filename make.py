import sys
import os
import shutil
from cx_Freeze import setup, Executable
from smlib import __version__ as version

build_path = os.path.abspath('build')
if os.path.exists(build_path):
    shutil.rmtree(build_path)

packages = [
    "smlib",
    # 'PyQt5', 'numpy', 'meshlib', 'voxlib',
    # "sys", "os", "zipfile", "shutil", "traceback", "struct", "math", "tempfile", 'encodings'
    ]
base = None
include_files = []
if sys.platform == "win32":
    base = "Win32GUI"
    dir_python_dlls = os.path.join(os.environ['TCL_LIBRARY'], "..", "..", "DLLs")
    tk86t_dll = os.path.join(dir_python_dlls, "tk86t.dll")
    tcl86t_dll = os.path.join(dir_python_dlls, "tcl86t.dll")
    include_files = [tcl86t_dll, tk86t_dll]

build_options = dict(
    packages=packages,
    excludes=[
        "unittests", "__pycache__", "nose",
        'PyQt5', 'numpy', 'meshlib', 'voxlib',
        # "scipy.lib.lapack.flapack", "setuptools",
        # "numpy.core._dotblas", "tkinter", "http",
        # 'PyQt5', "html", "html", "email"
        ],
    bin_excludes=['setup.py'],
    include_files=include_files,
    silent=True
    )

executable_files = [
    Executable('smbedit.py', 'Console'),
    # Executable('smbeditGUI.py', base=base)
]

setup(
    name='SMBEdit',
    version=version,
    description='StarMade Blueprint Editor',
    author='Peter Hofmann',
    author_email='',
    url='https://github.com/p-hofmann/SMBEdit',
    packages=['smlib'],
    options=dict(build_exe=build_options),
    executables=executable_files
    )

# Some issue with TCL can occur on Windows
#
# see https://github.com/ContinuumIO/anaconda-issues/issues/36
#
# set TCL_LIBRARY=C:\Anaconda\envs\<venvname>\tcl\tcl8.6
# set TK_LIBRARY=C:\Anaconda\envs\<venvname>\tcl\tk8.6
