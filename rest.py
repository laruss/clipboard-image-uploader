import cloudscraper

from logger import logger
from app_types import Content


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
        content: Content,
        url: str,
        upload_key: str = 'file',
        timeout: int = 60,
        login: str = None,
        password: str = None,
        api_key: str = None,
) -> bool:
    """
    Upload content to the server

    :param content: Content, content to upload
    :param url: str, server url
    :param upload_key: str, key to use for the upload payload
    :param timeout: int, request timeout
    :param login: login, if required
    :param password: password, if required
    :param api_key: api key, if required
    :return: bool, True if content was uploaded successfully, False otherwise
    """
    session = cloudscraper.session()
    files = {upload_key: (content.name, content.data, content.mime_type)}
    if login and password:
        session.auth = (login, password)
    elif api_key:
        session.headers.update({'Authorization': f'Bearer {api_key}'})

    try:
        response = session.post(url, files=files, timeout=timeout)
        response.raise_for_status()
        logger.info(f"Content uploaded. Server response: status {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"Error uploading content: {e}")
        return False
