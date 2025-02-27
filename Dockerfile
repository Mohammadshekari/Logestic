FROM python:3.10-slim-buster

LABEL maintainer="bigdeli.ali3@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .
COPY ./entrypoint.sh .
COPY ./core .
RUN chmod +x ./entrypoint.sh

RUN pip install --upgrade pip -i https://mirror-pypi.runflare.com && pip install -r requirements.txt  -i https://mirror-pypi.runflare.com


EXPOSE 8000

# execute our entrypoint.sh file
CMD ["sh","./entrypoint.sh"]