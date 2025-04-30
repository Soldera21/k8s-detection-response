
# Tracee + RCE Scenario

Questo pacchetto estende lo scenario con Tracee in Kubernetes per monitorare runtime events.

## Setup

1. **Crea il namespace**:
```bash
kubectl apply -f manifests/tracee-namespace.yaml
```

2. **Deploy di Tracee come DaemonSet**:
```bash
kubectl apply -f manifests/tracee-daemonset.yaml
```

3. **Verifica che Tracee sia in esecuzione**:
```bash
kubectl -n tracee get pods
kubectl -n tracee logs -l app=tracee
```

4. **Esegui gli attacchi dal pacchetto precedente (`falco-rce-scenario/attack-scripts`)**.

5. **Guarda gli eventi rilevati da Tracee**:
```bash
kubectl -n tracee logs -l app=tracee -f
```

## Eventi che Tracee può rilevare:
- Esecuzione di comandi sospetti (`sh`, `bash`, `curl`, ecc.)
- Creazione di socket (`reverse_shell`)
- Accesso a file sensibili (`/etc/passwd`)
