import google.generativeai as genai
import os
import json
import string
import nltk
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# --- 1. INITIALIZATION & SETUP ---
load_dotenv()
google_key = os.getenv("GOOGLE_API_KEY")

def prepare_nltk():
    resources = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']
    for res in resources:
        try:
            nltk.data.find('tokenizers/punkt' if res == 'punkt' else res)
        except LookupError:
            nltk.download(res)

prepare_nltk()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# --- 2. CORE LOGIC FUNCTIONS ---
def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in string.punctuation]
    clean_tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(clean_tokens)

def load_data():
    if not os.path.exists('data.json'):
        return []
    with open('data.json', 'r') as f:
        return json.load(f)

def get_best_response(user_query, dataset):
    if not dataset: return -1, 0.0
    questions = [item.get('question', '') for item in dataset]
    processed_questions = [preprocess_text(q) for q in questions]
    processed_query = preprocess_text(user_query)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_questions + [processed_query])
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    idx = np.argmax(similarities)
    score = similarities[0][idx]
    return idx, score

def ask_gemini(user_query):
    if not google_key:
        return "API Key missing."
    try:
        genai.configure(api_key=google_key)
        # Automatically find the best model available to you
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"You are a supportive Youth Mental Health Assistant. {user_query}")
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# --- 3. THE MISSING FUNCTION (Fixes your error) ---
def process_user_input(prompt, data):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Logic to get response
    idx, score = get_best_response(prompt, data)
    if score > 0.40: 
        res = f"**[Guided Support]** {data[idx]['answer']}"
    else:
        with st.spinner("Connecting to AI..."):
            res = ask_gemini(prompt)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": res})
    st.rerun()

# --- 4. MODERN 3D UI DESIGN ---
def apply_3d_ui():
    st.markdown("""
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>
        
        <style>
        /* Modern Dark Theme Base */
        .stApp { background: #000000; color: white; }
        
        /* 3D Background */
        #vanta-canvas {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1;
        }

        /* Glassmorphism Chat Bubbles */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.07) !important;
            backdrop-filter: blur(12px);
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin-bottom: 15px;
        }

        /* Sidebar Glass */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(20px);
        }

        /* Hide Streamlit Clutter */
        header, footer { visibility: hidden; }
        
        /* Button Styling */
        .stButton>button {
            border-radius: 15px;
            background: rgba(78, 204, 163, 0.2);
            border: 1px solid #4ecca3;
            color: white;
            transition: 0.3s;
        }
        .stButton>button:hover { background: #4ecca3; color: black; }
        </style>

        <div id="vanta-canvas"></div>
        <script>
            VANTA.NET({
                el: "#vanta-canvas",
                mouseControls: true,
                touchControls: true,
                gyroControls: false,
                minHeight: 200.00,
                minWidth: 200.00,
                scale: 1.00,
                scaleMobile: 1.00,
                color: 0x4ecca3,
                backgroundColor: 0x0a192f,
                points: 12.00,
                maxDistance: 24.00,
                spacing: 16.00
            })
        </script>
    """, unsafe_allow_html=True)

# --- 5. MAIN APP ---
def main():
    st.set_page_config(page_title="YouthMind 3D", layout="wide")
    apply_3d_ui()

    data = load_data()

    # Sidebar
    with st.sidebar:
        st.markdown("# 🕊️ YouthMind")
        st.markdown("---")
        st.error("🆘 **Crisis Support**\n\nCall **999** or Text **SHOUT** to **85258**")
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

    # Chat Layout
    _, chat_col, _ = st.columns([1, 2, 1])

    with chat_col:
        st.markdown("<h1 style='text-align: center;'>Safe Space AI</h1>", unsafe_allow_html=True)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Quick Suggestion Pills
        if not st.session_state.messages:
            st.write("How can I help you today?")
            c1, c2, c3 = st.columns(3)
            if c1.button("Exam Stress"): process_user_input("I'm stressed about exams.", data)
            if c2.button("Anxiety Help"): process_user_input("I feel very anxious.", data)
            if c3.button("Loneliness"): process_user_input("I've been feeling lonely.", data)

        # Chat Input
        if prompt := st.chat_input("Tell me what's on your mind..."):
            process_user_input(prompt, data)

if __name__ == "__main__":
    main()