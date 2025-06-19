from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = "region"

    id = Column(BigInteger, primary_key=True, index=True)
    main_id = Column(Integer, nullable=False)
    main = Column(String(10), nullable=False)
    sub = Column(String(10), nullable=False)


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    region_id = Column(BigInteger, ForeignKey("region.id"), nullable=False)
    name = Column(String, index=True)
    user_id = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    pet_type = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False, default=1)
    created_at = Column(DATETIME, nullable=False)
