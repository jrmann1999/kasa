#!/bin/bash
envsubst '$FLASK_SERVER_ADDR' < /app/default.conf > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'