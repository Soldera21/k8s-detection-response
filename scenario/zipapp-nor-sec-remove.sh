#!/bin/bash

kubectl delete deployment zipapp -n default
kubectl delete service zipapp -n default
