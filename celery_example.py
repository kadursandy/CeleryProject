from celery import chain, group
from flask import Flask
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy
from random import choice

# python celery_example.py
# celery -A celery_example worker --loglevel=info
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'db+sqlite:///results.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


celery = make_celery(app)
db = SQLAlchemy(app)

class Results(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.String(50))


@app.route('/process/<name>')
def process(name):
    # Call the celery task here using delay
    # reverse.delay(name)
    result = reverse.delay(name)
    print('result', result, result.status, result.get())
    # call using apply_async() using apply_async
    # reverse.apply_async(args=[name])
    return name


@app.route('/insertData')
def insert_data():
    # call  insert data from
    # app
    result = insert.delay()
    return 'Inserted Data!!'
    # call insert normally without celery
    # return insert()

@app.route('/add')
def add():
    result = create_chain()
    return result

@app.route('/groupcall')
def group_call():
    result = call_group()
    return result

#===============CELERY_WORKERS=================
# Worker CODE for reverse
# Run this worker from seperate terminal
# Task name = celery_example
# celery -A celery_example.celery worker --loglevel=info/debug
@celery.task(name='celery_example')
def reverse(string):
    return string[::-1]


@celery.task(name="celery_example.reverse")
def insert():
    for i in range(10):
        data = ''.join(choice('ABCDE') for i in range(10))
        result = Results(data=data)
        db.session.add(result)
    db.session.commit()
    return 'Done!!'

#chain add and mul example
# class Addandmultiple:
@celery.task(name="added")
def added(a, b):
    return a + b

@celery.task(name="multiply")
def multiply(a, b):
    return a * b

def call_group():
    res = group(added.s(i, i) for i in range(10)).apply_async()
    print('Group', res.get())
    return str(res)

def create_chain():
    # There are 3 ways of calling
    chain_result = chain(added.s(2, 2), multiply.s(2)).apply_async(link=added.s(2))
    # chain_result1 = (added.s(2, 2) | multiply.s(3)).apply_async()
    # chain_result2 = chain(added.s(2, 2) | multiply.s(2)).apply_async()
    print('chain result', chain_result, chain_result.status, chain_result.get())


    # Calling from class
    # chain_result = chain(Addandmultiple().added.s(2, 2), Addandmultiple().multiply.s(2)).apply_async()
    # chain_result1 = (Addandmultiple().added.s(2, 2) | Addandmultiple().multiply.s(3)).apply_async()
    # chain_result2 = chain(Addandmultiple().added.s(2, 2) | Addandmultiple().multiply.s(2)).apply_async()
    # print('chain result', chain_result, chain_result.status, chain_result.get())
    # print('chain_result1', chain_result1.get())
    # print('chain_result2', chain_result2.get())
    # if chain_result.status == u'SUCCESS':
        # print(chain_result.get())
    return "Chain submitted"


if __name__ == '__main__':
    app.run(debug=True)
