FROM alpine:latest

COPY ./compose/django/gunicorn.sh /
COPY ./requirements /tmp/requirements

RUN apk -U add python3 python3-dev git libpq postgresql-dev gcc musl-dev gettext \
    && pip3 install --upgrade pip \
    && pip3 install -r /tmp/requirements/production.txt \
    && apk del gcc python3-dev musl-dev zlib-dev openssl-dev postgresql-dev \
    && rm -fr /tmp/* && rm -rf /var/cache/apk/*

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

CMD ["/gunicorn.sh"]
