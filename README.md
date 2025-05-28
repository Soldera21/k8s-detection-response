# K8s Attack Detection and Countermeasures
**Network & Cloud Security Project**

Politecnico di Torino

Soldera Marco (s338823) - Stella Francesca (s343411)

## Introduction
The main goal of this project is to explore detection mechanisms in K8s environment like Falco and Tracee. Then we tried to manage alerts from this tools. We simulated three types of attacks are launched and then the respective countermeasures are proposed. Countermeasures are presented singularly but they can be combined to protect from all the presented attacks at the same time.

---

## Requirements
The project and the related scripts are tested in MacOS and Linux. For Windows some commands are different when building docker images. The corresponding command is listed in ```.sh``` files and should be run manually.
To run the project the following tools are needed:
- ```minikube``` or k8s cluster
- ```kubectl```
- ```helm```
- ```docker```

---

## Installation
Here we present installation of Flaco, Tracee and their respective event handler. The handlers have an example of event management that is very basic but it can be personalized based on requirements.

### Falco
This is the first detection tool that we used. It can detect various attacks through system calls using ePBF. It can be installed with:

```
bash falco-conf/falco-install.sh
```

Now it is running in the cluster. We installed it in the ```default``` namespace. It has a default set of rules to detetct attacks and events in the cluster. Logs can be viewed with:

```
bash falco-conf/falco-logs.sh
```

If logs gives an error, just wait some seconds. If the log file is not found it is because there are no logs yet.

Finally we can uninstall it using:

```
bash falco-conf/falco-remove.sh
```

#### Falco Handler
This is a service that can receive Falco events through a webhook. It has management privileges on the cluster, so it can be used to perform some automatic action on the specific pod/deployment when an alert is received.
First of all we need to build its image:

```
bash falco-conf/falco-handler-build.sh
```

And then start its deployment:

```
bash falco-conf/falco-handler-start.sh
```

When Falco is removed and the handler is not needed anymore we can remove it:

```
bash falco-conf/falco-handler-stop.sh
```

### Tracee
This is the second detection tool that we used. It can detect various attacks through system calls using ePBF like Falco. It can be installed with:

```
bash tracee-conf/tracee-install.sh
```

Now it is running in the cluster. We installed it in the ```default``` namespace. It has a default set of rules to detetct attacks and events in the cluster. Logs can be viewed with:

```
bash tracee-conf/tracee-logs.sh
```

Finally we can uninstall it using:

```
bash tracee-conf/tracee-remove.sh
```

#### Tracee Handler
This is a service that can receive Tracee events through a webhook. It has management privileges on the cluster, so it can be used to perform some automatic action on the specific pod/deployment when an alert is received.
First of all we need to build its image:

```
bash tracee-conf/tracee-handler-build.sh
```

And then start its deployment:

```
bash tracee-conf/tracee-handler-start.sh
```

When Tracee is removed and the handler is not needed anymore we can remove it:

```
bash tracee-conf/tracee-handler-stop.sh
```

---

## Scenario Setup
To simulate some attacks we prepared a deployment of a web application performing zip/unzip service. It is vulnerable to command injection because the input is not sanitized. Here we want to show that with some countermeasures applied to the deployment we can contain the attacks performed.
First we need to build all the needed images with:

```
bash scenario/zipapp-build-images.sh
```

### 1. Base
We can start the basic unsecure scenario with:

```
bash scenario/zipapp-normal-start.sh
```

Beware to not interrupt the previous command if it is not done automatically.
Now we can verify that everything (detection tool, handler and scenario) is working in another terminal with the command:

```
kubectl get pods
```

From the first command we obtain an URL to connect to the ```zipapp``` service and navigate the website with a browser. From here we can launch the attacks explained better later.
To stop this scenario we can run:

```
bash scenario/zipapp-nor-sec-remove.sh
```

### 2. Seccomp Protection
We can start the scenario using ```seccomp``` policies with:

```
bash scenario/zipapp-seccomp-ptrace-start.sh
```

for the attack that runs ptrace and the following one for the attack about reveser shell:

```
bash scenario/zipapp-seccomp-revshell-start.sh
```

Beware to not interrupt the previous command if it is not done automatically.
Now we can verify that everything (detection tool, handler and scenario) is working in another terminal with the command:

```
kubectl get pods -n default
```

From the first command we obtain an URL to connect to the ```zipapp``` service and navigate the website with a browser. From here we can launch the attacks explained better later.
To stop this scenario we can run:

```
bash scenario/zipapp-nor-sec-remove.sh
```

### 3. PSA Protection
In this case we craete a secure namespace called ```secured``` that is controlled at pod start by Pod Security Admission policies. We can start the scenario using this mechanism with:

```
bash scenario/zipapp-psa-start.sh
```

Beware to not interrupt the previous command if it is not done automatically.
Now we can verify that everything (detection tool, handler and scenario) is working in another terminal with the command:

```
kubectl get pods -n secured
```

From the first command we obtain an URL to connect to the ```zipapp``` service and navigate the website with a browser. From here we can launch the attacks explained better later.
To stop this scenario we can run:

```
bash scenario/zipapp-psa-remove.sh
```

---

## Attacks
Here we present the three attacks that we prepared to show how ```seccomp``` and PSA work in a K8s cluster. After uploading the zip payload if any file starting with ```._``` is found in the web interface listing all the unzipped files, delete them.

### Dropped Binary
In this attack we are uploading the payload ```binary_download.zip```. Here we are exploting the vulnerability in the zip command that with files ```-T``` and ```-TT```, takes them as flags executing what is sent after (other files with the same name as a bash command). The attack is triggered pressing "Download All" after having uploaded the zip file. In the uploaded script we are installing ```wget```, downloading and executing an example binary called ```busybox```. This can be blocked using the PSA scenario.
To check what is happening we can use the command for Falco:

```
bash falco-conf/falco-logs.sh
```

or for Tracee:

```
bash tracee-conf/tracee-logs.sh
```

Then we can check logs also from handlers using. For Falco:

```
kubectl logs deployment/falco-handler -n default
```

or for Tracee handler:

```
kubectl logs deployment/tracee-handler -n default
```

After the attack is executed successfully the handler adds a label to the deployment. This can be verified with:

```
kubectl get deployments -n <namespace-name> --show-labels
```

If the action used in the handlers is to scale down to 0 replicas (check for this in the ```handler.py``` of the detection tool used if it is commented or not) the affected deployments, we can verify there are no more pods of that deployment with:

```
kubectl get pods -n <namespace-name>
```

Then we can scale them up with:

```
kubectl scale deployment <deployment-name> -n <namespace-name> --replicas=1
```

After rescaling (likely because the problem have been solved) we can remove the label with:

```
kubectl label deployment <deployment-name> -n <namespace-name> <label-key>-
```

### Ptrace In Binary
In this attack we are uploading the payload ```ptrace_payload.zip```. Here we are exploting the vulnerability in the zip command that with files ```-T``` and ```-TT```, takes them as flags executing what is sent after (other files with the same name as a bash command). The attack is triggered pressing "Download All" after having uploaded the zip file. Here we are uploading a compiled binary that is executing a ptrace syscall (usually used by malwares to understand if they are in debugging-mode). This can be blocked using the seccomp ptrace scenario.
To check what is happening we can use the command for Falco:

```
bash falco-conf/falco-logs.sh
```

or for Tracee:

```
bash tracee-conf/tracee-logs.sh
```

Then we can check logs also from handlers using. For Falco:

```
kubectl logs deployment/falco-handler -n default
```

or for Tracee handler:

```
kubectl logs deployment/tracee-handler -n default
```

After the attack is executed successfully the handler adds a label to the deployment. This can be verified with:

```
kubectl get deployments -n <namespace-name> --show-labels
```

If the action used in the handlers is to scale down to 0 replicas (check for this in the ```handler.py``` of the detection tool used if it is commented or not) the affected deployments, we can verify there are no more pods of that deployment with:

```
kubectl get pods -n <namespace-name>
```

Then we can scale them up with:

```
kubectl scale deployment <deployment-name> -n <namespace-name> --replicas=1
```

After rescaling (likely because the problem have been solved) we can remove the label with:

```
kubectl label deployment <deployment-name> -n <namespace-name> <label-key>-
```

### Reverse Shell
In this attack we are uploading the payload ```reverse_shell.zip```. Here we are exploting the vulnerability in the zip command that with files ```-T``` and ```-TT```, takes them as flags executing what is sent after (other files with the same name as a bash command). The attack is triggered pressing "Download All" after having uploaded the zip file. Here we are uploading a script that is executing a reverse shell to the given server. This can be blocked using the seccomp revshell scenario.
Before uploading the payload we need to prepare the script. First we run ```ngrok``` to redirect traffic to our machine with:

```
ngrok tcp 4444
```

Then open a netcat TCP listening server in another terminal:

```
nc -nlv 4444
```

Now change the domain and port in the file ```evil``` in the payload with the ones from ```ngrok```. Re-pack in a zip file and upload to the zipapp. After running the attack we can interact with a shell of the zipapp pod from the netcat terminal.

To check what is happening we can use the command for Falco:

```
bash falco-conf/falco-logs.sh
```

or for Tracee:

```
bash tracee-conf/tracee-logs.sh
```

Then we can check logs also from handlers using. For Falco:

```
kubectl logs deployment/falco-handler -n default
```

or for Tracee handler:

```
kubectl logs deployment/tracee-handler -n default
```

After the attack is executed successfully the handler adds a label to the deployment. This can be verified with:

```
kubectl get deployments -n <namespace-name> --show-labels
```

If the action used in the handlers is to scale down to 0 replicas (check for this in the ```handler.py``` of the detection tool used if it is commented or not) the affected deployments, we can verify there are no more pods of that deployment with:

```
kubectl get pods -n <namespace-name>
```

Then we can scale them up with:

```
kubectl scale deployment <deployment-name> -n <namespace-name> --replicas=1
```

After rescaling (likely because the problem have been solved) we can remove the label with:

```
kubectl label deployment <deployment-name> -n <namespace-name> <label-key>-
```

---

## Other Useful Commands
To explore and debug the pods we can spawn a shell inside using:

```
kubectl exec -it <pod-name> -n <namespace-name> -- sh
```

Or restart the deployment with:

```
kubectl rollout restart deployment/<deployment-name> -n <namespace-name>
```
