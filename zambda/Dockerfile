FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

LABEL name="messaging v1.0"

WORKDIR /app

RUN pip install --upgrade pip

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip3 install pipenv
RUN pipenv install --deploy --system

RUN ls -a

COPY . /app/

RUN ls -a

EXPOSE 8000 443

# Development server
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
# .. or ASGI server
# CMD daphne zambda.asgi:application
