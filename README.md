# Simple Django Messaging Template

This is a simple Django messaging template that you can use to quickly prototype a project. Feel free to download and modify for you own needs.

__NOTE:__ This project uses VueJS for the front end. You will need to have knownledge in Vue if you want to keep using it.

In case you need to deploy the application in a Docker environment, the template is shipped with all the required DockerFile and docker-compose files for just that.

# Organization

The Pipfile comes with the following applications:

* Redis
* Django
* Celery
* Celery Beat
* Channels
* Channels redis
* Daphne
* Django extensions

## Models

![Test Image 4](./assets/models1.png)

## Views

![Test Image 4](./assets/views.png)

## URLS

![Test Image 4](./assets/urls.png)


# Starting

Once you've cloned the repository or downloaded the zip file, start your project normally with `./manager.py/runserver` after having run `./manage.py migrate`.

You will need to run the redis server if you want to benefit from the full live chat functionnalities. For that, click on `redis-server` from the `redis/3.0.5` folder this will start the terminal with the server.

The template also comes with celery and celery beat in order to create tasks or periodic tasks. For a local utilisation, run `celery worker -A zambda -l info` to start the main process and `celery beat -A zambda -l info` for the scheduler.

You can add custom tasks either in the `zambda/celery.py` file or in the `forum/tasks.py`.
