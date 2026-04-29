from typing import Any, Callable, TypeVar


T = TypeVar("T")


def run_safely(
    function: Callable[..., T],
    *args: Any,
    fallback: T,
    **kwargs: Any,
) -> tuple[T, Exception | None]:
    """
    Run a function safely.

    Returns:
    - result
    - error object if something failed, otherwise None
    """
    try:
        return function(*args, **kwargs), None
    except Exception as error:
        print(f"\nSystem warning: {function.__name__} failed.")
        return fallback, error
