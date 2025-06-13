import streamlit as st
import os
import json
from agent import build_agent
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🏀 NBA Agent Chat",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: rgba(255, 255, 255, 0.1);
        border-left: 4px solid #ffd700;
    }
    .chat-message.bot {
        background-color: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #ff6b35;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .chat-message .message {
        flex: 1;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: rgba(255, 255, 255, 0.1);
    }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffd700;
    }
    .stButton > button {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    with st.spinner("🏀 Loading NBA Agent..."):
        st.session_state.agent = build_agent()

# Sidebar
with st.sidebar:
    st.title("🏀 NBA Agent")
    st.markdown("---")
    
    st.markdown("### 📊 What I Can Help With:")
    st.markdown("""
    - **Player Stats** 📈
      - Points, Assists, Rebounds
      - Steals, Blocks, All Stats
    
    - **Team Schedules** 📅
      - Next games, Upcoming matches
    
    - **Season Analysis** 🏆
      - Compare players
      - Find leaders in categories
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Example Questions:")
    example_questions = [
        "How many assists did Tyler Herro have this season?",
        "What are all of LeBron's stats?",
        "When do the Warriors play next?",
        "Who had the most rebounds this season?",
        "Show me Giannis stats for 2024-25"
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(f"💬 {question}", key=f"example_{i}"):
            st.session_state.example_question = question
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📈 Chat Stats")
    st.metric("Messages", len(st.session_state.messages))
    if st.session_state.messages:
        last_message_time = st.session_state.messages[-1].get("timestamp", "Unknown")
        st.metric("Last Activity", last_message_time)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("🏀 NBA Agent Chat")
st.markdown("Ask me anything about NBA stats and schedules!")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <div class="avatar">🤔</div>
                    <div class="message">
                        <strong>You:</strong><br>
                        {message["content"]}
                        <br><small>{message.get("timestamp", "")}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                content = message["content"]
                try:
                    data = json.loads(content)
                except Exception:
                    data = None
                if isinstance(data, dict) and "stats" in data:
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="avatar">🏀</div>
                        <div class="message">
                            <strong>NBA Agent:</strong><br>
                            {data.get('player', '')} {data.get('season', '')} Stats
                            <br><small>{message.get('timestamp', '')}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.table(data["stats"])
                    st.bar_chart(data["stats"])
                elif isinstance(data, dict) and "wins" in data and "losses" in data:
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="avatar">🏀</div>
                        <div class="message">
                            <strong>NBA Agent:</strong><br>
                            {data['team']} - {data['wins']}W/{data['losses']}L (Rank {data.get('rank','')})
                            <br><small>{message.get('timestamp','')}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot">
                        <div class="avatar">🏀</div>
                        <div class="message">
                            <strong>NBA Agent:</strong><br>
                            {content}
                            <br><small>{message.get("timestamp", "")}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
st.markdown("---")
col1, col2 = st.columns([8, 1])

with col1:
    # Check if there's an example question to use
    default_value = ""
    if "example_question" in st.session_state:
        default_value = st.session_state.example_question
        del st.session_state.example_question
    
    user_input = st.text_input(
        "Ask your NBA question:",
        placeholder="e.g., How many assists did Luka have this season?",
        key="user_input",
        value=default_value
    )

with col2:
    send_button = st.button("🚀 Send", type="primary")

# Process user input
if (send_button and user_input) or (user_input and st.session_state.get("enter_pressed")):
    # Add user message
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Get bot response
    with st.spinner("🤖 NBA Agent is thinking..."):
        try:
            response = st.session_state.agent.invoke({"input": user_input})
            bot_response = response.get("output", str(response))
        except Exception as e:
            bot_response = f"Sorry, I encountered an error: {str(e)}"
    
    # Add bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response,
        "timestamp": timestamp
    })
    
    # Clear input and rerun
    st.rerun()

# Handle Enter key press
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
        window.parent.postMessage({type: 'enter_pressed'}, '*');
    }
});
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.7); padding: 1rem;">
    🏀 NBA Agent • Powered by OpenAI & LangChain • Built with Streamlit
</div>
""", unsafe_allow_html=True)

# Auto-scroll to bottom
if st.session_state.messages:
    st.markdown("""
    <script>
    setTimeout(function() {
        window.scrollTo(0, document.body.scrollHeight);
    }, 100);
    </script>
    """, unsafe_allow_html=True) 