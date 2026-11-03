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

    /* Title Styling */
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

    /* Card Styling for the Result */
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
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }

    /* Code input styling */
    .stTextArea textarea {
        font-family: 'Fira Code', monospace !important;
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #3b82f6 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2563eb !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- UI HEADER ---
st.markdown('<div class="main-title">🚀 CodeAnalogy Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Bridging the gap between complex syntax and human intuition.</div>', unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Control Panel")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("API Key loaded from Secrets")
    else:
        api_key = st.text_input("Groq API Key", type="password")
    
    st.divider()
    
    st.subheader("⚙️ Translation Settings")
    style = st.select_slider(
        "Analogy Complexity",
        options=["ELI5 (Child)", "Beginner", "Professional", "Philosophical"]
    )
    
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7)

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 💻 Input Source")
    code_input = st.text_area(
        "Paste your source code here:", 
        height=400, 
        placeholder="Paste C++, Python, Java, or Javascript code...",
        label_visibility="collapsed"
    )
    submit_button = st.button("Generate Intuition ✨")

with col2:
    st.markdown("### 🌟 Human Interpretation")
    
    if submit_button:
        if not api_key:
            st.error("Please provide an API key in the sidebar.")
        elif not code_input:
            st.warning("The input area is empty. Please provide code.")
        else:
            with st.spinner("⚙️ Decoding logic and crafting analogy..."):
                try:
                    client = Groq(api_key=api_key)
                    
                    # IMPROVED PROFESSIONAL SYSTEM PROMPT
                    system_prompt = (
                        f"You are an elite technical communicator. Your goal is to translate code into a high-quality analogy. "
                        f"Current Complexity Level: {style}. "
                        "Structure your response exactly as follows:\n\n"
                        "1. **The Analogy**: Create a vivid, real-world scenario that mirrors the code's logic. "
                        "Avoid clichés. Be creative and precise.\n"
                        "2. **The Mapping**: Explain exactly which part of the analogy represents which part of the code. "
                        "(e.g., 'The Warehouse = The Array').\n"
                        "3. **The Core Intuition**: One sentence that captures the 'Why' behind this logic.\n\n"
                        "Constraints: Do not use technical jargon in the Analogy section. Use professional, polished language."
                    )

                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"Translate this code into a professional analogy:\n\n{code_input}"},
                        ],
                        model="openai/gpt-oss-120b", # Using the larger 70b model for much better quality
                        temperature=temperature,
                    )

                    result = completion.choices[0].message.content
                    
                    # Displaying the result in a professional card
                    st.markdown(f"""
                        <div class="result-card">
                            <div class="analogy-header">✨ Interpretation Complete</div>
                            <div style="color: #334155; line-height: 1.6;">
                                {result.replace('\n', '<br>')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Your translation will appear here once you click 'Generate Intuition'.")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #94a3b8; font-size: 12px;">Powered by Groq Llama3-70B & Streamlit Pro UI</div>', unsafe_allow_html=True)
