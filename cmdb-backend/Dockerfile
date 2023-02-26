 FROM registry.cn-shanghai.aliyuncs.com/mpd_k8s/python:3.8-buster

WORKDIR /app

RUN set -ex; \
    sed -i 's#http://deb.debian.org#https://mirrors.aliyun.com#g' /etc/apt/sources.list; \
    apt update; \
    apt install -y curl

COPY . /app

RUN set -ex; \
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

ENV PYTHONPATH=$PYTHONPATH:/app

LABEL project="cmdb-backend"

CMD ["python","manage.py","runserver","0.0.0.0:9090"]
