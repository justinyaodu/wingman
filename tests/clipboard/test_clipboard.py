import unittest

from wingman.clipboard import primary

mime_plaintext = 'text/plain'
mime_bytes = 'application/octet-stream'

class TestClipboard(unittest.TestCase):
    def test_clear(self):
        primary.set_data((mime_plaintext, "Hello!"))
        primary.clear()
        self.assertEqual(len(primary.available_formats()), 0)

    def test_get_plaintext(self):
        text = "Hello! Here's an avocado: 🥑"
        primary.set_data((mime_plaintext, text))
        self.assertEqual(primary.get_data(mime_plaintext), text)

    def test_get_bytes(self):
        some_bytes = b'Throw in a \0 and see if anything breaks.'
        primary.set_data((mime_bytes, some_bytes))
        self.assertEqual(primary.get_data(mime_bytes), some_bytes)

    def test_set_data_clears_previous(self):
        primary.set_data((mime_plaintext, "I should be cleared in a moment."))
        primary.set_data((mime_bytes, b'I should be alone on the clipboard.'))
        self.assertFalse(mime_plaintext in primary.available_formats())

    def test_get_unavailable_format(self):
        text = "I am text."
        primary.set_data((mime_plaintext, text))
        self.assertEqual(primary.get_data(mime_bytes, mime_plaintext), text)

    def test_format_ordering(self):
        primary.set_data((mime_plaintext, "text"), (mime_bytes, b'bytes'))
        self.assertEqual(
                primary.available_formats(),
                [mime_plaintext, mime_bytes])

    def test_requested_format_returned(self):
        some_bytes = b'These are the bytes you want.'
        primary.set_data((mime_plaintext, "Not me!"), (mime_bytes, some_bytes))
        self.assertEqual(primary.get_data(mime_bytes), some_bytes)

