import cloudscraper

from logger import logger
from app_types import Content


def download_content(url: str, timeout: int = 60) -> bytes | None:
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
        timeout: int = 60
) -> bool:
    session = cloudscraper.session()
    files = {upload_key: (content.name, content.data, content.mime_type)}

    try:
        response = session.post(url, files=files, timeout=timeout)
        response.raise_for_status()
        logger.info(f"Content uploaded. Server response: status {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"Error uploading content: {e}")
        return False
