"""
Ryan Faulkner, 2014

Schema definitions for sqlalchemy
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class Model(Base):

    __tablename__ = 'Models'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    name = Column(String)

    def __repr__(self):
        return "<Model(name='%s', uid='%s')>" % (
            self.name, self.uid)