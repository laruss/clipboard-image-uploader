import threading
from PIL import ImageGrab, Image
import time
import hashlib
import io

import rest
import utils
from env import env
from logger import logger
from app_types import Notification

from pynput import keyboard

notifications: list[Notification] = []
IS_ACTIVE = False


def on_activate():
    global IS_ACTIVE
    IS_ACTIVE = not IS_ACTIVE
    caption = "is active" if IS_ACTIVE else "is not active"
    logger.info(f"Hotkey activated, IS_ACTIVE: {IS_ACTIVE}")
    notifications.append(Notification(title="Hotkey activated", subtitle=f"Now it's {caption}"))


def process_image(image_bytes: bytes):
    image_bytes = utils.to_webp(image_bytes=image_bytes)

    for i in range(3):
        logger.info(f"Uploading content, attempt {i + 1}")
        result = rest.upload_content(
            image_data=image_bytes,
            url=env.UPLOAD_URL,
            token=env.API_KEY,
            credentials=(env.LOGIN, env.PASSWORD),
            payload_type=env.UPLOAD_PAYLOAD_TYPE,
            upload_key=env.UPLOAD_FILE_KEY,
            upload_method=env.UPLOAD_METHOD,
            timeout=env.REQUEST_TIMEOUT,
        )
        if result:
            logger.info("Content uploaded successfully")
            notifications.append(Notification(title="Content uploaded", subtitle="Content was uploaded successfully"))
            break
        else:
            logger.warning("Failed to upload content")
    else:
        logger.error("Failed to upload content after 3 attempts")
        notifications.append(Notification(title="Failed to upload content", subtitle="Failed to upload content after 3 attempts"))


def main():
    processed_hashes = set()

    while True:
        if len(notifications) > 0:
            for nt in notifications:
                utils.notify(title=nt.title, subtitle=nt.subtitle)
            notifications.clear()

        if not IS_ACTIVE:
            time.sleep(env.TIME_DELTA)
            continue

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
    logger.info("Starting the app...")
    keyboard.GlobalHotKeys({'<ctrl>+<alt>+i': on_activate}).start()
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bye bye!")
        exit(0)
