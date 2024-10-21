import threading
from PIL import ImageGrab, Image
import time
import hashlib
import io

import rest
import utils
from env import env
from logger import logger


notifications: list[dict[str, str]] = []


def process_image(image_bytes: bytes):
    for i in range(3):
        logger.info(f"Uploading content, attempt {i + 1}")
        result = rest.upload_content(
            image_bytes,
            url=env.UPLOAD_URL,
            upload_key=env.UPLOAD_FILE_KEY,
            timeout=env.REQUEST_TIMEOUT,
            login=env.LOGIN,
            password=env.PASSWORD,
            api_key=env.API_KEY
        )
        if result:
            logger.info("Content uploaded successfully")
            notifications.append(dict(title="Content uploaded", subtitle="Content was uploaded successfully"))
            break
        else:
            logger.warning("Failed to upload content")
    else:
        logger.error("Failed to upload content after 3 attempts")
        notifications.append(dict(title="Failed to upload content", subtitle="Failed to upload content after 3 attempts"))


def main():
    processed_hashes = set()

    while True:
        if len(notifications) > 0:
            for notification in notifications:
                utils.notify(title=notification["title"], subtitle=notification["subtitle"])
            notifications.clear()

        clipboard_content = ImageGrab.grabclipboard()
        if isinstance(clipboard_content, Image.Image):
            logger.debug("Image found in clipboard")
            image = clipboard_content
            width, height = image.size

            if width < env.MIN_SIDE_SIZE or height < env.MIN_SIDE_SIZE:
                logger.info("Image is too small, skipping...")
                time.sleep(env.TIME_DELTA)
                continue

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            image_hash = hashlib.sha256(image_bytes).hexdigest()
            if image_hash not in processed_hashes:
                logger.info("Image is unique, processing...")
                processed_hashes.add(image_hash)
                thread = threading.Thread(target=process_image, args=(image_bytes,))
                thread.start()

        time.sleep(env.TIME_DELTA)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bye bye!")
        exit(0)
