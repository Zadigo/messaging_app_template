FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

LABEL name="messaging v1.0"

RUN mkdir /app

WORKDIR /app

RUN pip install --upgrade pip

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip3 install "pipenv==2018.11.26"
RUN pipenv install --deploy --system

COPY . /app/

EXPOSE 8000

# Start project using a simple script file
# ENTRYPOINT [ "../start/start.sh" ]
# ...or with development server
# ENTRYPOINT [ "python", "/app/mywebsite/manage.py", "runserver", "0.0.0.0:8000" ]
CMD pipenv run python manage.py runserver 0.0.0.0:8000
# ...or Gunicorn for production purposes
# CMD gunicorn zambda.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/app/zambda/ --log-file -
# CMD gunicorn zambda.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/app/zambda --log-level=debug --log-file=/var/log/gunicorn/gunicorn_log.log
