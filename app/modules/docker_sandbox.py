"""
🐳 Docker Sandbox Module
Simulates Docker commands safely for learning
"""

import random
import string

# Simulated state
containers = []
images = [
    {"repository": "nginx", "tag": "latest", "id": "a1b2c3d4e5f6", "size": "142MB"},
    {"repository": "mysql", "tag": "8.0", "id": "b2c3d4e5f6a1", "size": "544MB"},
    {"repository": "redis", "tag": "alpine", "id": "c3d4e5f6a1b2", "size": "32MB"},
    {"repository": "node", "tag": "18-alpine", "id": "d4e5f6a1b2c3", "size": "178MB"},
    {"repository": "python", "tag": "3.11-slim", "id": "e5f6a1b2c3d4", "size": "125MB"},
]

EXPLANATIONS = {
    "run": {
        "en": "🐳 **docker run** creates and starts a container.\n\nFlags:\n• `-d` = background\n• `-p 8080:80` = port mapping\n• `-v /host:/container` = volume\n• `--name` = container name",
        "si": "🐳 **docker run** command එකෙන් container එකක් හදලා run කරනවා.\n\n• `-d` = background එකේ run කරන්න\n• `-p` = port mapping\n• `-v` = volume mount"
    },
    "ps": {
        "en": "📋 **docker ps** lists running containers.\n\n• `docker ps` = running only\n• `docker ps -a` = all containers",
        "si": "📋 **docker ps** command එකෙන් containers පෙන්නනවා."
    },
    "images": {
        "en": "🖼️ **docker images** lists downloaded images.",
        "si": "🖼️ **docker images** download කරපු images පෙන්නනවා."
    },
    "build": {
        "en": "🔨 **docker build** creates an image from Dockerfile.\n\n`docker build -t myapp:1.0 .`",
        "si": "🔨 **docker build** Dockerfile එකකින් image හදනවා."
    },
    "stop": {
        "en": "🛑 **docker stop** gracefully stops a container.",
        "si": "🛑 **docker stop** container එක නවතනවා."
    }
}


def generate_id():
    return ''.join(random.choices(string.hexdigits.lower(), k=12))


def simulate_docker(command: str) -> dict:
    """Simulate Docker command and return output with explanation"""
    parts = command.strip().split()
    
    if not parts or parts[0] != "docker":
        return {"success": False, "output": "❌ Command must start with 'docker'", "explanation": None}
    
    if len(parts) < 2:
        return {"success": False, "output": "❌ Missing subcommand", "explanation": None}
    
    subcmd = parts[1]
    
    if subcmd == "run":
        image = parts[-1] if len(parts) > 2 else "nginx"
        container_id = generate_id()
        containers.append({
            "id": container_id,
            "image": image,
            "status": "Up 2 seconds",
            "name": f"{image.split(':')[0]}_{container_id[:4]}"
        })
        return {
            "success": True,
            "output": f"✅ Container started!\n```\n{container_id}\n```",
            "explanation": EXPLANATIONS.get("run")
        }
    
    elif subcmd == "ps":
        if not containers:
            output = "```\nCONTAINER ID   IMAGE   STATUS   NAMES\n```\n_No containers_"
        else:
            output = "```\nCONTAINER ID   IMAGE          STATUS          NAMES\n"
            for c in containers:
                output += f"{c['id'][:12]}   {c['image']:14} {c['status']:15} {c['name']}\n"
            output += "```"
        return {"success": True, "output": output, "explanation": EXPLANATIONS.get("ps")}
    
    elif subcmd == "images":
        output = "```\nREPOSITORY    TAG          IMAGE ID       SIZE\n"
        for img in images:
            output += f"{img['repository']:13} {img['tag']:12} {img['id']}   {img['size']}\n"
        output += "```"
        return {"success": True, "output": output, "explanation": EXPLANATIONS.get("images")}
    
    elif subcmd == "build":
        return {
            "success": True,
            "output": f"🔨 Building...\n```\nStep 1/5 : FROM node:18-alpine\nStep 2/5 : WORKDIR /app\nStep 3/5 : COPY . .\nStep 4/5 : RUN npm install\nStep 5/5 : CMD [\"npm\", \"start\"]\nSuccessfully built {generate_id()}\n```",
            "explanation": EXPLANATIONS.get("build")
        }
    
    elif subcmd == "stop":
        if len(parts) > 2 and containers:
            target = parts[2]
            for c in containers:
                if c["id"].startswith(target) or c["name"] == target:
                    c["status"] = "Exited (0)"
                    return {"success": True, "output": f"🛑 Stopped {c['name']}", "explanation": EXPLANATIONS.get("stop")}
        return {"success": False, "output": "❌ Container not found", "explanation": EXPLANATIONS.get("stop")}
    
    elif subcmd == "logs":
        return {
            "success": True,
            "output": "📜 Logs:\n```\n2024-01-22 10:00:01 [INFO] Started\n2024-01-22 10:00:02 [INFO] Listening on :3000\n```",
            "explanation": None
        }
    
    elif subcmd == "exec":
        return {
            "success": True,
            "output": "🔧 Exec:\n```\nroot@container:/# ls\napp bin etc home lib\nroot@container:/# exit\n```",
            "explanation": None
        }
    
    elif subcmd in ("help", "--help"):
        return {
            "success": True,
            "output": """📚 **Docker Commands**

• `docker run <image>` - Run container
• `docker ps` - List containers
• `docker images` - List images
• `docker build -t name .` - Build image
• `docker stop <id>` - Stop container
• `docker logs <id>` - View logs
• `docker exec -it <id> bash` - Enter container""",
            "explanation": None
        }
    
    return {"success": False, "output": f"❓ Unknown: docker {subcmd}", "explanation": None}


def get_docker_menu():
    return """🐳 **Docker Sandbox**

Practice Docker commands safely!

**Try:**
• `docker run nginx`
• `docker ps`
• `docker images`
• `docker build -t myapp .`
• `docker help`

💡 _All commands are simulated!_"""


def reset():
    global containers
    containers = []
