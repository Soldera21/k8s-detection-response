#!/bin/bash

kubectl apply -f ./scenario/manifests/psa-ns.yaml
kubectl apply -f ./scenario/manifests/zipapp-deployment-psa.yaml
kubectl apply -f ./scenario/manifests/zipapp-service-psa.yaml

echo "Waiting for the service to be ready..."
sleep 5

minikube service zipapp-sec -n secured --url
