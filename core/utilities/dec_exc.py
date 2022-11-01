import copy
import functools


def exception_quiet(exception_return=None):
    def _exception_quiet(func):
        @functools.wraps(func)
        def _func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:  # pylint: disable=broad-except
                assert ex
                return exception_return

        return _func

    return _exception_quiet


def exception_safe(exception_return=None, keyword=None, return_filter=copy.copy):
    def _exception_safe(func):
        @functools.wraps(func)
        def _func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:  # pylint: disable=broad-except
                # pylint: disable=import-outside-toplevel
                from loguru import logger

                logger.error(keyword or func.__name__, {}, ex)
                if return_filter:  # pylint: disable=no-else-return
                    return return_filter(exception_return)
                else:
                    return exception_return

        return _func

    return _exception_safe
