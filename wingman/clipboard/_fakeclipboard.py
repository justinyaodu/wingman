"""Fake system clipboard implementation, intended for testing.
"""

__all__ = []

from collections import OrderedDict

from . import clipboard


class FakeClipboard(clipboard.Clipboard):
    """Fake clipboard implementation."""

    def __init__(self):
        super().__init__()
        self.data_by_type = OrderedDict()

    def clear(self):
        self.data_by_type.clear()

    def available_formats(self):
        return list(self.data_by_type.keys())

    def _get_data_single(self, mime_type):
        return self.data_by_type[mime_type]

    def _set_data_single(self, mime_type, data):
        self.data_by_type[mime_type] = data


clipboard.primary = FakeClipboard()

