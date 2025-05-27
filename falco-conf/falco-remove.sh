#!/bin/bash

helm uninstall falco -n default
kubectl delete service falcosidekick -n default
