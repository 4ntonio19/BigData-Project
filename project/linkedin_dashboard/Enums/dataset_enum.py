from enum import Enum


class DatasetName(Enum):
    JOB_POSTINGS = "job_postings"
    JOB_SKILLS = "job_skills"
    SKILLS = "skills"
    PREDICT_JOB_POSTINGS_2025 = "predict_job_postings_2025"
    PREDICT_JOB_POSTINGS_IT  = 'predict_job_postings_it'
    PREDICT_JOB_POSTINGS_QA  = 'predict_job_postings_qa'
    PREDICT_JOB_POSTINGS_PRDM  = 'predict_job_postings_prdm'
    PREDICT_JOB_POSTINGS_DSGN  = 'predict_job_postings_dsgn'
