class Config:
    CELERY = {
        'broker_url': 'redis://redis',
        'result_backend': 'redis://redis',    
    }

    MONGODB_SETTINGS = {
        'host': 'mongodb://mongo/dev'
    }
