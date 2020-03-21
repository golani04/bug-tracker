from functools import wraps
from typing import Callable, Dict, Set, Union
from flask import request

from backend.models.projects import Project
from .errors import bad_request, not_found


def check_requested_data(route_func: Callable) -> Callable:
    @wraps(route_func)
    def wrapper() -> Dict:
        data = request.get_json()
        error_msg = ""

        if data is None:
            error_msg = "Provided data is not a json."
        elif not data:
            error_msg = "Received json is empty."

        if error_msg:
            return bad_request(error_msg)

        return route_func(data)

    return wrapper


def check_required_keys(required_keys: Set) -> Callable:
    def wrapper(route_func: Callable) -> Callable:
        @wraps(route_func)
        def inner_wrapper(data: Dict) -> Dict:
            if not required_keys <= set(data):
                keys = sorted(required_keys - set(data))
                return bad_request(
                    f"Missing required key{'s' if len(keys) > 1 else ''}: {', '.join(keys)}."
                )

            return route_func(data)

        return inner_wrapper

    return wrapper


def check_item_exists(model: Union[Project], error_msg: str) -> Callable:
    def wrapper(route_func: Callable) -> Callable:
        @wraps(route_func)
        def inner_wrapper(project_id: str, *args, **kwargs) -> Union[Project]:
            item = model.find_by_id(project_id)
            if item is None:
                return not_found(error_msg)

            return route_func(item, *args, **kwargs)

        return inner_wrapper

    return wrapper