from pydantic import BaseModel


class CommonResponse(BaseModel):
    success: bool = True
    status_code: int = 200
    message: str | None = None
    data: dict | list | None = None
