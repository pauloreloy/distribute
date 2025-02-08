import functools
import logging
import traceback

def exception_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Capture and format the traceback
            tb = traceback.format_exc()
            # Log the error with traceback
            logging.error(f"Exception in {func.__name__}: {e}\nTraceback: {tb}")
            return None  # Or return a meaningful default value
    return wrapper