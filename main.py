"""
🚀 DevOps Learning Assistant - Main Entry Point
FastAPI server with Telegram bot integration
"""

import os
import asyncio
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.bot.telegram_bot import create_bot_application
from app.modules import docker_sandbox, kubernetes_concepts, yaml_validator
from app.modules import cicd_visualizer, interview_qa, ai_error_explainer

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot application
bot_app = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for FastAPI"""
    global bot_app
    
    # Initialize OpenAI
    ai_error_explainer.init_openai()
    
    # Start Telegram bot
    bot_app = create_bot_application()
    if bot_app:
        await bot_app.initialize()
        await bot_app.start()
        asyncio.create_task(bot_app.updater.start_polling())
        logger.info("✅ Telegram bot started!")
    else:
        logger.warning("⚠️ Telegram bot not started - check TELEGRAM_BOT_TOKEN")
    
    logger.info("🚀 DevOps Learning Assistant is running!")
    
    yield
    
    # Cleanup
    if bot_app:
        await bot_app.updater.stop()
        await bot_app.stop()
        await bot_app.shutdown()


# Create FastAPI app
app = FastAPI(
    title="DevOps Learning Assistant",
    description="Learn Docker, Kubernetes, CI/CD, and more!",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="public"), name="static")


# ============ API Routes ============

@app.get("/")
async def root():
    """Serve the web dashboard"""
    return FileResponse("public/index.html")


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "bot_running": bot_app is not None}


# Docker API
@app.post("/api/docker")
async def docker_api(request: Request):
    """Execute Docker command simulation"""
    data = await request.json()
    command = data.get("command", "")
    result = docker_sandbox.simulate_docker(command)
    return JSONResponse(result)


# Kubernetes API
@app.post("/api/kubernetes")
async def kubernetes_api(request: Request):
    """Execute kubectl command simulation"""
    data = await request.json()
    command = data.get("command", "")
    result = kubernetes_concepts.simulate_kubectl(command)
    return JSONResponse(result)


@app.get("/api/kubernetes/concept/{name}")
async def k8s_concept(name: str, lang: str = "en"):
    """Get K8s concept explanation"""
    explanation = kubernetes_concepts.get_concept(name, lang)
    return {"concept": name, "explanation": explanation}


# YAML API
@app.post("/api/yaml/validate")
async def yaml_api(request: Request):
    """Validate YAML content"""
    data = await request.json()
    content = data.get("content", "")
    result = yaml_validator.validate_yaml(content)
    return JSONResponse(result)


# CI/CD API
@app.post("/api/cicd/visualize")
async def cicd_api(request: Request):
    """Visualize CI/CD pipeline"""
    data = await request.json()
    content = data.get("content", "")
    workflow = cicd_visualizer.parse_workflow(content)
    return {
        "workflow": workflow,
        "visualization": cicd_visualizer.visualize_pipeline(workflow),
        "explanation": cicd_visualizer.explain_workflow(workflow)
    }


@app.get("/api/cicd/sample/{name}")
async def cicd_sample(name: str):
    """Get sample workflow"""
    sample = cicd_visualizer.get_sample(name)
    if sample:
        return sample
    return {"error": "Sample not found"}


# Quiz API
@app.get("/api/quiz/question")
async def quiz_question(category: str = None):
    """Get random interview question"""
    result = interview_qa.get_random_question(category)
    return result


@app.get("/api/quiz/categories")
async def quiz_categories():
    """Get available quiz categories"""
    return {"categories": interview_qa.get_categories()}


# AI Error API
@app.post("/api/explain")
async def explain_api(request: Request):
    """Explain error using AI"""
    data = await request.json()
    error_log = data.get("error", "")
    lang = data.get("lang", "en")
    explanation = await ai_error_explainer.explain_error(error_log, lang)
    return {"explanation": explanation}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
