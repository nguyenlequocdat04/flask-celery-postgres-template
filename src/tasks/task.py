from manage import celery_app

@celery_app.task(rate_limit='20/s', name='task_greeting')
def task_greeting(msg):
    print(msg)
    return msg