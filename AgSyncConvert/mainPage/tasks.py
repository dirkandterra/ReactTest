# mainPage/tasks.py

from datetime import timedelta
from celery.utils.log import get_task_logger
from celery.task import periodic_task
from .models import AgSyncCredential

logger = get_task_logger(__name__)


@periodic_task(name="increment", run_every=timedelta(minutes=1))
def increment():
    logger.info("Inc++")
    userid = 'admin'
    u = AgSyncCredential.objects.filter(username=userid)
    if not u:
        userid=''
    else:
        u.update(expires_in=u.expires_in-1)
        userid = 'admin'