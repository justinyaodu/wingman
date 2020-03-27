"""Expose the DLL functions of the Windows clipboard API."""

__all__ = ['OpenClipboard', 'CloseClipboard', 'EmptyClipboard',
        'EnumClipboardFormats', 'GetClipboardFormatNameW',
        'RegisterClipboardFormatW', 'GetClipboardData', 'SetClipboardData']

from ctypes import *
from ctypes.wintypes import *

from wingman.winutil import dllhelper


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-openclipboard
OpenClipboard = dllhelper.get_func('OpenClipboard', BOOL,
        [
            (HWND, 1, 'owner_hwnd')
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-closeclipboard
CloseClipboard = dllhelper.get_func('CloseClipboard', BOOL,
        None,
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-emptyclipboard
EmptyClipboard = dllhelper.get_func('EmptyClipboard', BOOL,
        None,
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumclipboardformats
EnumClipboardFormats = dllhelper.get_func('EnumClipboardFormats', UINT,
        [
            (UINT, 1, 'format')
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclipboardformatnamew
GetClipboardFormatNameW = dllhelper.get_func('GetClipboardFormatNameW', c_int,
        [
            (UINT, 1, 'format'),
            (LPWSTR, 1, 'name_buf'),
            (c_int, 1, 'buf_len')
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclipboardformatw
RegisterClipboardFormatW = dllhelper.get_func('RegisterClipboardFormatW', UINT,
        [
            (LPCWSTR, 1, 'format_name')
        ],
        int(0).__ne__)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclipboarddata
GetClipboardData = dllhelper.get_func('GetClipboardData', HANDLE,
        [
            (UINT, 1, 'format')
        ],
        lambda r: r is not None)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setclipboarddata
SetClipboardData = dllhelper.get_func('SetClipboardData', HANDLE,
        [
            (UINT, 1, 'format'),
            (HANDLE, 1, 'data_handle')
        ],
        lambda r: r is not None)

