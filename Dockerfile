FROM python:3.6
ENV PYTHONUNBUFFERED=1
LABEL maintainer="b.p.blankenmeister@gmail.com"
LABEL version="1.0.0"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "./chatty.py"]

