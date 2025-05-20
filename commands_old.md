kubectl get pods -A

kubectl exec -it testpod -- sh -c "echo 'test' > /etc/testfile"

kubectl run testpod --image=alpine --command -- sleep 3600

kubectl exec -it testpod -- sh

kubectl logs -f --timestamps -n default falco-

kubectl delete pod <pod-name> -n <namespace> --grace-period=0 --force

helm repo add falcosecurity https://falcosecurity.github.io/charts

helm repo update

helm install falco falcosecurity/falco -n default

kubectl rollout restart deployment -n default

minikube start
minikube stop
minikube delete
minikube delete --purge --all

kubectl exec -it <FALCO_POD_NAME> -n <NAMESPACE> -- cat /etc/falco/falco.yaml

helm upgrade falco falcosecurity/falco -n default --set falco.file_output.enabled=true --set falco.file_output.filename="./events.txt" --set falco.file_output.keep_alive=false --set falcosidekick.enabled=true --set falco.http_output.enabled=true --set falco.http_output.url="http://falco-falcosidekick:2801/" --set falco.json_output=true --set falco.json_include_output_property=true --set falcosidekick.config.webhook.enabled=true --set falcosidekick.config.webhook.address="http://handler:80/"

kubectl create configmap falco-custom-rules \
  --from-file=custom.yaml=falco-rules/custom.rules.yaml \
  -n default

helm upgrade --install falco falcosecurity/falco \
  -n default -f falco-rules/falco-conf.yaml

helm upgrade --install falco falcosecurity/falco \
  -n default -f falco-rules/falco-conf.yaml -f falco-rules/custom-rules.yaml

kubectl exec -it $(kubectl get pod -l app.kubernetes.io/name=falco -n default -o jsonpath='{.items[0].metadata.name}') -n default -- sh
# keep_alive "false" permits real time update but the file is opened and closed every time
# IDK why logs in "kubectl logs" are not real time

kubectl logs deployment/handler

kubectl exec -it falco-qw42b -n default -- touch ./events.txt
kubectl exec -it falco-swmzq -n default -- tail -f ./events.txt

kubectl exec -it -n default $(kubectl get pod -n default -l app.kubernetes.io/name=falco -o jsonpath="{.items[0].metadata.name}") -- tail -f /var/log/falco.log

kubectl get pods --show-labels
kubectl get deployments --show-labels


apt-get install wget
wget https://busybox.net/downloads/binaries/1.21.1/busybox-i686
chmod +x busybox-i686
./busybox-i686 echo "BOOM — upper layer binary executed"


https://falco.org/docs/concepts/outputs/channels/

https://falco.org/docs/reference/rules/default-rules/

https://falco.org/docs/reference/rules/examples/