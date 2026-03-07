from pydantic_settings import BaseSettings
import dotenv
dotenv.load_dotenv()

class Settings(BaseSettings):
    """Loads environment configuration"""

    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: str
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: str


settings = Settings()