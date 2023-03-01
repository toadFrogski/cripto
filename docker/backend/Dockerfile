FROM python:3.10-slim as build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libmariadb-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --upgrade pip

RUN pip3 install --no-cache-dir --no-warn-script-location \
        uwsgi \
        Django>=4.1.1 \
        djangorestframework>=3.11.1 \
        django-bootstrap5 \
        django-mysql>=3.8.1 \
        mysqlclient>=2.0.1 \
        Pillow>=9.1.1 \
        openpyxl>=3.0.4 \
        requests>=2.24.0 \
        celery>=5.2.2 \
        redis>=3.5.3 \
        safety \
        bandit \
        tzdata \
        graypy


FROM python:3.10-slim as runtime

ENV SOCK_PATH=/var/run/python/uwsgi.sock \
    WSGI_FILE_PATH=/var/www/backend/main/wsgi.py \
    WSGI_PROCESSES=4

VOLUME [ "/var/run/python" ]

WORKDIR /var/www/backend

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmariadb3 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin/uwsgi /usr/local/bin/
COPY --from=build /usr/local/bin/celery /usr/local/bin/
COPY --from=build /usr/local/bin/bandit* /usr/local/bin/
COPY --from=build /usr/local/bin/safety /usr/local/bin/

CMD ["sh", "-c", "uwsgi --master --die-on-term --protocol uwsgi --wsgi-file $WSGI_FILE_PATH --socket $SOCK_PATH --chmod-socket=666 --processes=$WSGI_PROCESSES"]