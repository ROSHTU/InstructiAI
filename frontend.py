import streamlit as st
import requests
import time
import json
from datetime import datetime

# Page configuration with custom theme
st.set_page_config(
    page_title="InstructiAI - Advanced AI Agent Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom Header */
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: slideDown 0.8s ease-out;
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* Card Styles */
    .agent-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .model-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        animation: pulse 2s infinite;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Styles */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Response Card */
    .response-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Animations */
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Loading Animation */
    .loading-dots {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
    }
    
    .loading-dots div {
        position: absolute;
        top: 33px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #667eea;
        animation-timing-function: cubic-bezier(0, 1, 1, 0);
    }
    
    .loading-dots div:nth-child(1) {
        left: 8px;
        animation: loading1 0.6s infinite;
    }
    
    .loading-dots div:nth-child(2) {
        left: 8px;
        animation: loading2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(3) {
        left: 32px;
        animation: loading2 0.6s infinite;
    }
    
    .loading-dots div:nth-child(4) {
        left: 56px;
        animation: loading3 0.6s infinite;
    }
    
    @keyframes loading1 {
        0% { transform: scale(0); }
        100% { transform: scale(1); }
    }
    
    @keyframes loading3 {
        0% { transform: scale(1); }
        100% { transform: scale(0); }
    }
    
    @keyframes loading2 {
        0% { transform: translate(0, 0); }
        100% { transform: translate(24px, 0); }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #d63384;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="custom-header">
    <div class="header-title">🤖 InstructiAI</div>
    <div class="header-subtitle">Advanced AI Agent Platform - Create, Configure & Interact</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🔧 Agent Configuration")
    
    # Model Provider Selection
    st.markdown("#### 🏢 Model Provider")
    provider = st.radio(
        "Choose your AI provider:",
        ("Groq", "OpenAI"),
        help="Select the AI model provider for your agent"
    )
    
    # Model Selection
    MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
    MODEL_NAMES_OPENAI = ["gpt-4o-mini"]
    
    st.markdown("#### 🧠 Model Selection")
    if provider == "Groq":
        selected_model = st.selectbox(
            "Select Groq Model:",
            MODEL_NAMES_GROQ,
            help="Choose the specific Groq model for your agent"
        )
        model_info = "⚡ High-performance open-source models"
    else:
        selected_model = st.selectbox(
            "Select OpenAI Model:",
            MODEL_NAMES_OPENAI,
            help="Choose the specific OpenAI model for your agent"
        )
        model_info = "🎯 Advanced GPT models from OpenAI"
    
    st.info(model_info)
    
    # Web Search Toggle
    st.markdown("#### 🌐 Web Search")
    allow_web_search = st.toggle(
        "Enable Web Search",
        help="Allow the agent to search the web for real-time information"
    )
    
    if allow_web_search:
        st.success("🔍 Web search enabled - Your agent can access real-time information!")
    else:
        st.info("📚 Using model knowledge only")
    
    # Chat History
    st.markdown("#### 📊 Session Stats")
    st.metric("Total Interactions", len(st.session_state.chat_history))
    
    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.rerun()

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    # Agent Configuration Card
    st.markdown("""
    <div class="agent-card">
        <h3>🎯 Define Your AI Agent</h3>
        <p>Create a specialized AI agent by defining its personality, expertise, and behavior.</p>
    </div>
    """, unsafe_allow_html=True)
    
    system_prompt = st.text_area(
        "System Prompt:",
        height=120,
        placeholder="Define your AI agent's role, personality, and expertise...\n\nExample: You are a helpful coding assistant specialized in Python. You provide clear, concise solutions with best practices.",
        help="This prompt defines your agent's behavior and expertise"
    )
    
    # Query Input
    st.markdown("### 💬 Chat with Your Agent")
    user_query = st.text_area(
        "Your Message:",
        height=150,
        placeholder="Ask your AI agent anything...\n\nExample: Explain quantum computing in simple terms, or help me debug this Python code.",
        help="Enter your question or request for the AI agent"
    )

with col2:
    # Model Info Card
    st.markdown(f"""
    <div class="model-card">
        <h4>🤖 Current Setup</h4>
        <p><strong>Provider:</strong> {provider}</p>
        <p><strong>Model:</strong> {selected_model}</p>
        <p><strong>Web Search:</strong> {'✅ Enabled' if allow_web_search else '❌ Disabled'}</p>
        <p><strong>Status:</strong> Ready</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Templates
    st.markdown("### 🚀 Quick Templates")
    template_options = {
        "Code Assistant": "You are an expert programming assistant. Help users with coding problems, debugging, and best practices. Provide clear, well-commented code examples.",
        "Creative Writer": "You are a creative writing assistant. Help users with storytelling, character development, and creative content creation.",
        "Data Analyst": "You are a data analysis expert. Help users understand data, create visualizations, and derive insights from datasets.",
        "Tutor": "You are a patient and knowledgeable tutor. Explain complex topics in simple terms and provide step-by-step guidance."
    }
    
    selected_template = st.selectbox("Choose a template:", ["Custom"] + list(template_options.keys()))
    
    if selected_template != "Custom" and st.button("📋 Apply Template"):
        st.session_state.template_prompt = template_options[selected_template]
        st.rerun()
    
    if 'template_prompt' in st.session_state:
        system_prompt = st.session_state.template_prompt

# Action Button
st.markdown("### 🚀 Launch Agent")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    ask_button = st.button(
        "🤖 Ask Agent!",
        use_container_width=True,
        type="primary"
    )

# API Configuration
API_URL = "http://127.0.0.1:9999/chat"

# Handle Button Click
if ask_button:
    if not user_query.strip():
        st.error("⚠️ Please enter a query to proceed!")
    else:
        # Create loading animation
        with st.spinner('🤖 Your AI agent is thinking...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            try:
                # Prepare payload
                payload = {
                    "model_name": selected_model,
                    "model_provider": provider,
                    "system_prompt": system_prompt,
                    "messages": [user_query],
                    "allow_search": allow_web_search
                }
                
                # Make API request
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    if "error" in response_data:
                        st.markdown(f"""
                        <div class="error-message">
                            <strong>❌ Error:</strong> {response_data['error']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Display success response
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        st.markdown(f"""
                        <div class="response-card">
                            <h3>🤖 Agent Response</h3>
                            <p><strong>Time:</strong> {timestamp}</p>
                            <p><strong>Model:</strong> {provider} - {selected_model}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display the response
                        st.markdown("### 💬 Response:")
                        st.markdown(f"**{response_data}**")
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "timestamp": timestamp,
                            "query": user_query,
                            "response": response_data,
                            "model": f"{provider} - {selected_model}",
                            "web_search": allow_web_search
                        })
                        
                        # Success notification
                        st.success("✅ Response generated successfully!")
                        
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        <strong>❌ API Error:</strong> Status code {response.status_code}
                    </div>
                    """, unsafe_allow_html=True)
                    
            except requests.exceptions.RequestException as e:
                st.markdown(f"""
                <div class="error-message">
                    <strong>❌ Connection Error:</strong> Unable to connect to the API server.<br>
                    <small>Make sure your backend server is running on http://127.0.0.1:9999</small>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    <strong>❌ Unexpected Error:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)

# Chat History Section
if st.session_state.chat_history:
    st.markdown("### 📜 Chat History")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"💬 Chat {len(st.session_state.chat_history) - i} - {chat['timestamp']}"):
            st.markdown(f"**🔤 Query:** {chat['query']}")
            st.markdown(f"**🤖 Response:** {chat['response']}")
            st.markdown(f"**⚙️ Model:** {chat['model']}")
            st.markdown(f"**🌐 Web Search:** {'✅ Enabled' if chat['web_search'] else '❌ Disabled'}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🤖 <strong>InstructiAI</strong> - Advanced AI Agent Platform</p>
    <p>Built with ❤️ using Streamlit | Powered by AI</p>
</div>
""", unsafe_allow_html=True)
