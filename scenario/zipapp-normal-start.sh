#!/bin/bash

kubectl apply -f ./scenario/manifests/zipapp-deployment.yaml
kubectl apply -f ./scenario/manifests/zipapp-service.yaml

echo "Waiting for the service to be ready..."
sleep 5

minikube service zipapp --url
