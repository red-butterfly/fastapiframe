FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY sources.list /etc/apt/

RUN apt-get update && apt-get install -y gettext
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN pip3 install pipenv -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

WORKDIR /app/

COPY ./app/Pipfile /app
COPY ./app/Pipfile.lock /app
RUN pipenv install --system --deploy --ignore-pipfile
