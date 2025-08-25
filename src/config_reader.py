from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

ROOT_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    SUPABASE_URL: SecretStr
    SUPABASE_KEY: SecretStr
    SUPABASE_SERVICE_KEY: SecretStr
    ADMIN_USER_IDS: str = ""  # Comma-separated list of admin user IDs
    LOG_GROUP_ID: str = ""  # Group chat ID for logging anonymous messages
    
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8"
    )


config = Config()

def get_admin_user_ids() -> list[int]:
    """Get list of admin user IDs from config"""
    if not config.ADMIN_USER_IDS:
        return []
    return [int(uid.strip()) for uid in config.ADMIN_USER_IDS.split(',') if uid.strip()]

def is_admin_user(user_id: int) -> bool:
    """Check if user is an admin"""
    return user_id in get_admin_user_ids()
