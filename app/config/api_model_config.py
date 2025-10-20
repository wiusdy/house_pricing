from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class APIPredictConfig(BaseSettings):
    demographics_path: str
    model_path: str
    model_features_path: str
    model_version: str
    feature_to_join: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )