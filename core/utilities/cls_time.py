from __future__ import absolute_import

import time


class TimeUtils:
    @classmethod
    def unix_timestamp(cls):
        return int(time.time())

    @classmethod
    def unix_seconds(cls):
        return time.time()

    @classmethod
    def unix_milliseconds(cls):
        return int(time.time() * 1000)


class Timer:
    @classmethod
    def _unix_ms(cls):
        return int(time.time() * 1000)

    @classmethod
    def _elapsed_ms_from(cls, _start_ms):
        return cls._unix_ms() - _start_ms

    def __init__(self):
        self._start_ms = None
        self._final_ms = None

    def __enter__(self):
        self._start_ms = self._unix_ms()
        return self

    def __exit__(self, *_args):
        self._final_ms = self.since_ms

    @property
    def start_ms(self):
        return self._start_ms

    @property
    def final_ms(self):
        return self._final_ms

    @property
    def since_ms(self):
        return self._elapsed_ms_from(self._start_ms)


class DictKeyTimer(Timer):
    def __init__(self, _dict, _key):
        super().__init__()
        self._dict = _dict
        self._key = _key

    def __enter__(self):
        super().__enter__()
        self._dict[self._key] = None
        return self

    def __exit__(self, *_args):
        super().__exit__()
        self._dict[self._key] = super(
            DictKeyTimer, self
        ).final_ms  # pylint: disable=super-with-arguments
