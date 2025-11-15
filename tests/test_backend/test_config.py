import os
import importlib.util


def load_settings():
    spec = importlib.util.spec_from_file_location("config", "backend/app/core/config.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Settings


def test_database_url_env_override():
    os.environ["DATABASE_URL_ENV"] = "sqlite:///./pokedex_test.db"
    Settings = load_settings()
    settings = Settings()
    assert settings.database_url == "sqlite:///./pokedex_test.db"