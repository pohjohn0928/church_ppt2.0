from mysql import Base
from sqlalchemy import Column, String, Integer, DATETIME


class Receiver(Base):
    __tablename__ = 'receiver'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    upload_time = Column(DATETIME, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
