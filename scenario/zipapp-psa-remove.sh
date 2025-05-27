#!/bin/bash

kubectl delete deployment zipapp -n default
kubectl delete service zipapp -n default
kubectl delete namespace secured
