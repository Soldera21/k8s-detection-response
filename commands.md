kubectl get pods -A

kubectl exec -it testpod -- sh -c "echo 'test' > /etc/testfile"

kubectl run testpod --image=alpine --command -- sleep 3600

kubectl exec -it testpod -- sh

kubectl logs -f --timestamps -n default falco-

kubectl delete pod <pod-name> -n <namespace> --grace-period=0 --force

helm repo add falcosecurity https://falcosecurity.github.io/charts

helm repo update

helm install falco falcosecurity/falco -n default

minikube start
minikube stop
minikube delete
minikube delete --purge --all

kubectl exec -it <FALCO_POD_NAME> -n <NAMESPACE> -- cat /etc/falco/falco.yaml

helm upgrade falco falcosecurity/falco -n default --set falco.file_output.enabled=true --set falco.file_output.filename="./events.txt" --set falco.file_output.keep_alive=false
# keep_alive "false" permits real time update but the file is opened and closed every time
# IDK why logs in "kubectl logs" are not real time

kubectl exec -it falco-qw42b -n default -- touch ./events.txt
kubectl exec -it falco-swmzq -n default -- tail -f ./events.txt


wget https://busybox.net/downloads/binaries/1.21.1/busybox-i686
chmod +x busybox-i686
./busybox-i686 echo "BOOM — upper layer binary executed"


https://falco.org/docs/concepts/outputs/channels/

https://falco.org/docs/reference/rules/default-rules/

https://falco.org/docs/reference/rules/examples/