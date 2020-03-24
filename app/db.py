from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, session

from config import Config

Base = declarative_base()


class DataAccessLayer():
    def __init__(self):
        self.engine = None
        self.session: session.Session = None
        self.conn_string = Config.SQLALCHEMY_DATABASE_URI

    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


dal = DataAccessLayer()


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
    created = Column(DateTime, default=datetime.now().astimezone(timezone.utc))
    jobdoctor = relationship("JobDoctor")


class JobDoctor(Base):
    __tablename__ = 'jobsdoctors'
    job_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key=True)
    request_id = Column(String(16))
    request_sended = Column(DateTime)

    doctor = relationship("Doctor", back_populates='jobdoctor')
    job = relationship("IncartJob", back_populates ='jobdoctor')


def prep_db(session: session.Session):
    doctor1 = Doctor(name='Айболит')
    doctor2 = Doctor(name='Сеченов')
    session.bulk_save_objects([doctor1, doctor2])
    session.commit()

    job1 = IncartJob(snipet='job_1')
    job2 = IncartJob(snipet='job_2')
    session.bulk_save_objects([job1, job2])
    session.commit()

    job_doctor: JobDoctor = JobDoctor(job_id=1, doctor_id=1)
    job_doctor.request_id = '1'
    session.add(job_doctor)
    session.commit()

    job_doctor2 = JobDoctor(job_id=1, doctor_id=2)
    job_doctor2.request_id = '2'
    job_doctor2.request_sended = datetime.utcnow()
    session.add(job_doctor2)
    session.commit()
