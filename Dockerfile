FROM mysql:5.7
ENV MYSQL_ROOT_PASSWORD my-secret-pw
ENV MYSQL_DATABASE waste
ENV MYSQL_USER root_user
ENV MYSQL_PASSWORD The_root_user1
WORKDIR /app
FROM python:3.8
ENV DJANGO_SETTINGS_MODULE waste_monitoring.settings
COPY . /app
WORKDIR /app
RUN apt install -y libssl-dev libmariadb-dev
RUN pip3 install -r requirements.txt
CMD [ "python3", "manage.py", "runserver", "8000"]