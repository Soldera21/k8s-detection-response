#!/bin/bash

helm repo add aqua https://aquasecurity.github.io/helm-charts/
helm repo update
helm install tracee aqua/tracee -n default

kubectl patch daemonset tracee --patch-file ./tracee-conf/tracee-rules/tracee-ds-patch.yaml
