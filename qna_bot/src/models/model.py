from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
import uuid

Base = declarative_base()

class BaseTable(Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)

class DataSourceType(Enum):
    API = 'API'
    DOCUMENT = 'DOCUMENT'
    WEBURL = 'WEBURL'

class User(BaseTable):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    data_spaces = relationship('DataSpace', back_populates='creator')
    bots = relationship('Bot', back_populates='creator')

class DataSpace(BaseTable):
    __tablename__ = 'data_spaces'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(1024))
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    creator = relationship('User', back_populates='data_spaces')
    data_sources = relationship('DataSource', back_populates='data_space')
    data_space_bots = relationship('DataSpaceBot', back_populates='data_space')

class DataSource(BaseTable):
    __tablename__ = 'data_sources'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(SQLEnum(DataSourceType), nullable=False)
    location = Column(String(1024), nullable=False)
    is_auth_required = Column(Boolean, default=False)
    data_space_id = Column(UUID(as_uuid=True), ForeignKey('data_spaces.id'), nullable=False)

    data_space = relationship('DataSpace', back_populates='data_sources')

class Bot(BaseTable):
    __tablename__ = 'bots'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    instruction = Column(String)
    llm_api_key = Column(String(255))
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    data_space_bots = relationship('DataSpaceBot', back_populates='bot')
    creator = relationship('User', back_populates='bots')

class DataSpaceBot(BaseTable):
    __tablename__ = 'data_space_bots'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_space_id = Column(UUID(as_uuid=True), ForeignKey('data_spaces.id'), nullable=False)
    bot_id = Column(UUID(as_uuid=True), ForeignKey('bots.id'), nullable=False)

    data_space = relationship('DataSpace', back_populates='data_space_bots')
    bot = relationship('Bot', back_populates='data_space_bots')