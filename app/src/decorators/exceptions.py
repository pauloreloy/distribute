import functools
import logging


def exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Exception in {func.__name__}: {e}")  # Log instead of stopping execution
            return None  # Or return a meaningful default value
    return wrapper