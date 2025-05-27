#!/bin/bash

kubectl delete deployment falco-handler -n default

kubectl delete service falco-handler -n default
kubectl delete serviceaccount falco-handler -n default
kubectl delete clusterrole falco-deployment-manager
kubectl delete clusterrolebinding falco-handler-deployment-binding
