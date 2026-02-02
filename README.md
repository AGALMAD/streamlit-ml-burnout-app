# 🧠 MindGuard AI

**MindGuard AI** is an intelligent application designed to detect early signs of professional burnout through natural language analysis. Using Machine Learning models and Generative AI, the tool provides real-time risk assessment and personalized wellness recommendations.

## ✨ Key Features

- **�️ Burnout Detection**: Analyzes user text input to predict the probability of burnout using a trained Scikit-learn model.
- **📊 Interactive Dashboard**: Visualizes risk levels with dynamic gauges and trend indicators using Plotly.
- **🤖 AI Chatbot Assistant**: A supportive chat interface powered by **Groq** (LLM) to offer advice, coping strategies, and empathetic conversation.
- **🌗 Dark/Light Mode Support**: Optimised UI that adapts seamlessly to your system theme.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Visualization**: Plotly Graph Objects
- **LLM/AI**: Groq API
- **Language**: Python 3.10+

## � Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/AGALMAD/streamlit-ml-burnout-app.git
cd streamlit-ml-burnout-app
```

### 2. Install Dependencies
Ensure you have Python installed. It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
This project requires a **Groq API Key** for the chatbot functionality.
1. Create a `.streamlit` folder in the root directory if it doesn't exist.
2. Create a `secrets.toml` file inside it:
3. Add your API key:
   ```toml
   # .streamlit/secrets.toml
   GROQ_API_KEY = "gsk_..."
   ```

## 🖥️ Usage

Run the Streamlit application with the following command:

```bash
streamlit run streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## 📂 Project Structure

```
streamlit-ml-burnout-app/
├── components/          # UI Components (Header, Footer, Chatbot, etc.)
├── models/              # Pre-trained ML models (.pkl files)
├── services/            # Logic for predictions and backend services
├── styles/              # CSS files for custom styling
├── .streamlit/          # Configuration and secrets (gitignored)
├── streamlit_app.py     # Main application entry point
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
