from types import SimpleNamespace
from contextvars import ContextVar

global_space = ContextVar("global_space", default=SimpleNamespace())
context = global_space.get()


def init_context() -> None:
    global_space.set(SimpleNamespace())
