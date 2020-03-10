from typing import Dict, List, Optional, Union

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


ErrorMessageType = Union[str, Dict, List[Union[str, Dict]]]


def error_response(status_code: int, message: Optional[ErrorMessageType] = None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(
    message: ErrorMessageType = "Bad request",
) -> Dict[str, Union[int, ErrorMessageType]]:

    return error_response(400, message)
