"""Manipulate data in Windows global memory."""

__all__ = ['size_of', 'copy_to_global', 'copy_from_global', 'free']

from ctypes import *

from ._globalmemapi import *


class _GlobalPointer:
    """Context manager for locking and unlocking global memory. Returns
    a pointer to the memory region.
    """

    def __init__(self, handle):
        self.handle = handle

    def __enter__(self):
        return GlobalLock(self.handle)

    def __exit__(self, exc_type, exc_value, traceback):
        GlobalUnlock(self.handle)


def size_of(handle):
    """Return the size (in bytes) of a global memory object."""
    return GlobalSize(handle)


def copy_to_global(data, encoding=None):
    """Copy a string or bytes object to global memory, and return a
    handle to the allocated memory. If ``data`` is a string,
    ``encoding`` should specify an encoding as used by ``str.encode()``.
    """
    if isinstance(data, str):
        if encoding is None:
            msg = "An encoding must be specified for string data"
            raise ValueError(msg)
        else:
            data = data.encode(encoding)
    return _copy_bytes_to_global(data)


def _copy_bytes_to_global(data):
    """Copy a bytes object to global memory and return its handle."""
    if not isinstance(data, bytes):
        msg = "Expected bytes object, got '{}'"
        raise TypeError(msg.format(type(data)))

    handle = GlobalAlloc(GMEM.MOVEABLE, len(data))
    with _GlobalPointer(handle) as ptr:
        memmove(ptr, data, len(data))
    return handle


def copy_from_global(handle, encoding=None):
    """Return a string or bytes object copied from global memory. If
    ``encoding`` is specified, a decoded string is returned; otherwise,
    a bytes object is returned.
    """
    with _GlobalPointer(handle) as ptr:
        if encoding is None: # return bytes object
            return string_at(ptr, size_of(handle))
        elif '16' in encoding: # return wide character string
            return wstring_at(ptr)
        else: # return decoded bytes object
            return string_at(ptr, size_of(handle)).decode(encoding)


def free(handle):
    """Free previously allocated global memory."""
    return GlobalFree(handle)

