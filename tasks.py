from celery import Celery
###
# sudo apt-get install rabbitmq-server
# sudo service rabbitmq-server status
# celery -A tasks worker --loglevel=info
###
app = Celery('tasks', broker='amqp://localhost//')

@app.task
def add(x, y):
    return x + y

@app.task
def reverse(string):
    return string[::-1]
