from sqlalchemy import create_engine, String, UUID, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

class Pet(Base):
    __tablename__ = 'pets_pavlovid'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
    favorite_delicacy = Column(String)
    weight = Column(Integer)
    age = Column(Integer)
    favorite_activity = Column(String)
