FROM python:3.9.0-slim-buster

RUN apt-get update \
    && apt-get install -y openssh-server \
    && mkdir -p /var/run/sshd
EXPOSE 22
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

