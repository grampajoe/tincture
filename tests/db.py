"""
Utilites for testing tincture with SQLAlchemy.

This is a temporary solution for initial testing of tincture. In the future,
tincture should have its own set of testing utilities to be used when testing
applications, not only tincture itself.

Accomplishing this generic testing interface will involve a deeper integration
of SQLAlchemy into the Django framework so we can do things like create an
engine and session directly from Django config.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Use an in-memory database to avoid teardown complication.
engine = create_engine('sqlite:///:memory:')
session = sessionmaker(bind=engine)()


# Create a Base class here for now.
Base = declarative_base()


def setup_environment():
    """Set up the SQLAlchemy environment."""
    Base.metadata.create_all(engine)
