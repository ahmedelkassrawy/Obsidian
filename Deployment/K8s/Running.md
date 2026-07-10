## 🛠 Part 1: How to Run Kubernetes Locally

Before you can run the YAML files, you need a cluster. Here are the three most popular ways for AI Engineers to run K8s on a laptop:

|**Tool**|**Best For...**|**Setup Command (Once installed)**|
|---|---|---|
|**Docker Desktop**|Beginners already using Docker.|Enable "Kubernetes" in Settings.|
|**Minikube**|Learning all K8s features locally.|`minikube start`|
|**Kind**|Fast, lightweight testing in CI/CD.|`kind create cluster`|

> **Pro-Tip:** Once your cluster is started, always run `kubectl get nodes` to verify you are connected.

---

## 🏗 Part 2: The Core "MLOps" Blueprint

In our exercise, we used two files. Think of the **Deployment** as the "Brain" (the logic/code) and the **Service** as the "Phone Number" (how others find the code).

### 1. The Deployment (`deployment.yaml`)

This tells Kubernetes: _"Run 2 copies of my Model V1."_

YAML

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-ai-model
spec:
  replicas: 2           # How many "workers" we want
  selector:
    matchLabels:
      app: mlops-api    # This connects the Deployment to the Service
  template:
    metadata:
      labels:
        app: mlops-api
    spec:
      containers:
      - name: model-container
        image: kennethreitz/httpbin  # Our "Fake" AI Model Image (v1)
        ports:
        - containerPort: 80
```

### 2. The Service (`service.yaml`)

This tells Kubernetes: _"Listen on port 8080 and send traffic to any pod labeled `mlops-api`."_

YAML

```
apiVersion: v1
kind: Service
metadata:
  name: ai-model-service
spec:
  selector:
    app: mlops-api      # The "Bridge": Must match the Deployment label!
  ports:
    - protocol: TCP
      port: 8080        # The port the Service listens on
      targetPort: 80    # The port the Pod is actually using
```

---

## 🚀 Part 3: The Workflow Commands

Here is the sequence of commands we used to make the magic happen:

### Step 1: Deploy the infrastructure

Bash

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### Step 2: Verify it’s running

Bash

```
kubectl get pods
# Look for 1/1 Running!
```

### Step 3: The Secure Tunnel (Port Forwarding)

Since Kubernetes is secure by default, we "drill a tunnel" to see the API from our browser.

Bash

```
kubectl port-forward deployment/my-ai-model 8080:80
```

_Now visit `http://localhost:8080` in your browser._

---

## 🔄 Part 4: The "Finale" (Zero-Downtime Update)

When you update the `image:` tag in your `deployment.yaml` (e.g., from `v1` to `v2`) and run `kubectl apply`, Kubernetes performs a **Rolling Update**.

### What happens under the hood:

1. **The Newcomer:** K8s spins up one new Pod with the **v2** model.
    
2. **The Health Check:** K8s waits until the v2 pod is "Ready."
    
3. **The Switch:** The Service starts sending some traffic to the new v2 pod.
    
4. **The Cleanup:** K8s kills one old v1 pod.
    
5. **Repeat:** It repeats this until 100% of your pods are running v2.
    

**The result?** Your users never saw an "Error 404" or a "Site Down" message. The transition was seamless.

---
### ⚠️ Common Pitfall: The YAML "Space" Trap

Remember: **YAML is sensitive to spaces.** * If you have **3** spaces instead of **2**, the file is broken.

- If a line is not aligned with its "parent," Kubernetes won't understand the relationship.
    
- **Study Tip:** Use a VS Code extension like "Kubernetes" or "YAML" to highlight these errors before you run `kubectl apply`.
    

**Ready to try a rollback?** If v2 was buggy, you could instantly go back by running:

`kubectl rollout undo deployment/my-ai-model`

deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlops-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mlops-api
  template:
    metadata: 
      labels:
        app: mlops-api
    spec:
      containers:
      - name: model-container
        image: mlops-fake-api:v2
        imagePullPolicy: Never   # <--- CRITICAL for local Docker Desktop builds
        ports:
        - containerPort: 80
```

service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mlops-api-service
spec:
  type: LoadBalancer       # <--- Exposes the service fully
  ports:
  - port: 8080             # The port we will access on our laptop
    targetPort: 80         # The port the container is listening on
  selector:
    app: mlops-api         # Connects to our deployment pods

```