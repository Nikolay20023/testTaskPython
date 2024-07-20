from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn



class Setting(BaseSettings):
    database_dsn: PostgresDsn
    project_host: str
    project_port: int
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    api_key: str
    api_url_geocode: str
    api_urL_open_meteo: str

    
    model_config = SettingsConfigDict(env_file=".env")
    


app_setting = Setting()