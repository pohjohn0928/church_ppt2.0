from pydantic import BaseSettings


class DBSettings(BaseSettings):
    # HOST: str = '124.221.251.102'
    # HOST: str = '116.205.184.4'
    HOST: str = '127.0.0.1'
    DB_USER: str = 'root'
    DB_PASSWORD: str = 'poh88990928'
    DB_PORT: int = 3306
    DB_NAME: str = 'ChurchPPT'
    DB_URL: str = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{HOST}:{DB_PORT}/{DB_NAME}'