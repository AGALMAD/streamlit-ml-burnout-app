# 🧠 MindGuard AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Groq](https://img.shields.io/badge/Groq-AI-f55036)

**MindGuard AI** is a workplace stress analysis tool that bridges the gap between traditional machine learning and generative AI. It combines linguistic analysis to detect burnout risks with an empathetic AI assistant to provide actionable wellness tips.

---

## ✨ Features

- **📊 Linguistic Analysis**: Detects probability of burnout based on text sentiment and keyword patterns using a trained scikit-learn model.
- **🤖 AI Wellness Assistant**: Powered by **Groq** (Llama 3), this assistant provides instant, actionable advice tailored to your needs.
- **⚡ Fast Inference**: Utilizes Groq's LPU™ Inference Engine for near-instantaneous responses.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **ML Engine**: Scikit-learn (Pipeline with TF-IDF & Logistic Regression)
- **GenAI**: Groq API (Llama-3.3-70b-versatile)
- **Visualization**: Plotly

---

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.9+** installed.
2. A **[Groq API Key](https://console.groq.com/keys)**.

---

## 🚀 Setup Guide

### 1. Clone the Repository
```bash
git clone <https://github.com/AGALMAD/streamlit-ml-burnout-app>
cd streamlit-ml-burnout-app
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets
Create a `.streamlit/secrets.toml` file in the root directory and add your Groq API key:

**File:** `.streamlit/secrets.toml`
```toml
GROQ_API_KEY = "gsk_..."
```

> **Note:** Do not commit this file to version control.

### 4. Run the Application
```bash
streamlit run streamlit_app.py
```

---

## 💻 Usage

1. Open your browser to `http://localhost:8501`.
2. **Left Panel**: View the project title and mission.
3. **Center Panel (Analysis)**: 
   - Type or paste descriptive text about your workday/feelings.
   - Click **Start Analysis** to get a burnout risk score.
4. **Right Panel (Assistant)**: 
   - Click the **💬 Open Wellness Assistant** button.
   - Chat with the AI to get stress relief tips (e.g., "Give me a 5-minute breathing exercise").

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **Missing API Key** | Ensure you have created `.streamlit/secrets.toml` with the correct `GROQ_API_KEY`. |
| **Model Not Found** | Verify `modelo_burnout_pipeline.pkl` exists in the `models/` directory or root, depending on your structure. |
| **Dependencies** | Run `pip install -r requirements.txt` to ensure all packages are installed. |

---


<div align="center">
    <i>MindGuard AI - Decoding Workplace Stress through Linguistic Intelligence</i>
</div>
