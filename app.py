import streamlit as st
from groq import Groq

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CodeAnalogy Pro", 
    page_icon="🚀", 
    layout="wide" # Keeps the wide capability, but we will center the content via CSS
)

# --- 2. SESSION STATE INITIALIZATION ---
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0
if "result" not in st.session_state:
    st.session_state.result = None

def reset_app():
    st.session_state.result = None
    st.session_state.reset_count += 1

# --- 3. PROFESSIONAL DASHBOARD CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Fira+Code:wght@400;500&display=swap');

    /* Global Font and Background */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #f1f5f9;
    }

        /* This targets the placeholder text specifically */
    .stTextArea textarea::placeholder {
        color: white !important;
        opacity: 0.7 !important; /* Makes it slightly transparent so it looks like a real placeholder */
    }


    /* Centering the entire app content to prevent "too stretched" look */
    .block-container {
        max-width: 1200px; 
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header Styling */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #0f172a;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    .sub-title {
        font-size: 20px;
        color: #64748b;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Result Card Styling */
    .result-card {
        background-color: white;
        padding: 35px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        margin-top: 10px;
        min-height: 400px; /* Matches the input box height for balance */
    }
    .analogy-header {
        color: #3b82f6;
        font-weight: 700;
        font-size: 22px;
        margin-bottom: 20px;
        border-bottom: 2px solid #eff6ff;
        padding-bottom: 10px;
    }

    /* Code Input Area */
    .stTextArea textarea {
        font-family: 'Fira Code', monospace !important;
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border-radius: 15px !important;
        border: none !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child {
        background-color: #3b82f6 !important;
        color: white !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
    }
    div.stButton > button:first-child:hover {
        background-color: #2563eb !important;
        transform: translateY(-2px);
    }
    .reset-btn-container {
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. UI HEADER ---
st.markdown('<div class="main-title">🚀 CodeAnalogy Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Translating complex syntax into human intuition.</div>', unsafe_allow_html=True)

# --- 5. SIDEBAR SETTINGS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Control Panel")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = st.text_input("Groq API Key", type="password")
    
    st.divider()
    st.subheader("⚙️ Simplicity Settings")
    style = st.select_slider(
        "Who is this for?",
        options=["A Child", "A Student", "A Non-Tech Adult", "A Manager"]
    )
    temperature = st.slider("Creativity", 0.0, 1.0, 0.6)

# --- 6. MAIN LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

# --- LEFT COLUMN: INPUT ---
with col1:
    st.markdown("### 💻 Source Code")
    code_input = st.text_area(
        "Enter source code:", 
        height=400, 
       placeholder="Drop your complex source code here to unlock its human intuition... 🚀",
        label_visibility="collapsed",
        key=f"input_{st.session_state.reset_count}"
    )
    
    if st.button("Simplify Logic ✨"):
        if not api_key:
            st.error("Please provide an API key in the sidebar.")
        elif not code_input:
            st.warning("Please paste some code first.")
        else:
            with st.spinner("⚙️ Crafting your analogy..."):
                try:
                    client = Groq(api_key=api_key)
                    system_prompt = (
                        f"You are an expert at making hard things simple. Your goal is to explain code to {style}. "
                        "STRICT RULES FOR VOCABULARY:\n"
                        "1. Use ONLY plain, everyday English. Avoid big words.\n"
                        "2. NO technical jargon. Instead of 'iterate', say 'go through'.\n"
                        "3. Use a vivid, real-world analogy.\n"
                        "4. Keep sentences short and clear.\n\n"
                        "STRUCTURE YOUR RESPONSE AS:\n"
                        "- **The Story**: A simple 2-3 sentence analogy.\n"
                        "- **How it matches**: A simple list.\n"
                        "- **The Main Idea**: One simple sentence."
                    )

                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Explain this code in very simple words:\n\n{code_input}"},
                        ],
                        model="openai/gpt-oss-120b", 
                        temperature=temperature,
                    )
                    st.session_state.result = completion.choices[0].message.content
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {e}")

# --- RIGHT COLUMN: OUTPUT ---
with col2:
    st.markdown("### 🌟 Interpretation")
    
    if st.session_state.result:
        # Result Card with fixed min-height for visual balance
        st.markdown(f"""
            <div class="result-card">
                <div class="analogy-header">✨ Simple Explanation</div>
                <div style="color: #334155; line-height: 1.8; font-size: 18px;">
                    {st.session_state.result.replace('\n', '<br>')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="reset-btn-container">', unsafe_allow_html=True)
        if st.button("🗑️ Clear and Start New"):
            reset_app()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Placeholder that matches the height of the input box
        st.markdown("""
            <div class="result-card" style="display: flex; align-items: center; justify-content: center; text-align: center; color: #94a3b8; font-style: italic;">
                Your simplified interpretation will appear here.
            </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #94a3b8; font-size: 13px;">Professional UI • Human-Centric Design • Powered by Groq Llama3</div>', unsafe_allow_html=True)
