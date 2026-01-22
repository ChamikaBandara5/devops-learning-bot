"""
📊 YAML Validator + Explainer Module
Validates YAML syntax and explains structure
"""

import yaml


def validate_yaml(content: str) -> dict:
    """Validate YAML content and return result with explanation"""
    try:
        parsed = yaml.safe_load(content)
        
        if parsed is None:
            return {
                "valid": True,
                "output": "✅ Valid YAML (empty document)",
                "parsed": None,
                "explanation": None
            }
        
        # Detect YAML type and provide explanation
        explanation = analyze_yaml_structure(parsed)
        
        return {
            "valid": True,
            "output": "✅ **Valid YAML!**",
            "parsed": parsed,
            "explanation": explanation
        }
        
    except yaml.YAMLError as e:
        error_msg = str(e)
        return {
            "valid": False,
            "output": f"❌ **Invalid YAML**\n\n```\n{error_msg}\n```",
            "parsed": None,
            "explanation": get_common_errors()
        }


def analyze_yaml_structure(parsed: dict) -> str:
    """Analyze YAML structure and provide explanation"""
    if not isinstance(parsed, dict):
        return f"📊 This YAML contains a {type(parsed).__name__}"
    
    # Check for Kubernetes manifest
    if "apiVersion" in parsed and "kind" in parsed:
        kind = parsed.get("kind", "Unknown")
        return f"""📊 **Kubernetes {kind} Manifest**

**Structure:**
• `apiVersion`: {parsed.get('apiVersion')} - API version
• `kind`: {kind} - Resource type
• `metadata`: Resource metadata (name, labels)
• `spec`: Desired state configuration

💡 Use `kubectl apply -f file.yaml` to deploy"""
    
    # Check for GitHub Actions
    if "name" in parsed and ("on" in parsed or "jobs" in parsed):
        jobs = list(parsed.get("jobs", {}).keys())
        return f"""📊 **GitHub Actions Workflow**

**Structure:**
• `name`: Workflow name
• `on`: Trigger events
• `jobs`: {len(jobs)} job(s) - {', '.join(jobs[:3])}

💡 Place in `.github/workflows/`"""
    
    # Check for Docker Compose
    if "services" in parsed or "version" in parsed:
        services = list(parsed.get("services", {}).keys())
        return f"""📊 **Docker Compose File**

**Structure:**
• `version`: Compose version
• `services`: {len(services)} service(s) - {', '.join(services[:3])}
• `volumes`: Persistent storage
• `networks`: Custom networks

💡 Run with `docker-compose up -d`"""
    
    # Generic YAML
    keys = list(parsed.keys())[:5]
    return f"""📊 **YAML Structure**

**Top-level keys:** {', '.join(keys)}
**Type:** Configuration file

💡 YAML uses indentation for nesting"""


def get_common_errors() -> str:
    """Return common YAML errors and fixes"""
    return """⚠️ **Common YAML Errors:**

1. **Indentation** - Use spaces, not tabs
2. **Colons** - Need space after `key: value`
3. **Strings** - Quote special characters
4. **Lists** - Start items with `- `

**Example:**
```yaml
# ✅ Correct
name: my-app
ports:
  - 8080
  - 3000

# ❌ Wrong
name:my-app  # No space after colon
```"""


def get_yaml_menu():
    return """📊 **YAML Validator + Explainer**

Send me any YAML to:
• ✅ Validate syntax
• 📖 Explain structure
• 🔍 Detect file type (K8s, Docker Compose, GitHub Actions)

**Supported:**
• Kubernetes manifests
• Docker Compose files
• GitHub Actions workflows
• Any YAML config

💡 _Just paste your YAML!_"""


def yaml_to_json_preview(content: str) -> str:
    """Convert YAML to JSON preview"""
    try:
        import json
        parsed = yaml.safe_load(content)
        return f"```json\n{json.dumps(parsed, indent=2)[:500]}\n```"
    except:
        return "❌ Could not convert to JSON"
