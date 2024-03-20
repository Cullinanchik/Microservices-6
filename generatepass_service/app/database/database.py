from sqlalchemy import create_engine, String, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

class Password(Base):
    __tablename__ = 'generated_passwords_based'

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=False)
    password_type = Column(String, nullable=False)  # 'password' or 'passphrase'