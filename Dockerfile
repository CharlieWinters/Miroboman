FROM python:3.10.3-slim

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apt-get update
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . .

EXPOSE 8000

#CMD [ "gunicorn", "main:app", "-w 4", "-k uvicorn.workers.UvicornWorker", "--bind 0.0.0.0:8000"]
CMD [ "gunicorn", "--config", "gunicorn_config.py", "main:app"]