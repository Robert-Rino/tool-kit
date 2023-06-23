class Config:
    CELERY = {
        'broker_url': 'redis://redis',
        'result_backend': 'redis://localhost',    
    }

    MONGODB_SETTINGS = {
        'host': 'mongodb://mongo/dev'
    }
