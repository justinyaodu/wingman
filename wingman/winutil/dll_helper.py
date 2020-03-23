"""Get functions from Windows DLLs."""

__all__ = ['get_func']

from ctypes import *
from ctypes.wintypes import *

# DLLs to search for functions in
_dlls = [
    WinDLL("user32"),
    WinDLL("kernel32"),
]

# For some reason, I couldn't get `use_last_error` to work (the ctypes
# local copy of LastError wasn't set automatically), so here's the DLL
# function to set LastError directly. Ironically, the DLL function
# loading functionality implemented below can't easily be used to load
# this function, since that would introduce a circular dependency, so
# it's defined the old-fashioned way here.
SetLastError = windll.kernel32.SetLastError
SetLastError.restype = None
SetLastError.argtypes = [DWORD]


def _clear_last_error_before(func):
    """Returns a wrapper function which will clear ``LastError`` before
    calling ``func``.
    """
    def wrapper(*args, **kwargs):
        SetLastError(0)
        return func(*args, **kwargs)
    return wrapper


def _errcheck(result, func, args):
    if not func.ret_val_assertion(result): # return value could indicate error
        if func.use_last_error: # LastError should be consulted
            last_error = GetLastError()
            if last_error != 0:
                msg = "{}: {} ({})"
                raise OSError(msg.format(
                        func.name, FormatError(last_error), last_error))
        else: # raise exception without checking LastError
            msg = "{} returned bad value {}"
            raise OSError(msg.format(func.name, result))
    return result


def get_func(name, restype, args, ret_val_assertion=None, use_last_error=True):
    """Return a function pointer to a system DLL function.

    :param name: The name of the DLL function.
    :param restype: The return type of the function.
    :param args: A tuple of tuples of the form
        ``(param_type, flags, param_name, default_value)``. The last
        three elements of each tuple are optional; see
        `ctypes paramflags <https://docs.python.org/3/library/ctypes.html#function-prototypes>`
        for details.
    :param ret_val_assertion: A callable which returns false if the DLL
        function's return value could indicate an error condition. If
        so, the Windows ``LastError`` variable is used to determine if
        an error occurred, and an ``OSError`` is raised if appropriate.
    :param use_last_error: If False, ``LastError`` will not be checked
        to determine whether an error occurred. (Some functions do not
        use ``LastError`` to indicate error conditions.) In this case,
        ``ret_val_assertion`` alone will be used to determine whether
        an exception is raised.

    """

    # find first DLL which has a function with this name
    matching_dll = None
    for dll in _dlls:
        try:
            dll[name]
            matching_dll = dll
        except AttributeError: # function not found in this DLL
            pass
    if matching_dll is None:
        msg = ("could not find function with name '{}' "
                "(check for missing A/W suffix?)")
        raise NameError(msg.format(name))

    if args is None:
        argtypes = ()
        paramflags = ()
    else:
        argtypes = tuple([arg[0] for arg in args])
        paramflags = tuple([arg[1:] for arg in args])

    # get the function from DLL
    prototype = WINFUNCTYPE(restype, *argtypes)
    func = prototype((name, matching_dll), paramflags)

    # set function attributes for _errcheck
    func.name = name
    func.ret_val_assertion = ret_val_assertion
    func.use_last_error = use_last_error

    # enable error checking for function if error condition defined
    if ret_val_assertion is not None:
        if not callable(ret_val_assertion):
            msg = "return value assertion is not callable: '{}'"
            raise TypeError(msg.format(ret_val_assertion))
        else:
            func.errcheck = _errcheck

    # if function uses LastError, clear it before calling the function
    if use_last_error:
        return _clear_last_error_before(func)
    else:
        return func

