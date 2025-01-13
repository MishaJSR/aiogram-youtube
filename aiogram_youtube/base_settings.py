from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TG_KEY: str
    USER_BOT_ID: int

    def get_token(self):
        return self.TG_KEY

    def get_user_bot_id(self):
        return self.USER_BOT_ID


base_settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
