#!/bin/bash

minikube cp ./sec-profiles/seccomp-profile-ptrace.json /var/lib/kubelet/seccomp/seccomp-profile.json

kubectl apply -f ./scenario/manifests/zipapp-deployment-seccomp.yaml
kubectl apply -f ./scenario/manifests/zipapp-service.yaml

minikube service zipapp --url
