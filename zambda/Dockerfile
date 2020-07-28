FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

LABEL name="messaging v1.0"

WORKDIR /app

# RUN pip install --upgrade pip

COPY Pipfile Pipfile.lock /app/

RUN pip3 install "pipenv==2018.11.26"
RUN pipenv install --deploy --system

COPY . /app/

EXPOSE 8000

# Development server
CMD [ "runserver", "0.0.0.0:8000" ]
ENTRYPOINT [ "python", "/app/manage.py" ]
# .. or ASGI server
# CMD daphne zambda.asgi:application
