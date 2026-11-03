import streamlit as st
from groq import Groq

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CodeAnalogy Pro", 
    page_icon="🚀", 
    layout="wide"
)

# --- PROFESSIONAL MODERN CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Fira+Code:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8fafc;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1e293b;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .sub-title {
        font-size: 18px;
        color: #64748b;
        text-align: center;
        margin-bottom: 40px;
    }

    .result-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }

    .analogy-header {
        color: #3b82f6;
        font-weight: 600;
        font-size: 20px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }

    .stTextArea textarea {
        font-family: 'Fira Code', monospace !important;
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #3b82f6 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI HEADER ---
st.markdown('<div class="main-title">🚀 CodeAnalogy Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Turning scary code into simple, everyday stories.</div>', unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
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

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 💻 Paste Your Code")
    code_input = st.text_area(
        "Enter source code:", 
        height=400, 
        placeholder="Paste C++, Python, etc...",
        label_visibility="collapsed"
    )
    submit_button = st.button("Simplify Logic ✨")

with col2:
    st.markdown("### 🌟 Simple Interpretation")
    
    if submit_button:
        if not api_key:
            st.error("Please provide an API key in the sidebar.")
        elif not code_input:
            st.warning("Please paste some code first.")
        else:
            with st.spinner("⚙️ Translating to simple words..."):
                try:
                    client = Groq(api_key=api_key)
                    
                    # NEW & IMPROVED SYSTEM PROMPT: Focused on simplicity
                    system_prompt = (
                        f"You are an expert at making hard things simple. Your goal is to explain code to {style}. "
                        "STRICT RULES FOR VOCABULARY:\n"
                        "1. Use ONLY plain, everyday English. Avoid big words.\n"
                        "2. NO technical jargon. Instead of 'iterate', say 'go through'. Instead of 'allocate', say 'set aside'.\n"
                        "3. Use a vivid, real-world analogy (like using a kitchen, a library, or a grocery store).\n"
                        "4. Keep sentences short and clear.\n\n"
                        "STRUCTURE YOUR RESPONSE AS:\n"
                        "- **The Story**: A simple 2-3 sentence analogy.\n"
                        "- **How it matches**: A simple list (e.g., 'The Box = The Variable').\n"
                        "- **The Main Idea**: One simple sentence explaining the goal of the code."
                    )

                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Explain this code in very simple words:\n\n{code_input}"},
                        ],
                        model="openai/gpt-oss-120b", 
                        temperature=temperature,
                    )

                    result = completion.choices[0].message.content
                    
                    # Display the result in the professional card
                    st.markdown(f"""
                        <div class="result-card">
                            <div class="analogy-header">✨ Simple Explanation</div>
                            <div style="color: #334155; line-height: 1.6; font-size: 17px;">
                                {result.replace('\n', '<br>')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Paste your code on the left and click 'Simplify Logic' to see the magic.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #94a3b8; font-size: 12px;">Professional UI • Simple Language • Powered by Groq</div>', unsafe_allow_html=True)
