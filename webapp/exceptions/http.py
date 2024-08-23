from pydantic import BaseModel, ConfigDict


class HTTPError(BaseModel):
    detail: str

    model_config = ConfigDict(json_schema_extra={"examples": [{"detail": "HTTPException raised."}]})
