"""
Models for tincture.views.generic tests
"""
from sqlalchemy import Column, Integer, String

from tests.db import Base


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
