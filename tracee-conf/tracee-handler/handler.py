from flask import Flask, request
import subprocess
import re
import json
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    pod = None
    namespace = None
    default_namespace = 'default'

    hostname = data.get("hostName", "")
    app.logger.info(f"[*] Extracted hostname: {hostname}")

    if hostname:
        # Extract the pod name from hostname
        pod_match = re.match(r"([a-z0-9-]+)-[a-z0-9]+$", hostname)
        if pod_match:
            pod_prefix = pod_match.group(1)
            app.logger.info(f"[*] Extracted pod prefix: {pod_prefix}")
            
            # If we have a pod prefix, try to get the full pod name and namespace
            if pod_prefix:
                try:
                    # First try with all-namespaces
                    try:
                        result = subprocess.run(["kubectl", "get", "pods", "--all-namespaces", "-o", "json"], stdout=subprocess.PIPE, check=True, text=True)
                        pods_json = json.loads(result.stdout)
                    except subprocess.CalledProcessError:
                        # Fall back to default namespace only if cluster-wide search fails
                        result = subprocess.run(["kubectl", "get", "pods", "-n", default_namespace, "-o", "json"], stdout=subprocess.PIPE, check=True, text=True)
                        pods_json = json.loads(result.stdout)
                    
                    # Find pods with names starting with our prefix
                    for item in pods_json.get("items", []):
                        pod_name = item.get("metadata", {}).get("name", "")
                        if pod_name.startswith(f"{pod_prefix}-"):
                            pod = pod_name
                            namespace = item.get("metadata", {}).get("namespace", "")
                            app.logger.info(f"[*] Found matching pod: {pod}, namespace: {namespace}")
                            break
                    
                    if not pod or not namespace:
                        # As a last resort, try using the hostname directly as the pod name
                        try:
                            result = subprocess.run(["kubectl", "get", "pod", hostname, "-n", default_namespace, "-o", "json"], stdout=subprocess.PIPE, check=True, text=True)
                            pod_json = json.loads(result.stdout)
                            pod = pod_json.get("metadata", {}).get("name", "")
                            namespace = pod_json.get("metadata", {}).get("namespace", "")
                            if pod and namespace:
                                app.logger.info(f"[*] Found pod using exact hostname: {pod}, namespace: {namespace}")
                        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
                            app.logger.error(f"[-] Error finding pod with exact hostname: {e}")
                except subprocess.CalledProcessError as e:
                    app.logger.error(f"[-] Error retrieving pod info for prefix {pod_prefix}: {e}")
                except json.JSONDecodeError as e:
                    app.logger.error(f"[-] Error parsing kubectl output: {e}")
    
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
                    "tainted-by-tracee=true", "-n", namespace, "--overwrite"
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