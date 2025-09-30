
import os

class Config:

    TOKEN_VALIDATE_URL = os.environ.get("TOKEN_VALIDATE_URL", "http://127.0.0.1:8000/api/v1/auth/validate-token/")

    MS_ORDEM_SERVICE_URL = os.environ.get("MS_ORDEM_SERVICE_URL", "http:// ")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             "postgresql+psycopg2://postgres:12345@localhost:5432/equipes-tecnicas")
