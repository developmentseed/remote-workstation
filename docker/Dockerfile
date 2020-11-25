FROM python:3.9.0-slim-buster

RUN apt-get update \
    && apt-get install -y curl openssh-server \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config \
    && mkdir -p /var/run/sshd
EXPOSE 22
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
