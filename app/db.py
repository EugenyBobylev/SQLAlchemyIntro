from _datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from config import Config

db_uri = Config.SQLALCHEMY_DATABASE_URI;
engine = create_engine(db_uri)
Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'
    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    jobdoctor = relationship("JobDoctor")


class IncartJob(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    snipet = Column(String(255))
    created = Column(DateTime, default=datetime.now)
    jobdoctor = relationship("JobDoctor")

class JobDoctor(Base):
    __tablename__ = 'jobsdoctors'
    job_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key=True)
    doctor = relationship("Doctor", back_populates='jobdoctor')
    job = relationship("IncartJob", back_populates ='jobdoctor')
