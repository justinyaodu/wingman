import unittest

from wingman.winutil import globalmem

class TestGlobalMem(unittest.TestCase):
    def test_size_of(self):
        handle = globalmem.copy_to_global(b"0123456789")
        self.assertEqual(globalmem.size_of(handle), 10)
        globalmem.free(handle)

    def test_copy_bytes(self):
        some_bytes = b"I contain a \0 so I can't be handled as a string!"
        handle = globalmem.copy_to_global(some_bytes)
        self.assertEqual(some_bytes, globalmem.copy_from_global(handle))
        globalmem.free(handle)

    def test_no_encoding_exception(self):
        with self.assertRaises(ValueError):
            handle = globalmem.copy_to_global("no encoding specified")
            globalmem.free(handle)

    def test_copy_invalid_type(self):
        with self.assertRaises(TypeError):
            handle = globalmem.copy_to_global(["a", "list"])
            globalmem.free(handle)

    def test_copy_utf8_string(self):
        string = "I contain non-ASCII characters: 你好!"
        encoding = 'UTF-8'
        handle = globalmem.copy_to_global(string, encoding)
        self.assertEqual(string, globalmem.copy_from_global(handle, encoding))
        globalmem.free(handle)

    def test_copy_utf16_string(self):
        string = "More non-ASCII characters: 再见!"
        encoding = 'UTF-16'
        handle = globalmem.copy_to_global(string, encoding)
        self.assertEqual(string, globalmem.copy_from_global(handle, encoding))
        globalmem.free(handle)

