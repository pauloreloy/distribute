import logging
import traceback


def exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            logging.error(f"Exception in {func.__name__}: {args}{kwargs}\n{e}\nTraceback: {tb}")
            return None
    return wrapper