# 🕊️ YouthMind: Safe Space AI
🌱 AI Mental Health Assistant


A modern, highly responsive, and empathetic **Youth Mental Health Assistant** designed to provide guided emotional support and instant AI-driven conversations. Built with Python and Streamlit, the application features an immersive, glassmorphic 3D user interface optimized for desktop and mobile viewing.

---

## 🔍 Project Overview

**YouthMind** serves as a digital sanctuary for students and young adults dealing with stress, anxiety, or burnout. The application combines structural knowledge-base querying with state-of-the-art Generative AI to provide seamless hybrid responses.

### Key Features:

* **Intelligent Hybrid Routing:** Uses Natural Language Toolkit (NLTK) lemmatization and TF-IDF Cosine Similarity to instantaneously fetch direct, validated guidance for high-frequency queries. If confidence falls below 40%, it seamlessly escalates the prompt to Google Gemini.
* **Immersive 3D Glassmorphism UI:** Features an animated dual-orb aurora gradient background layer, high-blur glass content cards, distinct user/assistant chat bubble structures, and smooth interactive hover micro-animations.
* **State-Preserved Sessions:** Utilizes Streamlit session states to maintain an ongoing conversation thread without losing previous context during page re-runs.
* **Crisis Safeguard Integration:** Includes permanent, globally visible crisis hotlines in the side navigation panel to ensure safety-first operations.

---

## 🤖 Bot Type: Hybrid AI Assistant

YouthMind utilizes a **Hybrid Retrieval-Augmented & Generative Architecture**:

1. **Rule-Based Retrieval Layer (Local NLP):** Text inputs are normalized, tokenized, stripped of punctuation/stopwords, and lemmatized via `WordNetLemmatizer`. It evaluates vectors against a local structured database (`data.json`) via Scikit-Learn's `TfidfVectorizer`.
2. **Generative LLM Layer (Cloud AI):** When nuanced contextual understanding is required, the app maps out available API resources and dynamically leverages the `gemini-1.5-flash` model via the Google Generative AI SDK to deliver supportive, context-aware prose.

---

## 🚀 Setup & Installation Instructions

### Local Development

Follow these steps to set up and run the application on your local machine:

**1. Clone the Repository:**

```bash
git clone https://github.com/yashvityagi/YouthMind-safe-space-ai.git
cd YouthMind-safe-space-ai

```

**2. Create a Virtual Environment & Activate it:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

**3. Install Dependencies:**

```bash
pip install -r requirements.txt

```

**4. Set Up Environment Variables:**
Create a file named `.env` in the root directory and append your Google Gemini API key:

```env
GOOGLE_API_KEY="your_actual_gemini_api_key"

```

**5. Execute the Application:**

```bash
streamlit run app.py

```

---

### 🌐 Cloud Deployment (Streamlit Community Cloud)

1. Connect your GitHub repository to [share.streamlit.io](https://share.streamlit.io/).
2. Specify the main file path as `app.py`.
3. Open **Advanced Settings** -> **Secrets** and inject your API key using TOML format:
```toml
GOOGLE_API_KEY = "your_actual_gemini_api_key_here"

```


4. Click **Deploy**.

---

## ❓ Sample Questions

The bot handles inputs smoothly through explicit user prompts or interactive quick-action triggers

### Local Database Math Triggers (Score > 0.40):

* *"What is mental health?"*
* *"Social media makes me feel bad about myself"*
* *"I've lost interest in things I used to love."*   +27 more

### Generative AI Triggers (Dynamic Responses):

* *"Can you give me a 5-minute breathing exercise to stop a panic attack?"*
* *"How do I talk to my parents about feeling burned out from college?"*
* *"I feel unmotivated to code or study today, what should I do?"*

---

## 📸 Screenshots
<img width="1919" height="874" alt="image" src="https://github.com/user-attachments/assets/202fc333-03aa-4ac9-971d-6ba518d0ec81" />
<img width="1918" height="865" alt="image" src="https://github.com/user-attachments/assets/111b7d8c-ee6c-472f-862b-630b6d35cff6" />







### 💻 Live Application : https://youthmind-safespaceai-bruq7osn77enhshqjqq6lt.streamlit.app/

