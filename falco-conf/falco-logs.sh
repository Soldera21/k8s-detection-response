#!/bin/bash

kubectl exec -it -n default $(kubectl get pod -n default -l app.kubernetes.io/name=falco -o jsonpath="{.items[0].metadata.name}") -- tail -f /var/log/falco.log
