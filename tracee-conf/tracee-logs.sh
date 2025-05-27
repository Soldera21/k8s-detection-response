#!/bin/bash

kubectl logs -n default -l app.kubernetes.io/name=tracee -f
