from dataclasses import dataclass
from enum import Enum


@dataclass
class Content:
    """ Content to upload """
    data: bytes
    mime_type: str
    name: str


class ClipContentType(Enum):
    URL = "url"
    IMAGE = "image"


@dataclass
class ClipboardItem:
    """ Current clipboard item """
    type: ClipContentType
    content: str | bytes
    hash: str


OptionalClipboardItem = ClipboardItem | None
