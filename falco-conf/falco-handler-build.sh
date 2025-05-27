#!/bin/bash

cd ./falco-conf/falco-handler/

# FOR WINDOWS
# & minikube -p minikube docker-env --shell powershell | Invoke-Expression
# FOR LINUX/MACOS
eval $(minikube docker-env)

docker build -t falco-handler:latest .

cd ../../
