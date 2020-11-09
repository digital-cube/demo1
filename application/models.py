from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from base import orm


class Storage(orm.BaseSql, orm.sql_base):
    __tablename__ = 'storage'

    id = Column(UUID, primary_key=True)

    key = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)


