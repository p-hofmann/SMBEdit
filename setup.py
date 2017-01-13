from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

executables = [
    Executable('smbedit.py', 'Console')
]

setup(name='SMBEdit',
      version = '0.1.2',
      description = 'StarMade Blueprint Editor',
      options = dict(build_exe = buildOptions),
      executables = executables)

# Some issue with TCL can occur on Windows 
#
# see https://github.com/ContinuumIO/anaconda-issues/issues/36
#
# set TCL_LIBRARY=C:\Anaconda\envs\<venvname>\tcl\tcl8.6
# set TK_LIBRARY=C:\Anaconda\envs\<venvname>\tcl\tk8.6