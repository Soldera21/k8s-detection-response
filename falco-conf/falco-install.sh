#!/bin/bash

helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install falco falcosecurity/falco -n default -f falco-conf/falco-rules/falco-conf.yaml -f falco-conf/falco-rules/custom-rules.yaml

kubectl apply -f ./falco-conf/falco-rules/falcosidekick-service.yaml
