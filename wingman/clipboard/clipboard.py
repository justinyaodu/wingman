"""System clipboard interface."""

__all__ = ['Clipboard', 'selection', 'primary', 'secondary']

from abc import ABC, abstractmethod
import logging

_logger = logging.getLogger(__name__)


# clipboard instances by type
# values are set by OS-specific modules
selection = None
primary = None
secondary = None


class Clipboard(ABC):
    """Abstract base class for clipboards."""

    def __init__(self):
        # configurable maximum size for objects transferred to/from clipboard
        # used by subclasses
        self.max_data_size = 64 * 1024 * 1024

    @abstractmethod
    def clear(self):
        """Clear the contents of the clipboard."""
        pass

    @abstractmethod
    def available_formats(self):
        """Return a list of MIME types, which indicate what data
        formats the clipboard data can be retrieved in.
        """
        pass

    @abstractmethod
    def _get_data_single(self, mime_type):
        """Return the clipboard contents in the specified format."""
        pass

    def get_data(self, *mime_types):
        """Return the clipboard contents in the first available of the
        specified formats. Return type will be a string or a bytes
        object, depending on the format. None is returned if none of
        the requested formats are available.
        """
        available = self.available_formats()
        for mime_type in mime_types:

            if mime_type not in available:
                msg = "Clipboard data not available in format '{}', skipping"
                _logger.debug(msg.format(mime_type))
                continue

            result = self._get_data_single(mime_type)
            if result is not None:
                return result
            else:
                msg = ("Failed to retrieve clipboard data in format '{}', "
                        "skipping")
                _logger.warning(msg.format(mime_type))

        msg = ("Could not retrieve clipboard data in any of the specified "
                "formats")
        _logger.debug(msg)
        return None

    @abstractmethod
    def _set_data_single(self, mime_type, data):
        """Add data to the clipboard in a single format."""
        pass

    def set_data(self, *data_items):
        """Set the clipboard data in one or more formats, with the most
        preferred formats first (i.e. formatted text before plaintext).
        Each argument is a ``(mime_type, data)`` tuple, where ``data``
        is a bytes object or string. Clears existing clipboard contents
        beforehand.
        """
        self.clear()
        for data_item in data_items:
            if not isinstance(data_item, tuple):
                msg = "Argument should be a tuple; got {} instead."
                raise TypeError(msg.format(type(data_item).__name__))

            mime_type = data_item[0]
            if not isinstance(mime_type, str):
                msg = "First tuple item should be a string; got {} instead."
                raise TypeError(msg.format(type(mime_type).__name__))

            data = data_item[1]
            if not (isinstance(data, str) or isinstance(data, bytes)):
                msg = ("Second tuple item should be a bytes object or string; "
                        "got {} instead.")
                raise TypeError(msg.format(type(data).__name__))

            self._set_data_single(mime_type, data)

    def save_state(self):
        """Return an object representing the current contents of the
        clipboard, so that the current contents can be restored later.
        Note that this will not work perfectly in all cases; if the
        clipboard contents depend on application resources which are
        freed when the application loses ownership of the clipboard,
        unexpected behaviour may result.
        """
        data_items = []
        for f in self.available_formats():
            data = self._get_data_single(f)
            if data is not None:
                data_items.append((f, data))
        return data_items

    def restore_state(self, state):
        """Restore the clipboard state from a clipboard state object
        previously returned by ``save_state``.
        """
        self.set_data(*state)

