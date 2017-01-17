from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    created = Column(DateTime, server_default=func.now())


class Garden(Base):
    __tablename__ = 'garden'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    garden_type = Column(String(250), nullable=False)
    location = Column(String(250))
    created = Column(DateTime, server_default=func.now())
    comments = Column(String)
    user_id = Column(String, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'garden_type': self.garden_type,
            'location': self.location,
            'comments': self.comments,
            'created': self.created,
            }


class Plant(Base):
    __tablename__ = 'plant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    plant_type = Column(String(250), nullable=False)
    date_planted = Column(DateTime, server_default=func.now())
    comments = Column(String)
    user_id = Column(String, ForeignKey('user.id'))
    user = relationship(User)
    garden_id = Column(String, ForeignKey('garden.id'))
    garden = relationship(Garden)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'plant_type': self.plant_type,
            'date_planted': self.date_planted,
            'comments': self.comments,
            'garden_id': self.garden_id,
            }


engine = create_engine('sqlite:///marketgardenlog.db')

Base.metadata.create_all(engine)
