import unittest
from typing import List

from app.db import dal, Doctor, IncartJob, JobDoctor, prep_db


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dal.conn_string = 'sqlite:///:memory:'
        dal.connect()
        dal.session = dal.Session()
        prep_db(dal.session)
        dal.session.close()

    def setUp(self):
        dal.session = dal.Session()

    def tearDown(self):
        dal.session.rollback()
        dal.session.close()

    def test_check_doctors_count(self):
        cnt = dal.session.query(Doctor).count()
        self.assertEqual(cnt, 2)

    def test_check_jobs_count(self):
        cnt = dal.session.query(IncartJob).count()
        self.assertEqual(cnt, 2)

    def test_check_jobdoctor_count(self):
        cnt = dal.session.query(JobDoctor).count()
        self.assertEqual(cnt, 2)

    def test_doctor1_relation(self):
        doc = dal.session.query(Doctor).filter(Doctor.id == 1).first()
        job_doctors: JobDoctor = doc.jobdoctor
        job = job_doctors[0].job

        self.assertIsNotNone(doc)
        self.assertIsNotNone(job_doctors)
        self.assertTrue(isinstance(job_doctors, List))
        self.assertTrue(len(job_doctors), 1)
        self.assertIsNotNone(job)
        self.assertTrue(isinstance(job, IncartJob))

    def test_jobdoctor_relation(self):
        job_doctor: JobDoctor = dal.session.query(JobDoctor).filter(JobDoctor.doctor_id == 1 and JobDoctor.job_id == 1).first()

        self.assertIsNotNone(job_doctor)
        self.assertTrue(isinstance(job_doctor.job, IncartJob))
        self.assertTrue(isinstance(job_doctor.doctor, Doctor))

    def test_job1_relation(self):
        job: IncartJob = dal.session.query(IncartJob).filter(IncartJob.id == 1).first()
        job_doctors = job.jobdoctor

        self.assertIsNotNone(job)
        self.assertTrue(isinstance(job, IncartJob))
        self.assertIsNotNone(job_doctors)
        self.assertTrue(isinstance(job_doctors, List))
        self.assertTrue(len(job_doctors), 2)


if __name__ == '__main__':
    unittest.main()
