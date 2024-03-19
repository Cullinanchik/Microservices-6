from sqlalchemy import Column, Integer, String, DateTime, func
from database.database import Base

class GeneratedPassword(Base):
    __tablename__ = 'generated_passwords'

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=False)
    password_type = Column(String, nullable=False)  # 'password' or 'passphrase'
    created_at = Column(DateTime, default=func.now())
