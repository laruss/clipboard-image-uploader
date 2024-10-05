import hashlib
import io
import platform
from urllib.parse import urlparse

from PIL import Image

from mac_notifications import client

from logger import logger


def is_valid_url(text: str):
    """Check if text is a valid URL."""
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except Exception as e:
        logger.error(f"Failed to validate URL: {e}")
        return False


def to_webp(image_bytes: bytes = None, image_path: str = None, max_size_in_kb: int = 500) -> bytes:
    """
    Convert image to WEBP format

    :param image_bytes: data of the image, if image is already in memory
    :param image_path: path to the image file, if image is on disk
    :param max_size_in_kb: maximum size of the image in KB
    :return: converted image bytes
    """
    IM_FORMAT = "WEBP"
    with Image.open(io.BytesIO(image_bytes) if image_bytes else image_path) as img:
        output = io.BytesIO()

        quality = 80
        img.save(output, format=IM_FORMAT, quality=quality)

        while output.tell() > max_size_in_kb * 1024:
            quality -= 10
            if quality < 10:
                break
            output.seek(0)
            output.truncate(0)
            img.save(output, format=IM_FORMAT, quality=quality)

        webp_image_bytes = output.getvalue()
        output.close()

        return webp_image_bytes


def get_hash(item: bytes | str) -> str:
    """Get hash of the item."""
    return hashlib.md5(item).hexdigest() if isinstance(item, bytes) else hashlib.md5(item.encode()).hexdigest()


def notify(title: str, subtitle: str):
    if (system := platform.system()) == "Darwin":
        client.create_notification(title=title, subtitle=subtitle)
    else:
        logger.warning(f"Notifications are not supported on {system}")
