from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class EnvSettings(BaseSettings):
    environment: str


class DatasetSettings(BaseSettings):
    job_postings_path: str
    job_skills_path: str
    skills_path: str
    company_specialities_path: str


class GeoSettings(BaseSettings):
    brazil_geo: str
    united_states_geo: str


class Settings(BaseSettings):
    env_settings: EnvSettings = EnvSettings()
    dataset_settings: DatasetSettings = DatasetSettings()
    geo_settings: GeoSettings = GeoSettings()

    class Config:
        extra = "forbid"


@lru_cache
def get_settings():
    return Settings()
