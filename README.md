
# Falco + RCE Scenario

Questo pacchetto contiene:
- Una webapp vulnerabile esposta via NodePort (porta 30080)
- Regole Falco personalizzate per rilevare RCE, reverse shell, SSRF
- Script per simulare attacchi reali da esterno

## Deploy

```bash
kubectl apply -f manifests/
```

## Simula Attacchi

```bash
cd attack-scripts
./01_rce_test.sh
./02_reverse_shell.sh
./03_ssrf_test.sh
./04_internal_recon.sh
```

Verifica gli alert nei log di Falco (`kubectl logs -n falco -l app=falco`)
