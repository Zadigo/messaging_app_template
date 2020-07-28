FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

LABEL name="messaging v1.0"

RUN pip install --upgrade pip

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

COPY . /app/

WORKDIR /app

RUN python -m pip install pipenv
RUN pipenv install --deploy --system

EXPOSE 8000 443

# Development server
# ENTRYPOINT [ "python", "zambda/manage.py", "runserver", "0.0.0.0:8000" ]
# .. or ASGI server
# CMD daphne zambda.asgi:application
