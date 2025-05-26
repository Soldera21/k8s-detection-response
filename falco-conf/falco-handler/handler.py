from flask import Flask, request
import subprocess
import re

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    pod = data.get("output_fields", {}).get("k8s.pod.name")
    namespace = data.get("output_fields", {}).get("k8s.ns.name")
    
    if not pod or not namespace:
        container_full_name = str(data.get("output_fields", {}).get("container.name") or "")
        match = re.match(r"k8s_([^_]+)_([^_]+)_([^_]+)_", container_full_name)
        if match:
            container_name, pod, namespace = match.groups()
    
    app.logger.info(f"[*] Triggered rule from pod={pod}, ns={namespace}")
    app.logger.info(f"[*] Full data: {data}")

    if pod and namespace:
        try:
            result = subprocess.run(
                ["kubectl", "get", "pod", pod, "-n", namespace,
                 "-o", "jsonpath={.metadata.ownerReferences[0].name}"],
                stdout=subprocess.PIPE, check=True, text=True
            )
            deployment = result.stdout.strip()[:-11]
            app.logger.info(f"[*] Result: {result}")
            app.logger.info(f"[*] Deployment: {deployment}")
            if deployment:
                subprocess.run([
                    "kubectl", "label", "deployment", deployment,
                    "tainted-by-falco=true", "-n", namespace, "--overwrite"
                ], check=True)
                app.logger.info(f"[+] Labeled deployment {deployment} in {namespace}")

                # SCALE REPLICAS TO 0 OR DO WHATEVER ACTION YOU WANT
                #subprocess.run([
                #    "kubectl", "scale", "deployment", deployment, "--replicas=0", "-n", namespace
                #], check=True)
                #app.logger.info(f"[+] Action on deployment {deployment} in {namespace}")
                
        except subprocess.CalledProcessError as e:
            app.logger.error(f"[-] Error labeling deployment: {e}")
    else:
        app.logger.warning("[!] Could not resolve pod or namespace")
    return "ok", 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)