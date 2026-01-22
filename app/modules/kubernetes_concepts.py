"""
☸️ Kubernetes Concepts Module
Simulates kubectl commands and teaches K8s concepts
"""

# Simulated resources
PODS = [
    {"name": "nginx-7c79c4bf97-x8k2j", "ready": "1/1", "status": "Running", "age": "2d"},
    {"name": "nginx-7c79c4bf97-m4n5p", "ready": "1/1", "status": "Running", "age": "2d"},
    {"name": "redis-master-0", "ready": "1/1", "status": "Running", "age": "5d"},
]

DEPLOYMENTS = [
    {"name": "nginx", "ready": "2/2", "available": 2, "age": "2d"},
    {"name": "api-gateway", "ready": "1/1", "available": 1, "age": "1d"},
]

SERVICES = [
    {"name": "kubernetes", "type": "ClusterIP", "cluster_ip": "10.96.0.1", "port": "443/TCP"},
    {"name": "nginx-svc", "type": "LoadBalancer", "cluster_ip": "10.96.45.123", "port": "80/TCP"},
]

CONCEPTS = {
    "pod": {
        "en": """☸️ **Pod** - Smallest deployable unit

• Can have 1+ containers
• Containers share network
• Ephemeral - can be replaced
• Gets unique IP

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: nginx
    image: nginx
```""",
        "si": """☸️ **Pod** - Kubernetes වල කුඩාම unit එක

• Containers කීපයක් තියෙන්න පුළුවන්
• Network share කරනවා
• ඕනෑම වෙලාවක replace වෙන්න පුළුවන්"""
    },
    "deployment": {
        "en": """☸️ **Deployment** - Manages Pod replicas

• Rolling updates
• Self-healing
• Rollback support

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
```""",
        "si": """☸️ **Deployment** - Pod replicas manage කරනවා

• Rolling updates
• Self-healing
• Rollback support"""
    },
    "service": {
        "en": """☸️ **Service** - Exposes Pods to network

Types:
• **ClusterIP** - Internal only
• **NodePort** - Node IP + static port
• **LoadBalancer** - External LB""",
        "si": """☸️ **Service** - Pods වලට network expose කරනවා

• ClusterIP - Cluster ඇතුලේ විතරයි
• LoadBalancer - External access"""
    },
    "configmap": {
        "en": "☸️ **ConfigMap** - Stores non-secret config data (env vars, config files)",
        "si": "☸️ **ConfigMap** - Configuration data store කරනවා"
    },
    "secret": {
        "en": "☸️ **Secret** - Stores sensitive data (passwords, tokens). Base64 encoded.",
        "si": "☸️ **Secret** - Sensitive data store කරනවා (passwords, tokens)"
    }
}


def simulate_kubectl(command: str) -> dict:
    """Simulate kubectl command"""
    parts = command.strip().split()
    
    if not parts or parts[0] != "kubectl":
        return {"success": False, "output": "❌ Command must start with 'kubectl'", "explanation": None}
    
    if len(parts) < 2:
        return {"success": False, "output": "❌ Missing action", "explanation": None}
    
    action = parts[1]
    
    if action == "get":
        if len(parts) < 3:
            return {"success": False, "output": "❌ Specify resource type", "explanation": None}
        
        resource = parts[2]
        
        if resource in ("pods", "pod", "po"):
            output = "```\nNAME                        READY   STATUS    AGE\n"
            for p in PODS:
                output += f"{p['name']:27} {p['ready']}     {p['status']:9} {p['age']}\n"
            output += "```"
            return {"success": True, "output": output, "explanation": CONCEPTS.get("pod")}
        
        elif resource in ("deployments", "deployment", "deploy"):
            output = "```\nNAME          READY   AVAILABLE   AGE\n"
            for d in DEPLOYMENTS:
                output += f"{d['name']:13} {d['ready']}     {d['available']}           {d['age']}\n"
            output += "```"
            return {"success": True, "output": output, "explanation": CONCEPTS.get("deployment")}
        
        elif resource in ("services", "service", "svc"):
            output = "```\nNAME         TYPE           CLUSTER-IP     PORT(S)\n"
            for s in SERVICES:
                output += f"{s['name']:12} {s['type']:14} {s['cluster_ip']:14} {s['port']}\n"
            output += "```"
            return {"success": True, "output": output, "explanation": CONCEPTS.get("service")}
        
        elif resource in ("nodes", "node"):
            return {
                "success": True,
                "output": "```\nNAME     STATUS   ROLES           VERSION\nnode-1   Ready    control-plane   v1.28.0\nnode-2   Ready    worker          v1.28.0\n```",
                "explanation": None
            }
    
    elif action == "describe":
        return {
            "success": True,
            "output": """📋 **Pod Description**
```
Name:         nginx-7c79c4bf97-x8k2j
Namespace:    default
Status:       Running
IP:           10.244.1.45
Containers:
  nginx:
    Image:   nginx:1.25
    Port:    80/TCP
    State:   Running
Events:
  Normal  Scheduled  Successfully assigned
  Normal  Started    Container started
```""",
            "explanation": CONCEPTS.get("pod")
        }
    
    elif action == "apply":
        return {
            "success": True,
            "output": "✅ `kubectl apply` - Configuration applied!\n```\ndeployment.apps/nginx configured\nservice/nginx-svc unchanged\n```",
            "explanation": None
        }
    
    elif action == "delete":
        return {
            "success": True,
            "output": f"🗑️ Deleting resource...\n```\n{parts[2] if len(parts) > 2 else 'resource'} deleted\n```",
            "explanation": None
        }
    
    elif action == "logs":
        return {
            "success": True,
            "output": "📜 **Pod Logs:**\n```\n2024-01-22 10:00:01 nginx started\n2024-01-22 10:00:02 listening on port 80\n```",
            "explanation": None
        }
    
    elif action == "scale":
        return {
            "success": True,
            "output": "📈 Scaling deployment...\n```\ndeployment.apps/nginx scaled\n```",
            "explanation": CONCEPTS.get("deployment")
        }
    
    elif action in ("help", "--help"):
        return {
            "success": True,
            "output": """📚 **kubectl Commands**

• `kubectl get pods` - List pods
• `kubectl get deployments` - List deployments
• `kubectl get services` - List services
• `kubectl describe pod <name>` - Pod details
• `kubectl apply -f file.yaml` - Apply config
• `kubectl delete <type> <name>` - Delete resource
• `kubectl logs <pod>` - View logs
• `kubectl scale deploy <name> --replicas=3`""",
            "explanation": None
        }
    
    return {"success": False, "output": f"❓ Unknown: kubectl {action}", "explanation": None}


def get_concept(name: str, lang: str = "en") -> str:
    """Get K8s concept explanation"""
    concept = CONCEPTS.get(name.lower())
    if concept:
        return concept.get(lang, concept.get("en"))
    return None


def get_kubernetes_menu():
    return """☸️ **Kubernetes Learning Center**

**Commands:**
• `kubectl get pods`
• `kubectl get deployments`
• `kubectl get services`
• `kubectl describe pod <name>`
• `kubectl help`

**Concepts:**
• /pod - What is a Pod?
• /deployment - Deployments
• /service - Services
• /configmap - ConfigMaps
• /secret - Secrets

💡 _Commands are simulated!_"""
