# import appropriate clipboard implementation
# TODO change this once a real clipboard implementation is finished
from . import _fakeclipboard

from .clipboard import selection, primary, secondary

