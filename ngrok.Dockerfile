FROM ngrok/ngrok:latest

COPY --chown=ngrok ngrok.yml /etc/ngrok.yml

ENTRYPOINT ["ngrok", "start", "--all", "--config", "/etc/ngrok.yml"]