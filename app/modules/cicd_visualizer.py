"""
🧪 CI/CD Pipeline Visualizer Module
Parses and visualizes GitHub Actions workflows
"""

import yaml

SAMPLE_WORKFLOWS = {
    "nodejs": """name: Node.js CI/CD
on:
  push:
    branches: [ main ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm test
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..." """,

    "docker": """name: Docker Build
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: myapp:latest"""
}


def parse_workflow(content: str) -> dict:
    """Parse GitHub Actions workflow YAML"""
    try:
        workflow = yaml.safe_load(content)
        
        if not workflow or "jobs" not in workflow:
            return {"success": False, "error": "Invalid workflow: No jobs found"}
        
        jobs = []
        for name, config in workflow.get("jobs", {}).items():
            needs = config.get("needs", [])
            if isinstance(needs, str):
                needs = [needs]
            
            jobs.append({
                "name": name,
                "runs_on": config.get("runs-on", "ubuntu-latest"),
                "needs": needs,
                "steps": len(config.get("steps", []))
            })
        
        return {
            "success": True,
            "name": workflow.get("name", "Workflow"),
            "trigger": workflow.get("on", {}),
            "jobs": jobs
        }
    except yaml.YAMLError as e:
        return {"success": False, "error": f"YAML error: {str(e)}"}


def visualize_pipeline(workflow: dict) -> str:
    """Generate ASCII visualization of pipeline"""
    if not workflow.get("success"):
        return f"❌ {workflow.get('error')}"
    
    output = f"🧪 **{workflow['name']}**\n\n```\n"
    output += "┌─────────────────────────────┐\n"
    output += "│      CI/CD PIPELINE         │\n"
    output += "└─────────────────────────────┘\n"
    
    # Sort jobs by dependencies
    sorted_jobs = topological_sort(workflow["jobs"])
    
    for job_name in sorted_jobs:
        job = next(j for j in workflow["jobs"] if j["name"] == job_name)
        output += "            │\n            ▼\n"
        output += f"    ┌─────────────────────┐\n"
        output += f"    │ 📦 {job['name'][:17]:17}│\n"
        output += f"    │   {job['steps']} steps{' ' * 10}│\n"
        output += f"    └─────────────────────┘\n"
    
    output += "            │\n            ▼\n"
    output += "    ┌─────────────────────┐\n"
    output += "    │    ✅ COMPLETE      │\n"
    output += "    └─────────────────────┘\n```"
    
    return output


def explain_workflow(workflow: dict, lang: str = "en") -> str:
    """Explain workflow in detail"""
    if not workflow.get("success"):
        return f"❌ {workflow.get('error')}"
    
    title = "📖 **Workflow පැහැදිලි කිරීම**" if lang == "si" else "📖 **Workflow Explanation**"
    output = f"{title}\n\n"
    
    # Triggers
    triggers = workflow.get("trigger", {})
    if isinstance(triggers, dict):
        trigger_list = list(triggers.keys())
        output += f"**Triggers:** {', '.join(trigger_list)}\n\n"
    
    # Jobs
    output += "**Jobs:**\n\n"
    for job in workflow["jobs"]:
        output += f"**{job['name']}**\n"
        output += f"• Runs on: `{job['runs_on']}`\n"
        if job["needs"]:
            output += f"• Depends on: {', '.join(job['needs'])}\n"
        output += f"• Steps: {job['steps']}\n\n"
    
    return output


def topological_sort(jobs: list) -> list:
    """Sort jobs by dependencies"""
    result = []
    visited = set()
    job_map = {j["name"]: j for j in jobs}
    
    def visit(name):
        if name in visited:
            return
        visited.add(name)
        job = job_map.get(name)
        if job:
            for dep in job.get("needs", []):
                visit(dep)
        result.append(name)
    
    for job in jobs:
        visit(job["name"])
    
    return result


def get_sample(name: str) -> dict:
    """Get sample workflow"""
    key = name.lower().replace("sample ", "").strip()
    if key in SAMPLE_WORKFLOWS:
        return {"yaml": SAMPLE_WORKFLOWS[key], "type": key}
    return None


def get_cicd_menu():
    return """🧪 **CI/CD Pipeline Visualizer**

Send GitHub Actions YAML or try:
• `sample nodejs` - Node.js CI/CD
• `sample docker` - Docker build

**Features:**
• 📊 Visual pipeline diagram
• 📖 Step-by-step explanation
• 🔍 Syntax validation"""
