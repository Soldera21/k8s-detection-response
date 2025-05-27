#!/bin/bash

kubectl delete deployment tracee-handler -n default

kubectl delete service tracee-handler -n default
kubectl delete serviceaccount tracee-handler -n default
kubectl delete clusterrole tracee-deployment-manager
kubectl delete clusterrolebinding tracee-handler-deployment-binding
