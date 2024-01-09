from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name, 
        broker='redis://localhost:6379/1', 
                backend='redis://localhost:6379/2',)


    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
