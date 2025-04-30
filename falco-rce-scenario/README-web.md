
# Falco RCE Scenario with Custom Flask App

## 🐳 Build Docker Image

Before deploying, build the vulnerable image locally:

```bash
cd webapp
docker build -t zipapp:latest .
```

If you're using Minikube:

```bash
eval $(minikube docker-env)
docker build -t zipapp:latest .
```

## 🚀 Deploy the Scenario

```bash
kubectl apply -f manifests/
```

Then, access the webapp or run the attack scripts from the previous package.

