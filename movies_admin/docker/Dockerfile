FROM python:3.10
WORKDIR /opt/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
COPY ././requirements.txt .
RUN pip install -r requirements.txt
COPY ././movies_admin .
COPY ././sqlite_to_postgres sqlite_to_postgres
RUN mkdir container_config
RUN mkdir static
RUN chmod +x docker/manage.sh
ENTRYPOINT ["docker/manage.sh"]