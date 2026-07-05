import streamlit as st
import requests
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configure page settings
st.set_page_config(
    page_title="AI Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint URL
API_URL = "http://127.0.0.1:8000"

# Inject beautiful CSS for custom styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Custom header container */
.header-container {
    background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
    padding: 2.2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.header-title {
    color: #ffffff !important;
    font-weight: 700;
    font-size: 2.6rem;
    margin: 0;
    letter-spacing: -0.5px;
}

.header-subtitle {
    color: #c084fc !important;
    font-size: 1.15rem;
    margin-top: 0.6rem;
    font-weight: 300;
    margin-bottom: 0;
}

/* Glassmorphism cards for suggestions */
.starter-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease-in-out;
}

.starter-card:hover {
    transform: translateY(-2px);
    border-color: rgba(192, 132, 252, 0.25);
    background: rgba(255, 255, 255, 0.04);
}

.starter-text {
    font-size: 1.1rem;
    color: #e2e8f0;
    line-height: 1.5;
    margin-bottom: 0.5rem;
    font-weight: 400;
}

/* Badge styles */
.badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.theme-badge {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white !important;
    padding: 0.35rem 0.95rem;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.fact-card {
    background: rgba(16, 185, 129, 0.03);
    border: 1px solid rgba(16, 185, 129, 0.15);
    border-radius: 12px;
    padding: 1.2rem;
    margin-top: 1rem;
}

.fact-title {
    color: #10b981 !important;
    font-weight: 600;
    font-size: 1.15rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🤝 Personalized Networking Assistant</h1>
    <p class="header-subtitle">Generate tailored conversation starters and verify networking topics using real-time AI.</p>
</div>
""", unsafe_allow_html=True)

# Check API Health
backend_online = True
try:
    health_resp = requests.get(f"{API_URL}/", timeout=2)
    if health_resp.status_code != 200:
        backend_online = False
except Exception:
    backend_online = False

if not backend_online:
    st.warning("⚠️ Backend server is currently offline or unreachable. Please start it using: `uvicorn app.main:app --reload`")

# Sidebar - User Profile Section
st.sidebar.markdown("### 👤 User Profile")
profile_name = st.sidebar.text_input("Name", value="Jane Doe")
profile_profession = st.sidebar.text_input("Profession", value="Product Manager")
profile_company = st.sidebar.text_input("Company", value="TechNova Solutions")
profile_bio = st.sidebar.text_area("Short Bio", value="Passionate about building scalable AI products and collaborative ecosystems.")
profile_skills_str = st.sidebar.text_input("Skills (comma-separated)", value="Product Strategy, Agile, AI Product Management, UX Design")
profile_interests_str = st.sidebar.text_input("Interests (comma-separated)", value="Generative AI, Sustainable Tech, Venture Capital")
profile_experience = st.sidebar.selectbox("Experience Level", ["Entry-Level", "Mid-Level", "Senior", "Director / Lead", "Executive"], index=2)
profile_goals = st.sidebar.text_area("Networking Goals", value="Connect with software engineers in AI space and meet potential co-founders.")

# Parse lists
profile_skills = [s.strip() for s in profile_skills_str.split(",") if s.strip()]
profile_interests = [i.strip() for i in profile_interests_str.split(",") if i.strip()]

# Sidebar - Event Context Section
st.sidebar.markdown("### 📅 Event Context")
event_name = st.sidebar.text_input("Event Name", value="Global AI Innovators Summit")
event_type = st.sidebar.selectbox("Event Type", ["Conference", "Meetup", "Panel", "Workshop", "Hackathon", "Networking Dinner"], index=0)
event_themes_str = st.sidebar.text_input("Known Themes (optional, comma-separated)", value="")
event_description = st.sidebar.text_area("Event Description", value="A premier gathering of AI researchers, developers, product managers, and founders looking to showcase the latest breakthroughs in machine learning and discuss ethics in technology.")

event_themes = [t.strip() for t in event_themes_str.split(",") if t.strip()] if event_themes_str else None

# Main Layout: 2 Columns
col1, col2 = st.columns([7, 5])

with col1:
    st.markdown("### ✨ Generate Conversation Starters")
    
    # Generate Button
    generate_disabled = not backend_online
    if st.button("🚀 Generate Tailored Conversation Starters", disabled=generate_disabled, use_container_width=True):
        payload = {
            "user_profile": {
                "name": profile_name,
                "bio": profile_bio,
                "skills": profile_skills,
                "interests": profile_interests,
                "profession": profile_profession,
                "company": profile_company,
                "experience": profile_experience,
                "goals": profile_goals
            },
            "event_context": {
                "event_name": event_name,
                "event_description": event_description,
                "event_themes": event_themes,
                "event_type": event_type
            }
        }
        
        with st.spinner("Analyzing themes and generating starters..."):
            try:
                response = requests.post(f"{API_URL}/generate-conversation", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["themes"] = data.get("themes", [])
                    st.session_state["starters"] = data.get("starters", [])
                    st.success("Conversation starters generated successfully!")
                else:
                    st.error(f"Error {response.status_code}: Failed to generate conversation.")
            except Exception as e:
                st.error(f"Connection error: {e}")

    # Display results
    if "starters" in st.session_state:
        st.write("#### 🏷️ Extracted Event Themes")
        themes = st.session_state.get("themes", [])
        if themes:
            badge_html = "".join([f'<span class="theme-badge">{t}</span>' for t in themes])
            st.markdown(f'<div class="badge-container">{badge_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No themes extracted.")

        st.write("#### 💬 Conversation Starters")
        for idx, starter in enumerate(st.session_state["starters"]):
            # Display starter in card style
            st.markdown(f"""
            <div class="starter-card">
                <div class="starter-text">"{starter}"</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Rating buttons
            btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1, 2, 4])
            with btn_col1:
                if st.button(f"👍 Like", key=f"like_{idx}"):
                    try:
                        feedback_payload = {"suggestion": starter, "feedback": "like"}
                        requests.post(f"{API_URL}/feedback", json=feedback_payload)
                        st.toast("Feedback recorded: Like!", icon="👍")
                    except Exception as e:
                        st.error("Failed to submit feedback.")
            with btn_col2:
                if st.button(f"👎 Dislike", key=f"dislike_{idx}"):
                    try:
                        feedback_payload = {"suggestion": starter, "feedback": "dislike"}
                        requests.post(f"{API_URL}/feedback", json=feedback_payload)
                        st.toast("Feedback recorded: Dislike", icon="👎")
                    except Exception as e:
                        st.error("Failed to submit feedback.")
            with btn_col3:
                # Optional feedback text input
                suggestion_comment = st.text_input("Suggestion...", key=f"comment_{idx}", placeholder="Suggest edits...", label_visibility="collapsed")
                if suggestion_comment:
                    if st.button("Submit Edit", key=f"sub_comment_{idx}"):
                        try:
                            feedback_payload = {
                                "suggestion": starter, 
                                "feedback": "suggestion", 
                                "comment": suggestion_comment
                            }
                            requests.post(f"{API_URL}/feedback", json=feedback_payload)
                            st.toast("Suggestion recorded!", icon="✅")
                        except Exception as e:
                            st.error("Failed to submit feedback.")
            st.markdown("---")

with col2:
    # Tab layout for Fact Checker and History/Feedback view
    tab1, tab2, tab3 = st.tabs(["🔍 Fact Checker", "📜 Session History", "💬 Feedback Logs"])
    
    with tab1:
        st.markdown("### Verify Networking Topics")
        st.write("Instantly look up complex networking technologies, frameworks, or business concepts.")
        
        fact_query = st.text_input("Enter topic to verify:", placeholder="e.g., Transformers in NLP, Blockchain smart contracts")
        if st.button("Fact Check Topic", disabled=generate_disabled):
            if fact_query:
                with st.spinner("Checking Wikipedia..."):
                    try:
                        resp = requests.post(f"{API_URL}/fact-check", json={"query": fact_query})
                        if resp.status_code == 200:
                            fact_data = resp.json()
                            status_emoji = "✅" if "Verified" in fact_data["status"] else "⚠️"
                            
                            st.markdown(f"""
                            <div class="fact-card">
                                <div class="fact-title">{status_emoji} {fact_data['topic']} ({fact_data['status']})</div>
                                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.4;">{fact_data['summary']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if fact_data["wikipedia_url"]:
                                st.markdown(f"[Read full Wikipedia article]({fact_data['wikipedia_url']})")
                        else:
                            st.error("Failed to fetch verification.")
                    except Exception as e:
                        st.error(f"Error connecting to fact checker API: {e}")
            else:
                st.warning("Please enter a valid query.")
                
    with tab2:
        st.markdown("### Generated Session Logs")
        if st.button("🔄 Refresh History", disabled=generate_disabled):
            pass  # Trigger rerun
            
        try:
            hist_resp = requests.get(f"{API_URL}/history")
            if hist_resp.status_code == 200:
                history_data = hist_resp.json()
                if not history_data:
                    st.info("No session logs found.")
                else:
                    # Show latest first
                    for session in reversed(history_data):
                        timestamp = datetime.fromisoformat(session["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                        user_info = session.get("user", {})
                        
                        with st.expander(f"🕒 {timestamp} | Event: {session['user'].get('goals', 'Goal')[:30]}..."):
                            st.markdown(f"**Attendee:** {user_info.get('name')} ({user_info.get('profession')} at {user_info.get('company')})")
                            st.markdown(f"**Themes:** {', '.join(session.get('themes', []))}")
                            st.markdown("**Conversation Starters:**")
                            for starter in session.get("starters", []):
                                st.write(f"- *\"{starter}\"*")
            else:
                st.error("Could not fetch history.")
        except Exception:
            st.info("Start backend to view history logs.")
            
    with tab3:
        st.markdown("### User Feedback History")
        if st.button("🔄 Refresh Feedbacks", disabled=generate_disabled):
            pass  # Trigger rerun
            
        try:
            fb_resp = requests.get(f"{API_URL}/feedback")
            if fb_resp.status_code == 200:
                fb_data = fb_resp.json()
                if not fb_data:
                    st.info("No feedback entries submitted yet.")
                else:
                    for fb in reversed(fb_data):
                        timestamp = datetime.fromisoformat(fb["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                        feedback_type = fb.get("feedback", "").upper()
                        color = "#10b981" if feedback_type == "LIKE" else "#ef4444" if feedback_type == "DISLIKE" else "#3b82f6"
                        
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.01); border-left: 4px solid {color}; padding: 0.8rem; margin-bottom: 0.8rem; border-radius: 4px;">
                            <span style="color: {color}; font-weight: bold; font-size: 0.85rem;">{feedback_type}</span>
                            <span style="color: #64748b; font-size: 0.8rem; float: right;">{timestamp}</span>
                            <p style="margin: 0.4rem 0 0 0; font-size: 0.95rem; color: #e2e8f0;">"{fb.get('suggestion')}"</p>
                            {f'<p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #94a3b8; font-style: italic;">Comment: "{fb.get("comment")}"</p>' if fb.get("comment") else ''}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Could not fetch feedback.")
        except Exception:
            st.info("Start backend to view feedback logs.")
