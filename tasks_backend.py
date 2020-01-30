from celery import Celery
import time

## Run with backend sqlite
## celery -A tasks_backend worker --loglevel=info
app = Celery('tasks', broker='amqp://localhost//', backend='db+sqlite:///results.db')

@app.task
def reverse(string):
    time.sleep(10)
    return string[::-1]


