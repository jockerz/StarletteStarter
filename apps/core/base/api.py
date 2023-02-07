import typing as t

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool = False
    errors: t.List[t.Any] = None
    data: t.Any
    pagination: t.Optional[t.Dict[str, int]] = None
