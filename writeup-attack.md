- run all deployments
- run minikube service zipapp --url
- run ngrok tcp 4444
- change url in revshell with ngrok's one
- run nc -nlv 4444
- upload zip file and do "download all"

how to recompile zipapp image:
- cd zipapp
- eval $(minikube docker-env)
  docker build -t zipapp:latest .
- cd ..
- kubectl delete deployment zipapp
- kubectl apply -f manifests/
