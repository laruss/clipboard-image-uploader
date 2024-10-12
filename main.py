import time

import clipboard
import rest
import utils
from env import env
from logger import logger
from app_types import OptionalClipboardItem, ClipContentType, ClipboardItem, Content

current_clipboard: OptionalClipboardItem = None
is_error = False
dots_waited = 0
DOTS_TO_WAIT = 20


def main():
    global current_clipboard, dots_waited

    new_clipboard = clipboard.get_content()
    if new_clipboard and (not current_clipboard or (current_clipboard.hash != new_clipboard.hash)):
        dots_waited = 0
        logger.info("New content found in clipboard")
        if new_clipboard.type == ClipContentType.URL:
            result = rest.download_content(url=new_clipboard.content, timeout=env.REQUEST_TIMEOUT)
            if not result:
                logger.warning(f"Failed to download content from {new_clipboard.content}, skipping...")
                return

            clip = ClipboardItem(
                type=ClipContentType.IMAGE,
                content=utils.to_webp(result),
                hash=''  # hash does not matter here
            )
        else:
            clip = new_clipboard

        content = Content(data=clip.content, mime_type='image/webp', name='image.webp')
        for i in range(3):
            logger.info(f"Uploading content, attempt {i + 1}")
            result = rest.upload_content(
                content,
                url=env.UPLOAD_URL,
                upload_key=env.UPLOAD_FILE_KEY,
                timeout=env.REQUEST_TIMEOUT,
                login=env.LOGIN,
                password=env.PASSWORD,
                api_key=env.API_KEY
            )
            if result:
                logger.info("Content uploaded successfully")
                utils.notify(title="Content uploaded", subtitle="Content was uploaded successfully")
                break
            else:
                logger.warning("Failed to upload content")
        else:
            logger.error("Failed to upload content after 3 attempts")
            utils.notify(title="Failed to upload content", subtitle="Failed to upload content after 3 attempts")

        current_clipboard = new_clipboard

    else:
        if dots_waited >= DOTS_TO_WAIT - 1:
            print('.')
            dots_waited = 0
        else:
            print('.', end='', flush=True)
            dots_waited += 1
        time.sleep(env.TIME_DELTA)


if __name__ == "__main__":
    logger.info("Starting...")
    while True:
        try:
            main()
            is_error = False
        except KeyboardInterrupt:
            logger.info("Exiting...")
            exit()
        except Exception as e:
            if not is_error:
                utils.notify(title="Error", subtitle=f"An error occurred: {e}")
                is_error = True
            pass
