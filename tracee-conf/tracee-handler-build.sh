#!/bin/bash

cd ./tracee-conf/tracee-handler/

# FOR WINDOWS
# & minikube -p minikube docker-env --shell powershell | Invoke-Expression
# FOR LINUX/MACOS
eval $(minikube docker-env)

docker build -t tracee-handler:latest .

cd ../../
