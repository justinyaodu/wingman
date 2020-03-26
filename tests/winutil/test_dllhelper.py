import unittest
from ctypes import *
from ctypes.wintypes import *

from wingman.winutil import dllhelper


class TestDllHelper(unittest.TestCase):
    def setUp(self):
        # function to get a handle to the desktop window
        self.GetDesktopWindow = dllhelper.get_func("GetDesktopWindow", HWND,
                None, lambda r: r is not None, check_last_error=False)
        
        # get the desktop window HWND to use in later tests
        self.desktop_hwnd = self.GetDesktopWindow()

        # initialize character buffer
        self.buffer_size = 256
        self.buffer = create_unicode_buffer(self.buffer_size)

        # function to get the name of a window
        # supply argument names and default parameters
        self.GetWindowTextW = dllhelper.get_func("GetWindowTextW", c_int,
                (
                    (HWND, 1, "hWnd", self.desktop_hwnd),
                    (LPWSTR, 1, "lpString", self.buffer),
                    (c_int, 1, "nMaxCount", self.buffer_size)
                ),
                int(0).__ne__)

    def test_nonexistent_function_name(self):
        with self.assertRaises(NameError):
            dllhelper.get_func("NonexistentFunction", None, None)

    def test_parameter_type_check(self):
        # pass in a float instead of a HWND
        with self.assertRaises(ArgumentError):
            self.GetWindowTextW(c_float(0.1), self.buffer, self.buffer_size)

    def test_lasterror_raise_oserror(self):
        # pass a null HWND and see if LastError is checked
        with self.assertRaises(OSError):
            self.GetWindowTextW(None, self.buffer, self.buffer_size)

    def test_parameters_by_name(self):
        self.GetWindowTextW(
                hWnd=self.desktop_hwnd,
                lpString=self.buffer,
                nMaxCount=self.buffer_size)

    def test_default_parameters(self):
        self.GetWindowTextW()

