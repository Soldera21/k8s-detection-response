minikube start
minikube stop
minikube delete
minikube delete --purge --all


helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install falco falcosecurity/falco -n default
helm upgrade --install falco falcosecurity/falco -n default -f falco-rules/falco-conf.yaml -f falco-rules/custom-rules.yaml

kubectl exec -it -n default $(kubectl get pod -n default -l app.kubernetes.io/name=falco -o jsonpath="{.items[0].metadata.name}") -- tail -f /var/log/falco.log


helm repo add aqua https://aquasecurity.github.io/helm-charts/
helm repo update
helm install tracee aqua/tracee -n default
kubectl patch daemonset tracee --patch-file tracee-rules/tracee-ds-patch.yaml

kubectl logs -n default -l app.kubernetes.io/name=tracee -f


cd falco-handler

eval $(minikube docker-env)
docker build -t falco-handler:latest .

cd tracee-handler

eval $(minikube docker-env)
docker build -t tracee-handler:latest .

cd zipapp

eval $(minikube docker-env)
docker build -t zipapp:latest .

eval $(minikube docker-env)
docker build -t zipapp:secure -f Dockerfile.sec .

kubectl apply -f manifests/


minikube service zipapp --url
minikube service zipapp-sec -n secured --url


minikube cp ./sec-profiles/seccomp-profile-ptrace.json /var/lib/kubelet/seccomp/seccomp-profile.json
minikube cp ./sec-profiles/seccomp-profile-connect.json /var/lib/kubelet/seccomp/seccomp-profile.json

# Extra commnds:
kubectl exec -it <pod> -- sh
kubectl rollout restart deployment -n default
kubectl label deployment <deployment-name> <label-key>-
kubectl logs deployment/handler
kubectl get deployments --show-labels
