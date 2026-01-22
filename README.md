# 🚀 DevOps Learning Assistant Bot

A comprehensive DevOps learning assistant with **Telegram bot** and **Web interface**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🐳 **Docker Sandbox** | Safe Docker command simulation |
| ☸️ **Kubernetes Concepts** | kubectl simulations & concept explanations |
| 🧪 **CI/CD Visualizer** | GitHub Actions pipeline visualization |
| 📊 **YAML Validator** | Validate & explain YAML files |
| 📝 **Interview Quiz** | DevOps interview Q&A with 5 categories |
| 🧠 **AI Error Explainer** | AI-powered error analysis (Sinhala support!) |

## 🛠️ Tech Stack

- **Backend:** Python + FastAPI
- **Bot:** python-telegram-bot
- **AI:** OpenAI GPT-4 (optional)
- **Deployment:** Docker / Railway / Render

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/devops-learning-bot.git
cd devops-learning-bot
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
TELEGRAM_BOT_TOKEN=your_token_from_botfather
OPENAI_API_KEY=your_openai_key  # Optional
```

### 3. Run
```bash
python main.py
```

- **Web Dashboard:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 🤖 Telegram Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Show main menu |
| `/docker` | Docker command sandbox |
| `/kubernetes` or `/k8s` | Kubernetes simulator |
| `/quiz [category]` | Start interview quiz |
| `/yaml` | YAML validator mode |
| `/explain` | AI error explainer |

### Sinhala Support 🇱🇰
- Add `/si` to get answers in Sinhala
- Example: `/answer si`

## 🌐 Deployment

### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Connect your GitHub repo
2. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY` (optional)
3. Deploy!

### Docker
```bash
docker build -t devops-bot .
docker run -d -p 8000:8000 --env-file .env devops-bot
```

### Render
1. Create new Web Service
2. Connect GitHub repo
3. Set environment variables
4. Deploy

## 📁 Project Structure

```
├── main.py                 # FastAPI entry point
├── requirements.txt        # Dependencies
├── Dockerfile             # Docker deployment
├── Procfile               # Heroku/Railway
├── app/
│   ├── bot/
│   │   └── telegram_bot.py
│   └── modules/
│       ├── docker_sandbox.py
│       ├── kubernetes_concepts.py
│       ├── yaml_validator.py
│       ├── cicd_visualizer.py
│       ├── interview_qa.py
│       └── ai_error_explainer.py
└── public/
    ├── index.html
    ├── css/styles.css
    └── js/app.js
```

## 📄 License

MIT License - feel free to use and modify!

---

Made with ❤️ for DevOps learners
