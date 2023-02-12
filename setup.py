from cx_Freeze import setup, Executable
import sys

build_options = {'packages': [], 'excludes': []}

base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('run.py', base=base, target_name = 'here_in_darkness')
]

setup(name='pong_deluxe_edition',
      version = '0.01',
      description = 'a game',
      options = {'build_exe': build_options},
      executables = executables)
