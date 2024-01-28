from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, CHAR, Boolean


from sqlalchemy.dialects.postgresql import UUID, INTEGER, ARRAY, JSONB, INET

from database import Base
import uuid
import datetime


class UserRecord(Base):
    __tablename__ = "user_record"

    id = Column(UUID, primary_key=True, index=True, unique=True)

    created_at = Column(DateTime)
    last_login = Column(DateTime)
    updated_at = Column(DateTime)

    last_IP_origin = Column(CHAR(2), nullable=True)

    folders = Column(JSONB)
    tags = Column(JSONB)

    def __init__(self, folders, tags, origin=None):
        self.id = uuid.uuid4()
        self.created_at = datetime.datetime.now()
        self.last_login = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.last_IP_origin = origin
        self.folders = folders
        self.tags = tags

    def __repr__(self):
        return f"<UserRecord(id={self.id}, created_at={self.created_at}, last_login={self.last_login}, updated_at={self.updated_at}, last_IP_origin={self.last_IP_origin}, folders={self.folders}, tags={self.tags})>"

    def __iter__(self):
        yield 'id', self.id
        yield 'created_at', self.created_at
        yield 'last_login', self.last_login
        yield 'updated_at', self.updated_at
        yield 'last_IP_origin', self.last_IP_origin
        yield 'folders', self.folders
        yield 'tags', self.tags


class IP_logger(Base):
    __tablename__ = "ip_logger"

    id = Column(INTEGER, autoincrement=True, primary_key=True, index=True, unique=True)
    ipaddress = Column(CHAR(15), nullable=False)
    # requested at is the time the request was made, always the current time by default
    requested_at = Column(DateTime, nullable=False)
