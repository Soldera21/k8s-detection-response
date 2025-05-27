#!/bin/bash

kubectl apply -f ./falco-conf/manifests/psa-ns.yaml
kubectl apply -f ./scenario/manifests/zipapp-deployment-psa.yaml
kubectl apply -f ./scenario/manifests/zipapp-service-psa.yaml

minikube service zipapp-sec -n secured --url
