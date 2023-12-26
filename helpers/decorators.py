import logging
from functools import wraps
from typing import Any, Callable, Iterable, TypeVar

from rest_framework.exceptions import NotFound

RT = TypeVar("RT")

logger = logging.getLogger(__name__)


def except_shell(
    errors: Iterable = (Exception,),
    default_value: Any = None,
    raise_404: bool = False,
) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    def decorator(func: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> RT:
            try:
                return func(*args, **kwargs)
            except errors as e:
                logging.error(e)
                if raise_404:
                    raise NotFound("Запрошенный объект не найден")
                return default_value

        return wrapper

    return decorator
