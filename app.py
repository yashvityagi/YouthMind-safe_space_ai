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
import streamlit as st
from ui_style import set_modern_3d_ui

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
        <style>
        /* 1. THE DYNAMIC BACKGROUND */
        .stApp {
            background: linear-gradient(125deg, #0a192f 0%, #0a192f 40%, #112240 100%);
            background-attachment: fixed;
        }

        /* Animated Aurora Orbs for 3D Depth */
        .stApp::before {
            content: "";
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 50% 50%, rgba(78, 204, 163, 0.1) 0%, transparent 25%),
                        radial-gradient(circle at 20% 30%, rgba(69, 183, 209, 0.1) 0%, transparent 30%);
            animation: rotate 30s linear infinite;
            z-index: -1;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        /* 2. GLASSMORPHISM LAYERS */
        [data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.04) !important;
            backdrop-filter: blur(15px);
            border-radius: 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            padding: 20px !important;
        }

        /* 3. MODERN TYPOGRAPHY */
        h1, h2, h3, p, span {
            color: #e6f1ff !important;
            font-family: 'Inter', sans-serif;
        }

        /* 4. CHAT INPUT STYLING */
        .stChatInputContainer {
            background: transparent !important;
            bottom: 30px !important;
        }
        
        .stChatInputContainer div {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 30px !important;
        }

        /* 5. HIDE DEFAULT ELEMENTS */
        header, footer { visibility: hidden; }
        
        /* Modern Button Styling */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            background: rgba(78, 204, 163, 0.1);
            border: 1px solid rgba(78, 204, 163, 0.3);
            color: #4ecca3;
            font-weight: 600;
            padding: 10px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: #4ecca3;
            color: #0a192f;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

# --- 5. MAIN APP ---
# ... (all your imports and logic functions at the top)

def main():
    st.set_page_config(page_title="YouthMind AI", layout="wide", page_icon="🕊️")
    
    # 2. Inject the UI (The CSS-only Aurora)
    from ui_style import set_modern_3d_ui
    set_modern_3d_ui()
    
   

    data = load_data()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 3. Sidebar (Now with Glassmorphism from ui_style)
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: white;'>🕊️ YouthMind</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.error("🆘 **Crisis Support**\n\nCall **999** or Text **SHOUT** to **85258**")
        st.markdown("---")
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

    # 4. Centered Chat Layout
    _, chat_col, _ = st.columns([1, 2, 1])

    with chat_col:
        # Title with a modern glowing effect
        with chat_col:
        # REPLACE YOUR OLD TITLE WITH THIS LINE:
            st.markdown('<p class="glowing-title">Safe Space AI</p>', unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #4ecca3; opacity: 0.7;'>Your private space to talk and heal.</p>", unsafe_allow_html=True)
        
        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Quick Suggestion Buttons (Only shown at start)
        if not st.session_state.messages:
            st.markdown("<p style='text-align:center;'>How can I help you today?</p>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            if c1.button("🎓 Exam Stress"): 
                process_user_input("I'm feeling very stressed about my upcoming exams.", data)
            if c2.button("😟 Anxiety Help"): 
                process_user_input("I'm feeling anxious and need some grounding techniques.", data)
            if c3.button("🤝 Loneliness"): 
                process_user_input("I've been feeling quite lonely and isolated lately.", data)

        # 5. Fixed Chat Input at the bottom
        if prompt := st.chat_input("Tell me what's on your mind..."):
            process_user_input(prompt, data)

if __name__ == "__main__":
    main()