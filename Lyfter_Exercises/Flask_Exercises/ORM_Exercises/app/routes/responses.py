""" Success responses """

from collections.abc import Iterable
from http import HTTPStatus
from typing import Any

from pydantic import BaseModel

type ResponseTuple = tuple[dict[str, Any] | str, HTTPStatus, dict[str, str]]

def serialize(schema: type[BaseModel], obj: Any) -> dict[str, Any]:
    """ Convert one object to JSON data using an output schema """
    return schema.model_validate(obj).model_dump(mode="json")


def serialize_many(schema: type[BaseModel], objs: Iterable[Any]) -> list[dict[str, Any]]:
    return [serialize(schema, obj) for obj in objs]


def ok(data: Any, headers: dict[str, str] | None = None) -> ResponseTuple:
    """ 200 OK with a body """
    return {"data": data}, HTTPStatus.OK, headers or {}


def created(data: Any, location: str) -> ResponseTuple:
    """ 201 Created: always says where the new resource lives """
    return {"data": data}, HTTPStatus.CREATED, {"location": location}


def no_content() -> ResponseTuple:
    """ 204 No Content: success with an empty body (DELETE) """
    return "", HTTPStatus.NO_CONTENT, {}