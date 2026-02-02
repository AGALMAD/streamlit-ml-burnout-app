# MindGuard AI

**MindGuard AI** is an intelligent application designed to detect early signs of professional burnout through natural language analysis. Using Machine Learning models and Generative AI, the tool provides real-time risk assessment and personalized wellness recommendations.

# [Web App](https://agalmad-streamlit-ml-burnout-app-streamlit-app-develop-b14kru.streamlit.app/)

# [Model Code](https://colab.research.google.com/drive/1g4TgEyQ3xQMwWzLuG-ZPpmNntL6Iflrj?usp=sharing)

# [Explanatory Video](https://youtu.be/cxrPAa1c2c4)

## Key Features

- **Burnout Detection**: Analyzes user text input to predict the probability of burnout using a trained SVM model.
- **Interactive Dashboard**: Visualizes risk levels with dynamic gauges and trend indicators using Plotly.
- **AI Chatbot Assistant**: A supportive chat interface powered by **Groq** (LLM) to offer advice, coping strategies, and empathetic conversation.
- **Modular Architecture**: Clean separation of concerns with dedicated components for UI, services, and models.
- **Dark/Light Mode Support**: Optimized UI that adapts seamlessly to your system theme.

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Machine Learning**: Scikit-learn (SVM with calibration), TF-IDF Vectorizer, Pandas, NumPy
- **Visualization**: Plotly Graph Objects
- **LLM/AI**: Groq API
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3.10+

## Installation & Setup

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

## Usage

### Local Development
Run the Streamlit application with the following command:

```bash
streamlit run streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### Docker Deployment
You can also run the application using Docker:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8501`.

## Project Structure

```
streamlit-ml-burnout-app/
├── components/
│   ├── header.py                 # Application header component
│   ├── input_section.py          # User input interface
│   ├── analysis_dashboard.py     # Risk assessment visualization
│   ├── chatbot.py                # AI chatbot interface
│   └── footer.py                 # Footer component
├── services/
│   ├── predictor.py              # ML prediction service (SVM model)
│   └── vectorizer.py             # TF-IDF vectorization service
├── models/
│   ├── svm_calibrated_model.joblib    # Pre-trained SVM classifier
│   └── tfidf_vectorizer.joblib        # TF-IDF vectorizer
├── styles/
│   └── main.css                  # Custom CSS styling
├── streamlit_app.py              # Main application entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker container configuration
├── docker-compose.yml            # Docker Compose orchestration
└── README.md                     # Project documentation
```

## Component Descriptions

- **Header**: Displays the application title and branding
- **Input Section**: Text area for users to describe their work experiences
- **Analysis Dashboard**: Shows burnout risk probability with visual indicators
- **Chatbot**: Interactive assistant powered by Groq LLM for wellness support
- **Footer**: Project information and attribution
- **Predictor Service**: Loads and manages the SVM model for burnout predictions
- **Vectorizer Service**: Handles TF-IDF text vectorization for the ML pipeline

## Model Information

The application uses a **Support Vector Machine (SVM)** classifier with probability calibration:
- **Vectorizer**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Model**: Calibrated SVM for reliable probability estimates
- **Input**: User text describing work-related situations
- **Output**: Burnout risk probability score
