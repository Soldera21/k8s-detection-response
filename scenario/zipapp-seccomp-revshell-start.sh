#!/bin/bash

minikube cp ./scenario/sec-profiles/seccomp-profile-connect.json /var/lib/kubelet/seccomp/seccomp-profile.json

kubectl apply -f ./scenario/manifests/zipapp-deployment-seccomp.yaml
kubectl apply -f ./scenario/manifests/zipapp-service.yaml

echo "Waiting for the service to be ready..."
sleep 5

minikube service zipapp --url
