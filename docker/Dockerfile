FROM python:3.9.0-buster

# --------------------------------------------------------------------------
# Install and configure sshd.
# https://docs.docker.com/engine/examples/running_ssh_service for reference.
# --------------------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y openssh-server \
    && mkdir -p /var/run/sshd

EXPOSE 22

# -------------------------------------------------------------------------------------
# Execute a startup script.
# https://success.docker.com/article/use-a-script-to-initialize-stateful-container-data
# for reference.
# -------------------------------------------------------------------------------------
COPY docker-entrypoint.sh /usr/local/bin/
RUN pip install jupyter
RUN mkdir /secrets
COPY special_message.txt /secrets/special_message.txt
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

