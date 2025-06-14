import unittest
import asyncio
import time

from serial_asyncio import read_with_timeout

class DummyStreamReader:
    def __init__(self, data: bytes, delay: float = 0):
        self._data = data
        self._delay = delay
        self._index = 0

    async def read(self, n: int):
        if self._index >= len(self._data):
            await asyncio.sleep(self._delay)
            return b''
        await asyncio.sleep(self._delay)
        chunk = self._data[self._index:self._index + n]
        self._index += n
        return chunk


class TestReadWithTimeout(unittest.IsolatedAsyncioTestCase):
    async def test_reads_all_bytes_before_timeout(self):
        reader = DummyStreamReader(b'abcdef', delay=0)
        result = await read_with_timeout(reader, 6, 0.1)
        self.assertEqual(result, b'abcdef')

    async def test_reads_partial_bytes_due_to_timeout(self):
        reader = DummyStreamReader(b'abcdef', delay=0.01)
        start = time.time()
        result = await read_with_timeout(reader, 6, 0.03)
        elapsed = time.time() - start
        self.assertTrue(len(result) < 6)
        self.assertLessEqual(elapsed, 0.1)

    async def test_returns_empty_if_timeout_immediate(self):
        reader = DummyStreamReader(b'abcdef', delay=0)
        result = await read_with_timeout(reader, 6, 0)
        self.assertEqual(result, b'')

    async def test_reads_until_n_bytes(self):
        reader = DummyStreamReader(b'abcdef', delay=0)
        result = await read_with_timeout(reader, 3, 0.1)
        self.assertEqual(result, b'abc')

    async def test_handles_stream_end(self):
        reader = DummyStreamReader(b'', delay=0)
        result = await read_with_timeout(reader, 5, 0.1)
        self.assertEqual(result, b'')

if __name__ == "__main__":
    unittest.main()