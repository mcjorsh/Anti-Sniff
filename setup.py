from distutils.core import setup as su
from distutils.core import Extension
from setuptools import find_packages
from cx_Freeze import setup, Executable
import sys

su(name='AS',
      version='0.1.0',
    install_requires=['scapy-python3', 'wxpython']
     )

base = 'Win32GUI'

if sys.platform == 'win32':
    base = 'Win32GUI'


executables = [Executable("gui/antisniff.py", base=base)]
setup(
    name = "antisniff",
    version = "0.1",
    description = 'Herramienta para crear servidores seguros (cuya actividad no se pueden rastrear)',
    executables = executables
)
