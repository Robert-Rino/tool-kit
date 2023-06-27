import celery

from demo import models

@celery.shared_task(bind=True, ignore_resullt=False)
def get_username_by_id(task, user_id: str) -> dict:
    if not (user := models.User.objects.filter(id=user_id).first()):
        return 
    return user.username
