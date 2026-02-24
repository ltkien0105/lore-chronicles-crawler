from pathlib import Path
from pydantic import BaseModel
from requests import Response
import json


def write_content(filename, content) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def write_json_from_pydantic_model(
    path: str | Path, model: BaseModel, response: dict | Response
) -> None:
    if isinstance(response, Response):
        response = dict(response.json())
    validated_model = model.model_validate(response)

    with open(path, "w") as f:
        json.dump(
            validated_model.model_dump(exclude_none=True, by_alias=True), f, indent=4
        )

    return validated_model
