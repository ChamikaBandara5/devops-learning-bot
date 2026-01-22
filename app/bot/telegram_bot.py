"""
🤖 Telegram Bot Handler
Main bot logic for DevOps Learning Assistant
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, ContextTypes, filters
)

from app.modules import docker_sandbox, kubernetes_concepts, yaml_validator
from app.modules import cicd_visualizer, interview_qa, ai_error_explainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User state tracking
user_modes = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    keyboard = [
        [InlineKeyboardButton("🐳 Docker", callback_data="menu_docker"),
         InlineKeyboardButton("☸️ Kubernetes", callback_data="menu_k8s")],
        [InlineKeyboardButton("🧪 CI/CD", callback_data="menu_cicd"),
         InlineKeyboardButton("📊 YAML", callback_data="menu_yaml")],
        [InlineKeyboardButton("📝 Quiz", callback_data="menu_quiz"),
         InlineKeyboardButton("🧠 AI Error", callback_data="menu_ai")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome = """🚀 **DevOps Learning Assistant**

Welcome! I'll help you learn:
• 🐳 Docker commands
• ☸️ Kubernetes concepts  
• 🧪 CI/CD pipelines
• 📊 YAML validation
• 📝 Interview prep
• 🧠 Error analysis (සිංහල supported!)

Select a topic below or use commands:
/docker /kubernetes /cicd /yaml /quiz /explain"""

    await update.message.reply_text(welcome, reply_markup=reply_markup, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if data == "menu_docker":
        user_modes[user_id] = "docker"
        await query.edit_message_text(docker_sandbox.get_docker_menu(), parse_mode="Markdown")
    
    elif data == "menu_k8s":
        user_modes[user_id] = "kubernetes"
        await query.edit_message_text(kubernetes_concepts.get_kubernetes_menu(), parse_mode="Markdown")
    
    elif data == "menu_cicd":
        user_modes[user_id] = "cicd"
        await query.edit_message_text(cicd_visualizer.get_cicd_menu(), parse_mode="Markdown")
    
    elif data == "menu_yaml":
        user_modes[user_id] = "yaml"
        await query.edit_message_text(yaml_validator.get_yaml_menu(), parse_mode="Markdown")
    
    elif data == "menu_quiz":
        user_modes[user_id] = "quiz"
        await query.edit_message_text(interview_qa.get_interview_menu(), parse_mode="Markdown")
    
    elif data == "menu_ai":
        user_modes[user_id] = "ai"
        await query.edit_message_text(ai_error_explainer.get_ai_menu(), parse_mode="Markdown")


async def docker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /docker command"""
    user_modes[str(update.effective_user.id)] = "docker"
    await update.message.reply_text(docker_sandbox.get_docker_menu(), parse_mode="Markdown")


async def kubernetes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kubernetes command"""
    user_modes[str(update.effective_user.id)] = "kubernetes"
    await update.message.reply_text(kubernetes_concepts.get_kubernetes_menu(), parse_mode="Markdown")


async def cicd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cicd command"""
    user_modes[str(update.effective_user.id)] = "cicd"
    await update.message.reply_text(cicd_visualizer.get_cicd_menu(), parse_mode="Markdown")


async def yaml_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /yaml command"""
    user_modes[str(update.effective_user.id)] = "yaml"
    await update.message.reply_text(yaml_validator.get_yaml_menu(), parse_mode="Markdown")


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quiz command"""
    user_id = str(update.effective_user.id)
    user_modes[user_id] = "quiz"
    
    # Get category from command args
    args = context.args
    category = args[0] if args else None
    
    session = interview_qa.get_quiz_session(user_id)
    question = session.start(category)
    
    await update.message.reply_text(
        f"📝 **Question {question['number']}** ({question['category']})\n\n{question['question']}\n\n_Use /answer to reveal, /next for next question_",
        parse_mode="Markdown"
    )


async def answer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /answer command"""
    user_id = str(update.effective_user.id)
    session = interview_qa.get_quiz_session(user_id)
    
    # Check for Sinhala flag
    lang = "si" if context.args and "si" in context.args else "en"
    answer = session.reveal_answer(lang)
    
    await update.message.reply_text(answer, parse_mode="Markdown")


async def next_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /next command"""
    user_id = str(update.effective_user.id)
    session = interview_qa.get_quiz_session(user_id)
    question = session.next_question()
    
    await update.message.reply_text(
        f"📝 **Question {question['number']}**\n\n{question['question']}",
        parse_mode="Markdown"
    )


async def explain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /explain command"""
    user_modes[str(update.effective_user.id)] = "ai"
    await update.message.reply_text(ai_error_explainer.get_ai_menu(), parse_mode="Markdown")


async def concept_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle K8s concept commands like /pod, /deployment, etc."""
    concept = update.message.text.strip("/").lower()
    lang = "si" if context.args and "si" in context.args else "en"
    
    explanation = kubernetes_concepts.get_concept(concept, lang)
    if explanation:
        await update.message.reply_text(explanation, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❓ Unknown concept: {concept}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages based on user mode"""
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    mode = user_modes.get(user_id, "docker")
    
    # Check for Sinhala flag
    lang = "si" if text.endswith("/si") else "en"
    if text.endswith("/si"):
        text = text[:-3].strip()
    
    if mode == "docker" and text.lower().startswith("docker"):
        result = docker_sandbox.simulate_docker(text)
        response = result["output"]
        if result.get("explanation"):
            exp = result["explanation"].get(lang, result["explanation"].get("en", ""))
            response += f"\n\n{exp}"
        await update.message.reply_text(response, parse_mode="Markdown")
    
    elif mode == "kubernetes" and text.lower().startswith("kubectl"):
        result = kubernetes_concepts.simulate_kubectl(text)
        response = result["output"]
        if result.get("explanation"):
            exp = result["explanation"].get(lang, result["explanation"].get("en", ""))
            response += f"\n\n{exp}"
        await update.message.reply_text(response, parse_mode="Markdown")
    
    elif mode == "yaml" or text.strip().startswith(("apiVersion:", "name:", "version:", "services:")):
        result = yaml_validator.validate_yaml(text)
        response = result["output"]
        if result.get("explanation"):
            response += f"\n\n{result['explanation']}"
        await update.message.reply_text(response, parse_mode="Markdown")
    
    elif mode == "cicd":
        if text.lower().startswith("sample"):
            sample = cicd_visualizer.get_sample(text)
            if sample:
                workflow = cicd_visualizer.parse_workflow(sample["yaml"])
                response = cicd_visualizer.visualize_pipeline(workflow)
                response += f"\n\n{cicd_visualizer.explain_workflow(workflow, lang)}"
            else:
                response = "❓ Unknown sample. Try: `sample nodejs` or `sample docker`"
        else:
            workflow = cicd_visualizer.parse_workflow(text)
            response = cicd_visualizer.visualize_pipeline(workflow)
            if workflow.get("success"):
                response += f"\n\n{cicd_visualizer.explain_workflow(workflow, lang)}"
        await update.message.reply_text(response, parse_mode="Markdown")
    
    elif mode == "ai" or any(err in text.lower() for err in ["error", "exception", "failed", "denied"]):
        await update.message.reply_text("🔄 Analyzing error...", parse_mode="Markdown")
        response = await ai_error_explainer.explain_error(text, lang)
        await update.message.reply_text(response, parse_mode="Markdown")
    
    else:
        # Try to auto-detect command type
        if text.lower().startswith("docker"):
            result = docker_sandbox.simulate_docker(text)
            await update.message.reply_text(result["output"], parse_mode="Markdown")
        elif text.lower().startswith("kubectl"):
            result = kubernetes_concepts.simulate_kubectl(text)
            await update.message.reply_text(result["output"], parse_mode="Markdown")
        else:
            await update.message.reply_text(
                "💡 Use /start to see available options or type:\n• `docker <command>`\n• `kubectl <command>`",
                parse_mode="Markdown"
            )


def create_bot_application():
    """Create and configure the bot application"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        logger.warning("⚠️ TELEGRAM_BOT_TOKEN not set!")
        return None
    
    application = Application.builder().token(token).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("docker", docker_command))
    application.add_handler(CommandHandler("kubernetes", kubernetes_command))
    application.add_handler(CommandHandler("k8s", kubernetes_command))
    application.add_handler(CommandHandler("cicd", cicd_command))
    application.add_handler(CommandHandler("yaml", yaml_command))
    application.add_handler(CommandHandler("quiz", quiz_command))
    application.add_handler(CommandHandler("answer", answer_command))
    application.add_handler(CommandHandler("next", next_command))
    application.add_handler(CommandHandler("explain", explain_command))
    
    # K8s concept commands
    for concept in ["pod", "deployment", "service", "configmap", "secret", "ingress", "namespace"]:
        application.add_handler(CommandHandler(concept, concept_command))
    
    # Button callback handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return application
