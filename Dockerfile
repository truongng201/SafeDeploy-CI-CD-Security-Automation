## base image
FROM python:3.13-alpine AS compile-image

## install dependencies
RUN apk update && \
    apk add --no-cache \
    libpq-dev \
    gcc

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## add and install requirements
RUN pip install --upgrade pip && pip install pip-tools
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## build-image
FROM python:3.13-alpine AS runtime-image

## install nc and vulnerable package
RUN apk update && \
    apk add --no-cache curl openssl=1.1.1t-r0

## copy Python dependencies from build image
COPY --from=compile-image /opt/venv /opt/venv

## set working directory
WORKDIR /usr/src/app

RUN echo -e 'CipherString = DEFAULT@SECLEVEL=1' >>/etc/ssl/openssl.cnf

## add user
RUN addgroup -S dev && adduser -S dev -G dev
RUN mkdir -p /usr/src/app && \
    chown -R dev:dev /usr/src/app

# switch to non-root user
USER dev

COPY . /usr/src/app

## set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"