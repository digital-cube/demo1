from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from base import orm


class Contact(orm.BaseSql, orm.sql_base):
    __tablename__ = 'contacts'

    id_owner = Column(UUID, nullable=False, index=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

