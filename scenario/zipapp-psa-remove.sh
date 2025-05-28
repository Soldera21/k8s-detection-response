#!/bin/bash

kubectl delete deployment zipapp-sec -n secured
kubectl delete service zipapp-sec -n secured
kubectl delete namespace secured
