"""__init__.py
This file is the first file that Python reads when a package is imported.
It is used to define the package's public API.
"""

from importlib.metadata import PackageNotFoundError, version

from asm1_influent_generator.asm1_generator import ASM1Generator

__all__ = ['ASM1Generator']
try:
    __version__ = version('asm1-influent-generator')
except PackageNotFoundError:  # pragma: no cover
    __version__ = 'unknown'
finally:
    del version, PackageNotFoundError
