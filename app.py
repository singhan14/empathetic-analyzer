import streamlit as st
from src.data_generator import DataGenerator, Message
from src.analyzer_engine import AnalyzerEngine

# --- Page Config ---
st.set_page_config(
    page_title="Riverline: Empathetic Analyzer",
    layout="wide",
    page_icon="🟣",
    initial_sidebar_state="expanded"
)

# --- Load Custom CSS ---
with open("src/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

@st.cache_resource
def load_analyzer():
    return AnalyzerEngine()

@st.cache_resource
def load_generator():
    return DataGenerator()

generator = load_generator()
analyzer = load_analyzer()

# --- Callback Handler (Fast & Bug-Free) ---
def handle_input():
    """Handle user input, generate response, and clear field instantly."""
    user_text = st.session_state.u_in.strip()
    if user_text:
        # 1. Add User Message
        st.session_state.conversation.append(Message("borrower", user_text))
        
        # 2. Analyze & Generate Response (Instant)
        borrower_msgs = [{"role": m.role, "content": m.content} for m in st.session_state.conversation if m.role == "borrower"]
        analysis = analyzer.classify_intent(borrower_msgs)
        intent = analysis[0]
        
        # 3. Generate Agent Response
        response = analyzer.generate_agent_response(intent, user_text)
        st.session_state.conversation.append(Message("agent", response))
        
        # 4. Clear Input (Must set key to empty)
        st.session_state.u_in = ""

def load_quick_reply(text):
    """Load a quick reply into the conversation."""
    st.session_state.u_in = text
    handle_input()

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🎛️ Simulation Control")
    st.markdown("---")
    
    scenario_options = {
        "job_loss": "😟 Job Loss (Distress)",
        "strategic_default": "😠 Strategic Avoidance",
        "medical_emergency": "🏥 Medical Emergency"
    }
    
    selected_key = st.selectbox(
        "Select Borrower Profile",
        options=list(scenario_options.keys()),
        format_func=lambda x: scenario_options[x],
        key="scenario_select"
    )
    
    if st.button("🚀 Start New Call", use_container_width=True, key="start_btn"):
        scenario = generator.get_scenario(selected_key)
        st.session_state.conversation = list(scenario.conversation_starter)
        st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.conversation = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 👨‍💻 Built by **Singhan Yadav**")

# --- Main Content ---
st.markdown("# 🟣 Riverline Empathetic Analyzer")
st.markdown("*AI-powered debt collection simulation*")
st.markdown("---")

col1, col2 = st.columns([1.3, 1], gap="large")

# --- Left Column: Chat ---
with col1:
    st.markdown("### 📞 Live Call")
    
    # Chat Container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.conversation:
            role = msg.role
            content = msg.content
            if role == "agent":
                st.markdown(f'<div class="chat-bubble agent-msg"><strong>🤖 Riverline Agent:</strong> {content}</div>', unsafe_allow_html=True)
            elif role == "borrower":
                st.markdown(f'<div class="chat-bubble user-msg"><strong>👤 Borrower:</strong> {content}</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Input Area with Callback (Enter Key Works Instantly)
    st.text_input(
        "Message", 
        placeholder="Type here and press Enter...", 
        label_visibility="collapsed", 
        key="u_in",
        on_change=handle_input
    )
    
    # Quick Actions (Instant)
    st.markdown("**Quick Messages:**")
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("😟 Job Loss"): load_quick_reply("I lost my job recently and cannot pay.")
    if q2.button("🏥 Medical"): load_quick_reply("I have a medical emergency.")
    if q3.button("😠 Refusal"): load_quick_reply("Stop calling me, I will not pay!")
    if q4.button("🤔 Constraint"): load_quick_reply("I have financial constraints right now.")


# --- Right Column: Analysis ---
with col2:
    st.markdown("### 🧠 Real-Time Analysis")
    
    if st.session_state.conversation:
        borrower_msgs = [{"role": m.role, "content": m.content} for m in st.session_state.conversation if m.role == "borrower"]
        if borrower_msgs:
            last_msg = borrower_msgs[-1]["content"]
            
            # Run Analysis
            sentiment = analyzer.analyze_sentiment(last_msg)
            intent, score, expl = analyzer.classify_intent(borrower_msgs)
            strat = analyzer.recommend_strategy(intent, sentiment)
            
            # --- Sentiment Card ---
            st.markdown("#### 💬 Sentiment")
            sent_label = sentiment['label']
            sent_score = sentiment['score']
            if sent_label == "POSITIVE": c = "#43A047"; i = "😊"
            elif sent_label == "NEGATIVE": c = "#E53935"; i = "😟"
            else: c = "#9E9E9E"; i = "😐"
            
            st.markdown(f"""
                <div class="metric-card" style="border-left: 5px solid {c}; padding: 15px;">
                    <h3 style="margin:0;">{i} {sent_label}</h3>
                    <p style="margin:0; font-size:0.9rem;">Confidence: {sent_score:.0%}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- Intent Card ---
            st.markdown("#### 📊 Detected Intent")
            st.info(f"**{intent}**\n\n{expl}")
            
            # --- Strategy Card ---
            st.markdown("#### 💡 Recommended Strategy")
            st.success(f"**{strat['Action']}**")
            st.markdown(f"_{strat['Script']}_")
            
            with st.expander("📚 Economic Rationale", expanded=True):
                st.markdown(f"**Principle:** {strat['Economic Principle']}")
                st.markdown(f"**Tone:** {strat['Tone']}")
    else:
        st.markdown("""
            <div class="metric-card" style="text-align: center; padding: 40px;">
                <h3>👆 Start a Call</h3>
                <p>Select a scenario to begin.</p>
            </div>
        """, unsafe_allow_html=True)
