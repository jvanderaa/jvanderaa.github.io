FROM ghcr.io/nautobot/nautobot:3.2.7-py3.12@sha256:ecd0cd8d9868cefcfe3d8e8fb275e81aa271a97c92de7dd1a7e6d78ecaca37a0
USER root
RUN pip install --no-cache-dir 'nautobot==3.2.7' 'nautobot-design-builder==3.1.2'
COPY --chown=nautobot:nautobot config/nautobot_config.py /opt/nautobot/nautobot_config.py
COPY --chown=nautobot:nautobot jobs /opt/nautobot/jobs
RUN mkdir -p /opt/nautobot/media && chown -R nautobot:nautobot /opt/nautobot/media
USER nautobot
