from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: SecretStr
    telegraph_token: SecretStr
    superuser_id: SecretStr
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
config = Settings()
superuser = int(config.superuser_id.get_secret_value())

