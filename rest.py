import base64

import cloudscraper

from logger import logger
from app_types import PayloadType, UploadMethod, ImageContentType


def download_content(url: str, timeout: int = 60) -> bytes | None:
    """
    Download content from the server

    :param url: str, server url
    :param timeout: int, request timeout
    :return: bytes | None, content if downloaded successfully, None otherwise
    """
    session = cloudscraper.create_scraper()
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.error(f"Error downloading content: {e}")
        return None


def upload_content(
    image_data: bytes,
    url: str,
    token: str | None = None,
    credentials: tuple[str, str] | None = None,
    payload_type: PayloadType = 'json',
    upload_key: str = 'file',
    content_type: ImageContentType = ImageContentType.WEBP,
    upload_method: UploadMethod = 'POST',
    timeout: int = 60
):
    """
    Upload image to the server.

    :param image_data: bytes, data of the image to upload.
    :param url: str, server url.
    :param token: if passed, should be treated as a Bearer token.
    :param credentials: if passed, should be treated as a tuple of login and password for Basic Auth.
    :param payload_type: str, type of the payload.
    :param upload_key: str, key of the payload.
    :param content_type: str, type of the content, default is WEBP.
    :param upload_method: str, method of the upload. (POST, PUT)
    :param timeout: int, request timeout.
    """
    headers = {}
    auth = None
    session = cloudscraper.session()
    method = session.post if upload_method == 'POST' else session.put

    if token:
        headers['Authorization'] = f'Bearer {token}'
    if credentials:
        auth = (credentials[0], credentials[1])

    if payload_type == 'json':
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        payload = {upload_key: image_b64}
        post_data = dict(json=payload)
    elif payload_type == 'form':
        files = {upload_key: ('filename', image_data, content_type)}
        post_data = dict(files=files)
    elif payload_type == 'buffer':
        headers['Content-Type'] = content_type
        post_data = dict(data=image_data)
    else:
        raise ValueError("Unknown payload type")

    try:
        response = method(url, headers=headers, auth=auth, timeout=timeout, **post_data)
        response.raise_for_status()
        logger.info(f"Content uploaded. Server response: status {response.status_code}")
    except Exception as e:
        logger.error(f"Error uploading content: {e}")
        return False

    return True
