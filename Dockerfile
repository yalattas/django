FROM python:3.9.7-slim
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "sh", "./devops/bootup.sh" ]