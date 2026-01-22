"""
🧠 AI Error Explainer Module
Uses OpenAI to explain error logs with Sinhala support
"""

import os
from openai import AsyncOpenAI

client = None


def init_openai():
    """Initialize OpenAI client"""
    global client
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        client = AsyncOpenAI(api_key=api_key)
        return True
    return False


async def explain_error(error_log: str, language: str = "en") -> str:
    """Explain error log using AI"""
    if not client:
        if not init_openai():
            return get_fallback_explanation(error_log, language)
    
    try:
        lang_instruction = "Respond in Sinhala (සිංහල)" if language == "si" else "Respond in English"
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a DevOps expert helping students understand error logs.
{lang_instruction}

Analyze the error and explain:
1. What went wrong (simple explanation)
2. Root cause
3. How to fix it
4. Prevention tips

Keep it concise and beginner-friendly."""
                },
                {
                    "role": "user",
                    "content": f"Explain this error:\n\n```\n{error_log[:2000]}\n```"
                }
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return f"🧠 **AI Analysis:**\n\n{response.choices[0].message.content}"
        
    except Exception as e:
        return get_fallback_explanation(error_log, language)


def get_fallback_explanation(error_log: str, language: str = "en") -> str:
    """Fallback pattern-based error detection"""
    error_lower = error_log.lower()
    
    patterns = {
        "connection refused": {
            "en": "🔌 **Connection Refused**\n\nThe service you're trying to connect to isn't running or is on a different port.\n\n**Fix:** Check if the service is running and verify the port number.",
            "si": "🔌 **Connection Refused**\n\nService එක run වෙන්නේ නැත්නම් port එක වෙනස්.\n\n**Fix:** Service run වෙනවද බලන්න, port check කරන්න."
        },
        "permission denied": {
            "en": "🔐 **Permission Denied**\n\nYou don't have permission to access this resource.\n\n**Fix:** Use `sudo` or check file permissions with `ls -la`.",
            "si": "🔐 **Permission Denied**\n\nFile/resource එකට access නැහැ.\n\n**Fix:** `sudo` use කරන්න හෝ permissions check කරන්න."
        },
        "out of memory": {
            "en": "💾 **Out of Memory**\n\nThe system ran out of RAM.\n\n**Fix:** Increase memory limits, optimize code, or add swap space.",
            "si": "💾 **Out of Memory**\n\nRAM මදි.\n\n**Fix:** Memory limits වැඩි කරන්න, code optimize කරන්න."
        },
        "command not found": {
            "en": "❓ **Command Not Found**\n\nThe command isn't installed or not in PATH.\n\n**Fix:** Install the package or add to PATH.",
            "si": "❓ **Command Not Found**\n\nCommand install වෙලා නැහැ හෝ PATH එකේ නැහැ.\n\n**Fix:** Package install කරන්න."
        },
        "port already in use": {
            "en": "🔒 **Port Already in Use**\n\nAnother process is using this port.\n\n**Fix:** Use `lsof -i :PORT` to find and kill the process.",
            "si": "🔒 **Port Already in Use**\n\nවෙන process එකක් port එක use කරනවා.\n\n**Fix:** `lsof -i :PORT` use කරලා process එක kill කරන්න."
        },
        "timeout": {
            "en": "⏱️ **Timeout Error**\n\nThe operation took too long.\n\n**Fix:** Check network connectivity, increase timeout, or optimize the operation.",
            "si": "⏱️ **Timeout Error**\n\nOperation එක වැඩි වෙලාවක් ගත්තා.\n\n**Fix:** Network check කරන්න, timeout වැඩි කරන්න."
        },
        "file not found": {
            "en": "📁 **File Not Found**\n\nThe specified file doesn't exist.\n\n**Fix:** Check the path, ensure file exists, check spelling.",
            "si": "📁 **File Not Found**\n\nFile එක නැහැ.\n\n**Fix:** Path එක check කරන්න, file තියෙනවද බලන්න."
        },
        "syntax error": {
            "en": "📝 **Syntax Error**\n\nThere's a syntax mistake in your code/config.\n\n**Fix:** Check line numbers, missing brackets, quotes, or colons.",
            "si": "📝 **Syntax Error**\n\nCode/config එකේ syntax වැරැද්දක්.\n\n**Fix:** Line numbers බලන්න, brackets/quotes check කරන්න."
        }
    }
    
    for pattern, explanations in patterns.items():
        if pattern in error_lower:
            return explanations.get(language, explanations["en"])
    
    # Generic response
    if language == "si":
        return "🧠 **Error Analysis**\n\nමෙම error එක analyze කරන්න AI API key එකක් අවශ්‍යයි.\n\n**Tips:**\n• Error message එක හොඳින් කියවන්න\n• Line numbers check කරන්න\n• Google search කරන්න"
    
    return "🧠 **Error Analysis**\n\nCouldn't auto-detect the error pattern. Add an OpenAI API key for AI-powered analysis.\n\n**Tips:**\n• Read the error message carefully\n• Check line numbers mentioned\n• Search the error online"


def get_ai_menu():
    return """🧠 **AI Error Explainer**

Send me any error log and I'll explain:
• 🔍 What went wrong
• 🎯 Root cause
• 🔧 How to fix it
• 💡 Prevention tips

**Sinhala Support:**
Add `/si` at the end for Sinhala explanation!

**Example:**
```
Error: EADDRINUSE: address already in use :3000
```

💡 _Powered by AI - paste your error logs!_"""


async def translate_to_sinhala(text: str) -> str:
    """Translate text to Sinhala using AI"""
    if not client:
        return text
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate the following DevOps explanation to Sinhala. Keep technical terms in English."},
                {"role": "user", "content": text}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except:
        return text
