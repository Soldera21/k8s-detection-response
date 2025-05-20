minikube start
minikube stop
minikube delete
minikube delete --purge --all

helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update
helm install falco falcosecurity/falco -n default
helm upgrade --install falco falcosecurity/falco \
  -n default -f falco-rules/falco-conf.yaml -f falco-rules/custom-rules.yaml

kubectl exec -it -n default $(kubectl get pod -n default -l app.kubernetes.io/name=falco -o jsonpath="{.items[0].metadata.name}") -- tail -f /var/log/falco.log

kubectl logs deployment/handler
kubectl get deployments --show-labels


cd handler

eval $(minikube docker-env)
docker build -t handler:latest .

cd zipapp

eval $(minikube docker-env)
docker build -t zipapp:latest .

eval $(minikube docker-env)
docker build -t zipapp:secure -f Dockerfile.sec .

kubectl apply -f manifests/


minikube service zipapp --url
minikube service zipapp-sec -n secured --url
