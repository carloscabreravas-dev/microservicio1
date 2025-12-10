"""
Configuración de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Base de datos
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "microservicio"
    
    # Aplicación
    DEBUG: bool = False
    APP_NAME: str = "Microservicio API"
    API_VERSION: str = "1.0.0"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    @property
    def DATABASE_URL(self) -> str:
        """Construir URL de base de datos a partir de variables individuales"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
