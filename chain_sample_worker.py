from celery_example import celery


class Addandmultiply:
    @celery.task(name="add", bind=True)
    def add(self, a, b):
        return a + b

    @celery.task(name="multiply", bind=True)
    def multiply(self, a, b):
        return a * b
