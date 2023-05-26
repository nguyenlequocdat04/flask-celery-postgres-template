FROM whoiskp/python:lus-base

WORKDIR /webapps

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

COPY conf/uwsgi.ini /etc/uwsgi/
COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps
CMD [ "supervisord", "-n", "-c", "/etc/supervisor.d/supervisord.conf" ]
