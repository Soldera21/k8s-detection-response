#!/bin/bash

kubectl apply -f ./scenario/manifests/zipapp-deployment.yaml
kubectl apply -f ./scenario/manifests/zipapp-service.yaml

minikube service zipapp --url
