import functools
from src.strategies.context import Context


def make_strategy(strategy: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            try:
                context_strategy = Context(strategy)
                return context_strategy
            except Exception:
                return False
        return wrapper
    return decorator