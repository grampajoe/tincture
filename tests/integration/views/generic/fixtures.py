"""
Fixtures for generic views tests.
"""
from fixture import DataSet


class PersonData(DataSet):
    class John(object):
        name = 'John Smith'
