from dotenv import load_dotenv
from pydantic_settings import BaseSettings 


class Settings (BaseSettings):
    APP_NAME : str
    APP_VERSION: str
    CO_API_KEY_API_KEY : str
    FILE_DEFAULT_CHUNK_SIZE : int
    FILE_DEFAULT_OVERLAP_SIZE : int
    DATA_BASE_NAME : str

    class config:
        env_file = '.env'

def get_setings ():
    load_dotenv()
    return Settings()