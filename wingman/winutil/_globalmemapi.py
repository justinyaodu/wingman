"""DLL functions for working with global memory."""

from ctypes import *
from ctypes.wintypes import *

from . import dllhelper

__all__ = ['GMEM', 'GlobalAlloc', 'GlobalFree', 'GlobalLock', 'GlobalUnlock',
        'GlobalSize']


class GMEM:
    """Global memory allocation flags. Source:
    https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalalloc
    """
    MOVEABLE = 0x0002


# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalalloc
GlobalAlloc = dllhelper.get_func('GlobalAlloc', HGLOBAL,
        [
            (UINT, 1, 'flags'),
            (c_size_t, 1, 'size')
        ],
        lambda r: r is not None)


# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalfree
GlobalFree = dllhelper.get_func('GlobalFree', HGLOBAL,
        [
            (HGLOBAL, 1, 'handle')
        ],
        lambda r: r is None)


# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globallock
GlobalLock = dllhelper.get_func('GlobalLock', HGLOBAL,
        [
            (LPVOID, 1, 'handle')
        ],
        lambda r: r is not None)


# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalunlock
GlobalUnlock = dllhelper.get_func('GlobalUnlock', BOOL,
        [
            (HGLOBAL, 1, 'handle')
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalsize
GlobalSize = dllhelper.get_func('GlobalSize', c_size_t,
        [
            (HGLOBAL, 1, 'handle')
        ],
        int(0).__ne__)

