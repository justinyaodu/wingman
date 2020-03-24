"""Expose the DLL functions of the Windows clipboard API."""

__all__ = ['OpenClipboard', 'CloseClipboard', 'EmptyClipboard',
        'EnumClipboardFormats', 'GetClipboardFormatNameW',
        'RegisterClipboardFormatW', 'GetClipboardData', 'SetClipboardData']

from ctypes import *
from ctypes.wintypes import *

from wingman.winutil import dll_helper


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-openclipboard
OpenClipboard = dll_helper.get_func('OpenClipboard', BOOL,
        [
            (HWND, 1, 'owner_hwnd'),
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-closeclipboard
CloseClipboard = dll_helper.get_func('CloseClipboard', BOOL,
        None,
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-emptyclipboard
EmptyClipboard = dll_helper.get_func('EmptyClipboard', BOOL,
        None,
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumclipboardformats
EnumClipboardFormats = dll_helper.get_func('EnumClipboardFormats', UINT,
        [
            (UINT, 1, 'format'),
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclipboardformatnamew
GetClipboardFormatNameW = dll_helper.get_func('GetClipboardFormatNameW', c_int,
        [
            (UINT, 1, 'format'),
            (LPWSTR, 1, 'name_buf'),
            (c_int, 1, 'buf_len')
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclipboardformatw
RegisterClipboardFormatW = dll_helper.get_func('RegisterClipboardFormatW', UINT,
        [
            (LPCWSTR, 1, 'format_name')
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclipboarddata
GetClipboardData = dll_helper.get_func('GetClipboardData', HANDLE,
        [
            (UINT, 1, 'format')
        ],
        lambda r: r is not None)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setclipboarddata
SetClipboardData = dll_helper.get_func('SetClipboardData', HANDLE,
        [
            (UINT, 1, 'format'),
            (HANDLE, 1, 'data_handle')
        ],
        lambda r: r is not None)

