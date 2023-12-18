from sqlalchemy import Column, DateTime, Integer, MetaData, String
from sqlalchemy.orm import declarative_base

metadata = MetaData(schema="user_microservice")
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        String(120),
        nullable=False,
    )
    surname = Column(
        String(120),
        nullable=False,
    )
    email = Column(
        String(120),
        nullable=False,
        unique=True,
    )
    birthday = Column(
        DateTime,
        nullable=False,
    )
