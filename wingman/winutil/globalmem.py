"""Manipulate data in Windows global memory."""

__all__ = ['size_of', 'copy_to_global', 'copy_from_global', 'free']

import ctypes

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


def _is_wide_encoding(encoding):
    """Check whether an encoding (represented by a string) is a wide
    character encoding.
    """
    return '16' in encoding


def copy_to_global(data, encoding=None):
    """Copy a string or bytes object to global memory, and return a
    handle to the allocated memory. If ``data`` is a string,
    ``encoding`` should specify an encoding as used by ``str.encode()``.
    """
    if isinstance(data, str):
        if encoding is None:
            msg = "An encoding must be specified for string data"
            raise ValueError(msg)
        elif _is_wide_encoding(encoding):
            data = ctypes.create_unicode_buffer(data)
        else:
            data = ctypes.create_string_buffer(data.encode(encoding))
    elif isinstance(data, bytes):
        size = len(data) # don't need a null terminator for binary data
        data = ctypes.create_string_buffer(data, size=size)
    else:
        msg = "Expected string or bytes object; got '{}'"
        raise TypeError(msg.format(type(data).__name__))

    size = ctypes.sizeof(data)
    handle = GlobalAlloc(GMEM.MOVEABLE, size)
    with _GlobalPointer(handle) as ptr:
        ctypes.memmove(ptr, data, size)
    return handle


def copy_from_global(handle, encoding=None):
    """Return a string or bytes object copied from global memory. If
    ``encoding`` is specified, a decoded string is returned; otherwise,
    a bytes object is returned.
    """
    with _GlobalPointer(handle) as ptr:
        if encoding is None: # return bytes object
            return ctypes.string_at(ptr, size=size_of(handle))
        elif _is_wide_encoding(encoding): # return wide character string
            return ctypes.wstring_at(ptr)
        else: # return decoded bytes object
            return ctypes.string_at(ptr).decode(encoding)


def free(handle):
    """Free previously allocated global memory."""
    return GlobalFree(handle)

