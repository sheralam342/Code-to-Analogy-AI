import streamlit as st
from groq import Groq

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CodeAnalogy AI", 
    page_icon="💡", 
    layout="centered"
)

# Custom CSS to make it look a bit more modern
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("💡 Code-to-Analogy Translator")
st.markdown("""
**Stop struggling with abstract code!** Paste any piece of programming logic below, 
and this AI will translate it into a simple, real-world analogy that anyone can understand.
""")
st.divider()

# --- API KEY SETUP ---
# It checks for the key in Streamlit Secrets (for cloud) or Sidebar (for local testing)
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Groq API Key", type="password", help="Get your key from console.groq.com")

if not api_key:
    st.info("🔑 Please provide your Groq API key in the sidebar to activate the AI.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# --- USER INTERFACE ---
col1, col2 = st.columns([1, 1])

with st.container():
    code_input = st.text_area(
        "💻 Paste your code snippet here:", 
        height=250, 
        placeholder="Example: \nfor i in range(5):\n    print('Hello')\n\n# Or a complex Python function..."
    )

    # Analogy Style Selection
    style = st.selectbox(
        "Choose Analogy Style:",
        ("Simple (for a 10-year-old)", "Professional/Corporate", "Funny/Witty", "Kitchen/Cooking themed")
    )

    submit_button = st.button("Translate to Analogy ✨", type="primary")

# --- LOGIC ---
if submit_button:
    if not code_input:
        st.warning("Please paste some code first!")
    else:
        with st.spinner("🧠 Analyzing logic and thinking of a story..."):
            try:
                # THE SYSTEM PROMPT: This defines the "uniqueness" of the app
                system_prompt = (
                    "You are a world-class educator who simplifies complex programming concepts. "
                    f"Your goal is to explain the provided code using a real-world analogy in a {style} style. "
                    "STRICT RULES: \n"
                    "1. Do NOT use technical jargon (like 'iteration', 'boolean', or 'integer').\n"
                    "2. Use a story or a physical object to describe how the code works.\n"
                    "3. Compare components of the code to components of the story (e.g., 'The variable is like a storage box').\n"
                    "4. Keep it concise and engaging."
                )

                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Explain this code: \n\n{code_input}"},
                    ],
                    model="llama3-8b-8192",
                    temperature=0.7,
                )

                result = completion.choices[0].message.content
                
                st.subheader("🌟 The Analogy:")
                st.markdown(f"```{result}```" if style == "Professional/Corporate" else result)
                st.balloons()

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.divider()
st.caption("Built with ❤️ using Groq Llama3 and Streamlit")
