# 🧠 MindGuard AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Ollama](https://img.shields.io/badge/Ollama-AI-yellow)

**MindGuard AI** is a workplace stress analysis tool that bridges the gap between traditional machine learning and generative AI. It combines linguistic analysis to detect burnout risks with an empathetic AI assistant to provide actionable wellness tips.

---

## ✨ Features

- **📊 Linguistic Analysis**: Detects probability of burnout based on text sentiment and keyword patterns.
- **🤖 AI Wellness Assistant**: Validated advice from a local LLM (Ollama/Phi-3) tailored to your stress levels.
- **📉 Visual Dashboard**: Interactive gauge charts and risk scores powered by Plotly.
- **🔒 Privacy-First**: All AI processing happens locally on your machine using Docker and Ollama.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **ML Engine**: Scikit-learn (Pipeline with TF-IDF & Logistic Regression)
- **GenAI**: Ollama (Phi-3 Mini)
- **Containerization**: Docker & Docker Compose

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**: For running the application container.
2. **[Ollama](https://ollama.com/)**: For the local AI chatbot.

---

## � Setup Guide

### 1. Configure Ollama (The AI Brain)

Since the AI model runs on your host machine, we need to allow the Docker container to communicate with it.

1. **Download the Model**  
   Open your terminal and pull the lightweight Phi-3 model:
   ```bash
   ollama pull phi3
   ```

2. **Set Environment Variable**  
   To allow external connections (from Docker), set `OLLAMA_HOST`:

   - **Windows**: 
     1. Search for "Edit the system environment variables".
     2. Click **Environment Variables** > **User variables** > **New**.
     3. Name: `OLLAMA_HOST`, Value: `0.0.0.0`
   
   - **Mac/Linux**:
     ```bash
     export OLLAMA_HOST=0.0.0.0
     ```

3. **Restart Ollama**  
   Quit the Ollama application from the taskbar and open it again to apply the changes.

### 2. Launch the Application

1. **Clone the Repository**
   ```bash
   git clone <your-repo-link>
   cd streamlit-ml-burnout-app
   ```

2. **Run with Docker Compose**
   ```bash
   docker compose up --build
   ```
   *This will install dependencies and start the server on port 8501.*

---

## 💻 Usage

1. Open your browser to `http://localhost:8501`.
2. **Left Panel**: View the project title and mission.
3. **Center Panel (Analysis)**: 
   - Type or paste descriptive text about your workday/feelings.
   - Click **Start Analysis** to get a burnout risk score.
4. **Right Panel (Assistant)**: 
   - Click the **💬 Open Assistant** button.
   - Chat with the AI to get stress relief tips (e.g., "Give me a 5-minute breathing exercise").

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **Connection Error** | Ensure `OLLAMA_HOST` is set to `0.0.0.0` and Ollama is running. The app uses `host.docker.internal` to connect. |
| **Model Not Found** | Verify `modelo_burnout_pipeline.pkl` exists in the root directory. |
| **Port Conflict** | If port 8501 is busy, change the mapping in `docker-compose.yml` (e.g., `8502:8501`). |

---


<div align="center">
    <i>MindGuard AI - Decoding Workplace Stress through Linguistic Intelligence</i>
</div>