import io

import pyperclip
from PIL import ImageGrab, Image

import utils
from logger import logger
from app_types import ClipboardItem, OptionalClipboardItem, ClipContentType


def get_content() -> OptionalClipboardItem:
    """ Get content from the clipboard. """
    if image := _get_image():
        buffered = io.BytesIO()
        image.save(buffered, format='PNG')
        image_bytes = buffered.getvalue()
        image_bytes = utils.to_webp(image_bytes)

        return ClipboardItem(
            type=ClipContentType.IMAGE,
            content=image_bytes,
            hash=utils.get_hash(image_bytes),
        )

    elif text := _get_text():
        return ClipboardItem(type=ClipContentType.URL, content=text, hash=utils.get_hash(text))

    else:
        return None


def _get_image() -> Image.Image | None:
    """ Try to get an image from the clipboard. """
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            return image
    except Exception as e:
        logger.error(f"Failed to get image from clipboard: {e}")
    return None


def _get_text() -> str | None:
    """
    Get text from the clipboard and check if it is a valid URL.

    :return: str | None - URL or None
    """
    current_text = pyperclip.paste()
    if utils.is_valid_url(current_text):
        return current_text
    return None
