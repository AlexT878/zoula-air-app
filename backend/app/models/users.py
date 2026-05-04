from sqlalchemy import Column, Date, Enum, Integer, String, Boolean, JSON, null
from app.constants.enums import Gender
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    country = Column(String, nullable=False)
    phone_country_code = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    roles = Column(JSON, default=["user"])
