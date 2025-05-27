#!/bin/bash

cd ./scenario/zipapp/

# FOR WINDOWS
# & minikube -p minikube docker-env --shell powershell | Invoke-Expression
# FOR LINUX/MACOS
eval $(minikube docker-env)
docker build -t zipapp:latest .

# FOR WINDOWS
# & minikube -p minikube docker-env --shell powershell | Invoke-Expression
# FOR LINUX/MACOS
eval $(minikube docker-env)
docker build -t zipapp:secure -f Dockerfile.sec .

cd ../../
