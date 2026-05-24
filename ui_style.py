import streamlit as st

def set_modern_3d_ui():
    st.markdown("""
        <style>
        /* 1. COMPLETELY REMOVE STREAMLIT'S LAYERS */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
            background: #050a14 !important; /* True Dark Base */
        }

        /* 2. THE 3D PERSPECTIVE GRID BACKGROUND */
        /* This creates a subtle 3D 'floor' effect moving in the background */
        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(78, 204, 163, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(78, 204, 163, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
            transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-100px);
            transform-origin: top;
            animation: gridMove 20s linear infinite;
            z-index: 0;
            pointer-events: none;
        }

        @keyframes gridMove {
            from { background-position: 0 0; }
            to { background-position: 0 1000px; }
        }

        /* 3. GLOWING TITLE EFFECT */
        .glowing-title {
            font-size: 4rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 0px;
            letter-spacing: 5px;
            /* The Neon Glow */
            text-shadow: 
                0 0 10px rgba(78, 204, 163, 0.8),
                0 0 20px rgba(78, 204, 163, 0.5),
                0 0 40px rgba(78, 204, 163, 0.3);
            animation: pulse 3s infinite alternate;
        }

        @keyframes pulse {
            from { opacity: 0.8; text-shadow: 0 0 10px #4ecca3; }
            to { opacity: 1; text-shadow: 0 0 30px #4ecca3, 0 0 50px #45b7d1; }
        }

        /* 4. GLASSMORPHISM CHAT BOXES */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            margin-bottom: 20px !important;
        }

        /* 5. SIDEBAR GLASS */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(25px) !important;
        }

        /* Hide Streamlit Header Clutter */
        header { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)