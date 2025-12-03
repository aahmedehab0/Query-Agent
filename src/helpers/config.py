from dotenv import load_dotenv
from pydantic_settings import BaseSettings 


class Settings (BaseSettings):
    APP_NAME : str
    APP_VERSION : str
    CO_API_KEY: str
    FILE_DEFAULT_CHUNK_SIZE : int
    FILE_DEFAULT_OVERLAP_SIZE : int
    DATA_BASE_NAME : str
    QUESTION_EMBEDING_MODEL : str
    LOCAL_DEVICE : str
    GENERATION_MODEL : str
    EMBEDIBG_MODEL : str
    DSPY_MODEL : str
    LOCAL_DEVICE  : str
    TEMPERATURE : int
    CHUNK_SIZE : int
    OVERLAP_SIZE : int

    class config:
        env_file = '.env'

def get_settings ():
    load_dotenv()
    return Settings()