"""Sample API Client."""
import asyncio
import logging

import aiohttp
import async_timeout

from typing import Optional

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class BenqSerialApiClient:
    def __init__(
        self, host: str, port: int, session: aiohttp.ClientSession
    ) -> None:
        """Sample API Client."""
        self._host = host
        self._port = port
        self._session = session
        self._reader = None
        self._writer = None
        self._lock = asyncio.Lock()

    async def _init_reader_writer(self):
        if self._reader is None or self._writer is None:
            self._reader, self._writer = await asyncio.open_connection(
                self._host, self._port
            )

    async def async_get_data(self, key: str) -> Optional[str]:
        """Get data from the API."""
        try:
            return await self._query(key, "?")
        except ValueError:
            return None

    async def async_set_data(self, key: str, value: str) -> None:
        """Get data from the API."""
        await self._query(key, value)

    async def _read_until_key_found(self, key: str) -> str:
        def get_value(data, key):
            for line in data.decode(encoding='ascii').splitlines():
                if line == '*Block item#':
                    # query blocked on device side
                    raise ValueError()
                line = line.lower()
                if not line.startswith(f'*{key}=') \
                        or not line.endswith('#'):
                    continue
                return line.split('=')[-1].strip('#')
            # key not yet found
            raise KeyError()

        BATCH_SIZE = 100
        data = b''
        while True:
            batch = await self._reader.read(BATCH_SIZE)
            data += batch
            try:
                return get_value(data, key)
            except ValueError:
                _LOGGER.warn(f"Key {key} not available")
                raise
            except KeyError:
                pass

    async def _query(self, key: str, value: str) -> str:
        """Get information from the API."""
        sentence = f"\r*{key}={value}#\r"
        try:
            async with async_timeout.timeout(TIMEOUT), self._lock:
                await self._init_reader_writer()
                self._writer.write(sentence.encode(encoding='ascii'))
                await self._writer.drain()

                val = await self._read_until_key_found(key)

                _LOGGER.warn(f"_query: {val}")
                return val

        except asyncio.TimeoutError:
            _LOGGER.error(
                f"Timeout error fetching data from {self._host}:{self._port}"
            )

        except ValueError:
            raise

        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
