FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential libsqlclient-dev libssl-dev default-libmysqlclient-dev \
    && pip install --no-cache-dir --upgrade pip

RUN apt-get install -y --no-install-recommends --no-install-suggests default-mysql-client


WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

RUN python manage.py migrate

RUN python manage.py loaddata fixtures/*.json

EXPOSE 8000
ENTRYPOINT [ "python3" ]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]
