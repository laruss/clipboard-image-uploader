import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(var_name: str, var_type: type, default=None):
    value = os.getenv(var_name, default)
    if value == '':
        value = default
    return var_type(value)


class Env:
    UPLOAD_URL: str = get_env_var('UPLOAD_URL', str)

    if not UPLOAD_URL:
        raise ValueError('UPLOAD_URL is not set')

    TIME_DELTA: int = get_env_var('TIME_DELTA', int, 1)
    UPLOAD_FILE_KEY: str = get_env_var('UPLOAD_FILE_KEY', str, 'file')
    REQUEST_TIMEOUT: int = get_env_var('REQUEST_TIMEOUT', int, 60)


env = Env()
