FROM homeassistant/home-assistant:latest

RUN apk add --no-cache curl bash
RUN pip3 install --no-cache-dir jupyterlab notebook
RUN pip3 install --no-cache-dir --no-deps huggingface_hub
RUN curl -sL "https://caddyserver.com/api/download?os=linux&arch=amd64" -o /usr/bin/caddy && chmod +x /usr/bin/caddy

COPY Caddyfile /etc/caddy/Caddyfile
COPY s6-services/caddy/run   /etc/services.d/caddy/run
COPY s6-services/jupyter/run /etc/services.d/jupyter/run
COPY cont-init.d/            /etc/cont-init.d/
RUN chmod +x /etc/services.d/caddy/run /etc/services.d/jupyter/run /etc/cont-init.d/*

COPY custom_components/ha_space_updater /usr/src/ha_space_updater
COPY HA_VERSION /HA_VERSION
