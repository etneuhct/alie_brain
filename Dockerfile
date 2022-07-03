FROM python:3.9.12-alpine3.15

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev flac
RUN python3 -m pip install -r requirements.txt --no-cache-dir && apk --purge del .build-deps
COPY . .
EXPOSE 80
EXPOSE 443
CMD uvicorn main:app --host 0.0.0.0 --port 80
