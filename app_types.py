from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

# todo: make it StrEnum
PayloadType = Literal['json', 'form', 'buffer']


# todo: make it StrEnum
UploadMethod = Literal['POST', 'PUT']


class ImageContentType(StrEnum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    WEBP = "image/webp"
    GIF = "image/gif"


class Notification(BaseModel):
    title: str
    subtitle: str
