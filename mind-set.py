import streamlit as st
import datetime
import pandas as pd
import random
from PIL import Image
import base64
import json
import os

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': '',
        'start_date': datetime.date.today(),
        'current_streak': 0,
        'longest_streak': 0,
        'last_login': None,
        'completed_challenges': [],
        'reflection_entries': []
    }

# Challenge database
challenges = {
    'beginner': [
        {"id": 1, "title": "Fixed to Growth", "description": "Identify one fixed mindset thought today and reframe it as growth mindset.", "duration": 1, "category": "awareness"},
        {"id": 2, "title": "The Power of Yet", "description": "Add 'yet' to three statements about things you can't do.", "duration": 1, "category": "language"},
        {"id": 3, "title": "Challenge Comfort", "description": "Do one thing outside your comfort zone today.", "duration": 1, "category": "action"},
        {"id": 4, "title": "Mistake Reflection", "description": "Reflect on a recent mistake and what you learned from it.", "duration": 1, "category": "reflection"},
        {"id": 5, "title": "Process Praise", "description": "Give genuine process-based praise to someone today.", "duration": 1, "category": "relationships"}
    ],
    'intermediate': [
        {"id": 6, "title": "Weekly Learning Goal", "description": "Set one learning goal for the week and plan how to achieve it.", "duration": 7, "category": "planning"},
        {"id": 7, "title": "Feedback Seeker", "description": "Ask for constructive feedback from someone this week.", "duration": 7, "category": "courage"},
        {"id": 8, "title": "Skill Builder", "description": "Dedicate 30 minutes daily to developing a new skill.", "duration": 7, "category": "practice"},
        {"id": 9, "title": "Obstacle Mapping", "description": "Identify potential obstacles for a goal and plan solutions.", "duration": 7, "category": "problem-solving"},
        {"id": 10, "title": "Growth Story", "description": "Journal about a time you grew through challenge.", "duration": 7, "category": "reflection"}
    ],
    'advanced': [
        {"id": 11, "title": "Month of Growth", "description": "Set and track progress on a meaningful 30-day growth goal.", "duration": 30, "category": "commitment"},
        {"id": 12, "title": "Challenge Network", "description": "Build a network of people who challenge you to grow.", "duration": 30, "category": "relationships"},
        {"id": 13, "title": "Deep Practice", "description": "Engage in deliberate practice for 1 hour daily on a skill.", "duration": 30, "category": "mastery"},
        {"id": 14, "title": "Fear Facing", "description": "Identify and take action on one significant fear each week.", "duration": 30, "category": "courage"},
        {"id": 15, "title": "Legacy Project", "description": "Create something that represents your growth journey.", "duration": 30, "category": "creation"}
    ]
}

# Growth mindset quotes
quotes = [
    {"quote": "The view you adopt for yourself profoundly affects the way you lead your life.", "author": "Carol Dweck"},
    {"quote": "Becoming is better than being.", "author": "Carol Dweck"},
    {"quote": "No matter what your ability is, effort is what ignites that ability and turns it into accomplishment.", "author": "Carol Dweck"},
    {"quote": "Challenge is the path to growth.", "author": "Unknown"},
    {"quote": "Mistakes are proof that you are trying.", "author": "Unknown"},
    {"quote": "Your brain is like a muscle - the more you use it, the stronger it gets.", "author": "Unknown"},
    {"quote": "I haven't failed. I've just found 10,000 ways that won't work.", "author": "Thomas Edison"},
    {"quote": "It's not that I'm so smart, it's just that I stay with problems longer.", "author": "Albert Einstein"}
]

# Helper functions
def update_streak():
    today = datetime.date.today()
    last_login = st.session_state.user_data['last_login']
    
    if last_login:
        delta = today - last_login
        if delta.days == 1:  # Consecutive day
            st.session_state.user_data['current_streak'] += 1
            if st.session_state.user_data['current_streak'] > st.session_state.user_data['longest_streak']:
                st.session_state.user_data['longest_streak'] = st.session_state.user_data['current_streak']
        elif delta.days > 1:  # Broken streak
            st.session_state.user_data['current_streak'] = 1
    else:  # First login
        st.session_state.user_data['current_streak'] = 1
    
    st.session_state.user_data['last_login'] = today

def get_random_quote():
    return random.choice(quotes)

def save_reflection(entry):
    st.session_state.user_data['reflection_entries'].append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "entry": entry
    })

def complete_challenge(challenge_id):
    challenge = next((c for level in challenges.values() for c in level if c['id'] == challenge_id), None)
    if challenge:
        st.session_state.user_data['completed_challenges'].append({
            "id": challenge['id'],
            "title": challenge['title'],
            "completed_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "reflection": ""
        })

def main():
    st.set_page_config(
        page_title="Growth Mindset Challenge",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextArea>div>div>textarea {
            min-height: 150px;
        }
        .challenge-card {
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🌱 Growth Mindset Challenge")
    st.markdown("Develop resilience, embrace challenges, and unlock your potential with daily growth mindset exercises.")
    
    # Sidebar
    with st.sidebar:
        st.header("Your Progress")
        
        if st.session_state.user_data['name']:
            st.subheader(f"Hello, {st.session_state.user_data['name']}!")
        
        st.metric("Current Streak", f"{st.session_state.user_data['current_streak']} days")
        st.metric("Longest Streak", f"{st.session_state.user_data['longest_streak']} days")
        
        completed_count = len(st.session_state.user_data['completed_challenges'])
        st.metric("Challenges Completed", completed_count)
        
        st.progress(min(completed_count / 15, 1.0))  # Progress through all challenges
        
        # Random quote
        quote = get_random_quote()
        st.markdown(f"*\"{quote['quote']}\"*  \n—{quote['author']}")
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🎯 Challenges", "📝 Reflections", "📊 Progress"])
    
    with tab1:  # Home
        if not st.session_state.user_data['name']:
            with st.form("user_form"):
                name = st.text_input("What's your name?")
                start_date = st.date_input("Start date", datetime.date.today())
                
                if st.form_submit_button("Start Growing!"):
                    st.session_state.user_data['name'] = name
                    st.session_state.user_data['start_date'] = start_date
                    update_streak()
                    st.rerun()
        else:
            update_streak()
            
            st.subheader("Welcome to Your Growth Journey")
            st.write("""
            **Growth mindset** is the belief that your abilities can be developed through dedication and hard work. 
            This app will guide you through challenges designed to help you:
            - Embrace challenges
            - Persist in the face of setbacks
            - See effort as the path to mastery
            - Learn from criticism
            - Find lessons and inspiration in the success of others
            """)
            
            st.image("https://images.unsplash.com/photo-1493612276216-ee3925520721?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80", 
                    caption="Growth requires both sunlight and storms")
            
            if st.session_state.user_data['completed_challenges']:
                st.subheader("Recently Completed")
                recent = st.session_state.user_data['completed_challenges'][-3:]
                for challenge in reversed(recent):
                    st.markdown(f"""
                    <div class="challenge-card">
                        <h4>{challenge['title']}</h4>
                        <p>Completed on {challenge['completed_date']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab2:  # Challenges
        st.subheader("Choose Your Challenge")
        level = st.radio("Select difficulty level:", ["Beginner", "Intermediate", "Advanced"], horizontal=True)
        
        level_key = level.lower()
        cols = st.columns(2)
        
        for i, challenge in enumerate(challenges[level_key]):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class="challenge-card">
                        <h4>{challenge['title']}</h4>
                        <p><small>{challenge['duration']} day{'s' if challenge['duration'] > 1 else ''} challenge</small></p>
                        <p>{challenge['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Start Challenge", key=f"start_{challenge['id']}"):
                        complete_challenge(challenge['id'])
                        st.success(f"You've started the {challenge['title']} challenge!")
                        st.session_state.active_challenge = challenge
                        st.rerun()
        
        if st.session_state.user_data['completed_challenges']:
            st.subheader("Your Completed Challenges")
            for challenge in st.session_state.user_data['completed_challenges']:
                st.markdown(f"""
                <div class="challenge-card">
                    <h4>{challenge['title']}</h4>
                    <p>Completed on {challenge['completed_date']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:  # Reflections
        st.subheader("Growth Reflections")
        st.write("""
        Reflection is a key part of developing a growth mindset. 
        Take time to journal about your challenges, what you've learned, and how you've grown.
        """)
        
        with st.form("reflection_form"):
            reflection = st.text_area("Write your reflection here:")
            if st.form_submit_button("Save Reflection"):
                save_reflection(reflection)
                st.success("Reflection saved!")
        
        if st.session_state.user_data['reflection_entries']:
            st.subheader("Your Reflection Journal")
            for entry in reversed(st.session_state.user_data['reflection_entries']):
                with st.expander(f"Entry from {entry['date']}"):
                    st.write(entry['entry'])
    
    with tab4:  # Progress
        st.subheader("Your Growth Progress")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Days Since Starting", (datetime.date.today() - st.session_state.user_data['start_date']).days)
            st.metric("Current Streak", f"{st.session_state.user_data['current_streak']} days")
        
        with col2:
            st.metric("Longest Streak", f"{st.session_state.user_data['longest_streak']} days")
            st.metric("Challenges Completed", len(st.session_state.user_data['completed_challenges']))
        
        # Challenge completion chart
        if st.session_state.user_data['completed_challenges']:
            st.subheader("Challenge Completion")
            df = pd.DataFrame(st.session_state.user_data['completed_challenges'])
            df['completed_date'] = pd.to_datetime(df['completed_date'])
            df = df.set_index('completed_date')
            st.line_chart(df.resample('W').count()['title'])
        
        # Export data
        st.subheader("Export Your Data")
        if st.button("Export Growth Journal"):
            json_data = json.dumps(st.session_state.user_data, indent=2)
            b64 = base64.b64encode(json_data.encode()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="growth_journal.json">Download JSON</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()