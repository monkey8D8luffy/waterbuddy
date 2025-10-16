"""
WaterBuddy - Age-Adaptive Hydration Tracking App
Fixed navigation and optimized for Streamlit
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta, date
import json
import os

# Page configuration
st.set_page_config(
    page_title="WaterBuddy - Hydration Companion",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DATA MODELS & CONSTANTS
# ============================================================================

AGE_GROUPS = {
    'children': {'label': 'Kids (2-12)', 'icon': '🌈', 'min': 2, 'max': 12},
    'teen': {'label': 'Teens (13-18)', 'icon': '🚀', 'min': 13, 'max': 18},
    'adult': {'label': 'Adults (19-64)', 'icon': '💼', 'min': 19, 'max': 64},
    'senior': {'label': 'Seniors (65+)', 'icon': '🌸', 'min': 65, 'max': 120}
}

BADGES = {
    'first-glass': {'emoji': '🌟', 'title': 'First Splash', 'description': 'Logged your first glass!'},
    'daily-goal': {'emoji': '🎯', 'title': 'Daily Champion', 'description': 'Reached daily goal!'},
    'week-streak': {'emoji': '🔥', 'title': 'Week Warrior', 'description': '7 day streak!'},
    'month-streak': {'emoji': '🏆', 'title': 'Monthly Master', 'description': '30 day streak!'},
    'hydration-hero': {'emoji': '💪', 'title': 'Hydration Hero', 'description': '100 glasses logged!'},
    'early-bird': {'emoji': '🌅', 'title': 'Early Bird', 'description': 'Morning hydration!'},
    'night-owl': {'emoji': '🦉', 'title': 'Night Owl', 'description': 'Evening hydration!'},
    'consistent': {'emoji': '⚡', 'title': 'Consistency King', 'description': '10 days in a row!'},
    'overachiever': {'emoji': '🚀', 'title': 'Overachiever', 'description': '150% of goal!'},
}

AGE_THEME_COLORS = {
    'children': {'primary': '#FF6B9D', 'secondary': '#FFE66D', 'accent': '#4ECDC4', 'bg': '#FFF0F5'},
    'teen': {'primary': '#7C3AED', 'secondary': '#F59E0B', 'accent': '#EF4444', 'bg': '#F5F3FF'},
    'adult': {'primary': '#70D6FF', 'secondary': '#1E9BC7', 'accent': '#FFB3A7', 'bg': '#F0F9FF'},
    'senior': {'primary': '#1E9BC7', 'secondary': '#FFB3A7', 'accent': '#70D6FF', 'bg': '#FFF7ED'}
}

WATER_SIZES = [
    {'amount': 250, 'label': 'Glass', 'icon': '🥛'},
    {'amount': 330, 'label': 'Can', 'icon': '🥤'},
    {'amount': 500, 'label': 'Bottle', 'icon': '🍶'},
    {'amount': 750, 'label': 'Large', 'icon': '🚰'}
]

# ============================================================================
# STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    
    defaults = {
        # User profile
        'name': '',
        'age_group': 'adult',
        'daily_goal': 2000,
        'join_date': datetime.now(),
        'weight': 70,
        'activity_level': 'moderate',
        
        # Tracking data
        'current_intake': 0,
        'intake_history': [],
        'last_drink': None,
        
        # Gamification
        'streak': 0,
        'best_streak': 0,
        'badges': [],
        'total_intake': 0,
        'total_glasses': 0,
        
        # Settings
        'notifications_enabled': True,
        'notification_frequency': 60,
        'notification_tone': 'gentle',
        'sound_enabled': True,
        'high_contrast': False,
        'family_mode': False,
        'dark_mode': False,
        'language': 'English',
        'units': 'metric',
        
        # UI state - IMPORTANT: default screen
        'current_screen': 'splash',
        'show_onboarding': True,
        'today_date': date.today(),
        
        # Data
        'weekly_data': [],
        'leaderboard_users': [],
        'last_reminder_time': datetime.now(),
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Initialize name-dependent values
    if st.session_state.name:
        st.session_state.show_onboarding = False
        if st.session_state.current_screen == 'splash':
            st.session_state.current_screen = 'dashboard'
    
    # Load or generate data
    if not st.session_state.weekly_data:
        st.session_state.weekly_data = generate_weekly_data()
    
    if not st.session_state.leaderboard_users:
        st.session_state.leaderboard_users = load_leaderboard_data()

def load_leaderboard_data():
    """Load leaderboard data from CSV if exists"""
    try:
        if os.path.exists('data/leaderboard.csv'):
            df = pd.read_csv('data/leaderboard.csv')
            return df.head(10).to_dict('records')
    except:
        pass
    
    return [
        {'name': 'You', 'intake': 0, 'streak': 0},
        {'name': 'Alex', 'intake': 1800, 'streak': 5},
        {'name': 'Sarah', 'intake': 2200, 'streak': 8},
        {'name': 'Mike', 'intake': 1500, 'streak': 3}
    ]

def generate_weekly_data():
    """Generate weekly data"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    data = []
    for i, day in enumerate(days):
        intake = 1700 + (i * 100) if i < 6 else st.session_state.get('current_intake', 0)
        data.append({
            'day': day,
            'intake': intake,
            'goal': st.session_state.get('daily_goal', 2000)
        })
    return data

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_age_specific_message(message_type: str) -> str:
    """Get age-appropriate messages"""
    messages = {
        'children': {
            'greeting': "Hi there, water buddy! 💧",
            'encouragement': "You're doing amazing! Keep it up! 🌟",
            'goal_reached': "WOW! You're a water superhero! 🎉"
        },
        'teen': {
            'greeting': "Hey! Ready to level up? 🚀",
            'encouragement': "Crushing it! Don't break the streak! 🔥",
            'goal_reached': "Goal Crushed! 🔥 Streak game strong!"
        },
        'adult': {
            'greeting': "Good day! Let's stay hydrated 💼",
            'encouragement': "Great progress! Boosting your focus! 🎯",
            'goal_reached': "Goal Achieved! 🎯 Excellent work!"
        },
        'senior': {
            'greeting': "Hello! Time to stay refreshed 🌸",
            'encouragement': "Wonderful progress! Keep it up! 🌿",
            'goal_reached': "Well Done! 🌿 Goal completed!"
        }
    }
    
    age_group = st.session_state.age_group
    return messages[age_group].get(message_type, '')

def create_water_drop_image():
    """Create simple water drop image using HTML/CSS"""
    colors = AGE_THEME_COLORS[st.session_state.age_group]
    
    html = f"""
    <div style="text-align: center; padding: 1rem;">
        <div style="
            width: 100px;
            height: 120px;
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            margin: 20px auto;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            position: relative;
        ">
            <div style="
                position: absolute;
                top: 20px;
                left: 20px;
                width: 30px;
                height: 40px;
                background: rgba(255,255,255,0.5);
                border-radius: 50%;
            "></div>
        </div>
    </div>
    """
    return html

def create_bottle_progress_bar(percentage: float):
    """Create vertical progress bar in bottle shape"""
    colors = AGE_THEME_COLORS[st.session_state.age_group]
    fill_pct = max(0, min(100, percentage))
    
    html = f"""
    <div style="text-align: center; padding: 1rem;">
        <div style="position: relative; width: 80px; height: 250px; margin: 0 auto;">
            <!-- Bottle Cap -->
            <div style="
                width: 40px;
                height: 15px;
                background: {colors['secondary']};
                border: 2px solid {colors['primary']};
                border-radius: 8px 8px 0 0;
                margin: 0 auto;
                position: absolute;
                left: 20px;
                top: 0;
            "></div>
            
            <!-- Bottle Neck -->
            <div style="
                width: 30px;
                height: 25px;
                background: rgba(255,255,255,0.9);
                border: 3px solid {colors['primary']};
                margin: 0 auto;
                position: absolute;
                left: 25px;
                top: 15px;
            "></div>
            
            <!-- Bottle Body (Outline) -->
            <div style="
                width: 80px;
                height: 200px;
                background: rgba(255,255,255,0.9);
                border: 3px solid {colors['primary']};
                border-radius: 8px;
                position: absolute;
                top: 40px;
                left: 0;
                overflow: hidden;
            ">
                <!-- Water Fill (from bottom) -->
                <div style="
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    height: {fill_pct}%;
                    background: linear-gradient(180deg, {colors['primary']} 0%, {colors['secondary']} 100%);
                    transition: height 0.5s ease;
                "></div>
                
                <!-- Percentage Text -->
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 24px;
                    font-weight: bold;
                    color: {colors['primary']};
                    z-index: 10;
                ">{int(fill_pct)}%</div>
                
                <!-- Measurement Lines -->
                <div style="position: absolute; left: 0; top: 25%; width: 10px; height: 2px; background: #999;"></div>
                <div style="position: absolute; left: 0; top: 50%; width: 10px; height: 2px; background: #999;"></div>
                <div style="position: absolute; left: 0; top: 75%; width: 10px; height: 2px; background: #999;"></div>
            </div>
            
            <!-- Amount Label -->
            <div style="
                position: absolute;
                bottom: -30px;
                left: 0;
                width: 100%;
                text-align: center;
                font-size: 12px;
                color: #666;
            ">{st.session_state.current_intake}/{st.session_state.daily_goal}ml</div>
        </div>
    </div>
    """
    return html

def add_water_intake(amount: int):
    """Add water intake and check for achievements"""
    old_intake = st.session_state.current_intake
    new_intake = old_intake + amount
    
    st.session_state.current_intake = new_intake
    st.session_state.total_intake += amount
    st.session_state.total_glasses += 1
    st.session_state.last_drink = datetime.now()
    
    # Log to history
    st.session_state.intake_history.append({
        'timestamp': datetime.now(),
        'amount': amount,
        'date': date.today()
    })
    
    # Check for badges
    check_badges(new_intake, old_intake)
    
    # Update data
    st.session_state.weekly_data = generate_weekly_data()
    update_leaderboard()

def check_badges(new_intake, old_intake):
    """Check and award badges"""
    if 'first-glass' not in st.session_state.badges and st.session_state.total_glasses == 1:
        st.session_state.badges.append('first-glass')
        st.success(f"🌟 Badge Earned: First Splash!")
    
    if new_intake >= st.session_state.daily_goal and old_intake < st.session_state.daily_goal:
        if 'daily-goal' not in st.session_state.badges:
            st.session_state.badges.append('daily-goal')
        st.balloons()
        st.success(get_age_specific_message('goal_reached'))
    
    if st.session_state.total_glasses >= 100 and 'hydration-hero' not in st.session_state.badges:
        st.session_state.badges.append('hydration-hero')
        st.success(f"💪 Badge Earned: Hydration Hero!")
    
    current_hour = datetime.now().hour
    if 5 <= current_hour < 9 and 'early-bird' not in st.session_state.badges:
        st.session_state.badges.append('early-bird')
        st.success(f"🌅 Badge Earned: Early Bird!")
    
    if 20 <= current_hour < 24 and 'night-owl' not in st.session_state.badges:
        st.session_state.badges.append('night-owl')
        st.success(f"🦉 Badge Earned: Night Owl!")
    
    if new_intake >= st.session_state.daily_goal * 1.5 and 'overachiever' not in st.session_state.badges:
        st.session_state.badges.append('overachiever')
        st.success(f"🚀 Badge Earned: Overachiever!")

def update_leaderboard():
    """Update leaderboard with current user data"""
    if st.session_state.family_mode:
        for user in st.session_state.leaderboard_users:
            if user.get('name') in [st.session_state.name, 'You']:
                user['intake'] = st.session_state.current_intake
                user['streak'] = st.session_state.streak

def check_streak():
    """Check and update streak"""
    today = date.today()
    if st.session_state.today_date != today:
        if st.session_state.current_intake >= st.session_state.daily_goal:
            st.session_state.streak += 1
            if st.session_state.streak > st.session_state.best_streak:
                st.session_state.best_streak = st.session_state.streak
        else:
            st.session_state.streak = 0
        
        st.session_state.current_intake = 0
        st.session_state.today_date = today
        
        if st.session_state.streak >= 7 and 'week-streak' not in st.session_state.badges:
            st.session_state.badges.append('week-streak')
        if st.session_state.streak >= 10 and 'consistent' not in st.session_state.badges:
            st.session_state.badges.append('consistent')
        if st.session_state.streak >= 30 and 'month-streak' not in st.session_state.badges:
            st.session_state.badges.append('month-streak')

# ============================================================================
# STYLING
# ============================================================================

def apply_custom_css():
    """Apply custom CSS for Streamlit"""
    colors = AGE_THEME_COLORS[st.session_state.age_group]
    
    font_sizes = {
        'children': '18px',
        'teen': '16px',
        'adult': '16px',
        'senior': '20px'
    }
    
    base_font = font_sizes[st.session_state.age_group]
    bg_color = colors['bg'] if not st.session_state.dark_mode else '#1a1a1a'
    text_color = '#123743' if not st.session_state.dark_mode else '#ffffff'
    
    css = f"""
    <style>
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-size: {base_font};
    }}
    
    h1, h2, h3 {{
        color: {colors['primary']};
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: transform 0.2s;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05);
    }}
    
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }}
    
    .badge-item {{
        background: linear-gradient(135deg, {colors['primary']}22, {colors['secondary']}22);
        border: 2px solid {colors['primary']};
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }}
    
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {colors['secondary']}, {colors['primary']});
    }}
    
    [data-testid="stMetricValue"] {{
        color: {colors['primary']};
        font-size: 2rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# VISUALIZATION COMPONENTS
# ============================================================================

def create_weekly_chart():
    """Create weekly intake chart"""
    colors = AGE_THEME_COLORS[st.session_state.age_group]
    data = st.session_state.weekly_data
    
    days = [d['day'] for d in data]
    intakes = [d['intake'] for d in data]
    goals = [d['goal'] for d in data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days, y=goals, mode='lines', name='Goal',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    bar_colors = [colors['primary'] if i >= g else colors['secondary'] 
                  for i, g in zip(intakes, goals)]
    
    fig.add_trace(go.Bar(
        x=days, y=intakes, name='Intake',
        marker_color=bar_colors,
        text=[f"{i}ml" for i in intakes],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Weekly Progress",
        xaxis_title="Day",
        yaxis_title="Water (ml)",
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_progress_gauge(percentage: float):
    """Create gauge chart for progress"""
    colors = AGE_THEME_COLORS[st.session_state.age_group]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Daily Goal Progress", 'font': {'size': 20}},
        number={'suffix': '%'},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': colors['primary']},
            'steps': [
                {'range': [0, 50], 'color': colors['secondary'] + '33'},
                {'range': [50, 75], 'color': colors['primary'] + '33'},
                {'range': [75, 100], 'color': colors['accent'] + '33'}
            ],
            'threshold': {
                'line': {'color': colors['accent'], 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# ============================================================================
# SCREEN COMPONENTS
# ============================================================================

def splash_screen():
    """Display splash screen"""
    st.markdown("""
    <div style='text-align: center; padding: 3rem 1rem;'>
        <h1 style='font-size: 4rem; color: #70D6FF;'>💧 WaterBuddy</h1>
        <p style='font-size: 1.5rem; margin-top: 1rem;'>Your Personal Hydration Companion</p>
        <p style='margin-top: 2rem; opacity: 0.7;'>🔒 Privacy-first • No account needed</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started →", key="splash_start", use_container_width=True):
            st.session_state.current_screen = 'onboarding'
            st.rerun()

def onboarding_screen():
    """Onboarding flow"""
    st.markdown("<h1 style='text-align: center;'>💧 Let's Get Started!</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        name = st.text_input("What's your name?", value=st.session_state.name, 
                            placeholder="Enter your name...")
        
        st.markdown("### Choose your age group:")
        cols = st.columns(2)
        for idx, (key, value) in enumerate(AGE_GROUPS.items()):
            with cols[idx % 2]:
                selected = st.session_state.age_group == key
                if st.button(f"{value['icon']} {value['label']}", 
                           key=f"age_{key}",
                           use_container_width=True,
                           type="primary" if selected else "secondary"):
                    st.session_state.age_group = key
                    st.rerun()
        
        st.info(f"**Selected:** {AGE_GROUPS[st.session_state.age_group]['label']}")
        
        st.markdown("### Set your daily goal:")
        daily_goal = st.slider("Daily goal (ml)", 1000, 4000, 
                              st.session_state.daily_goal, 250)
        st.success(f"Goal: **{daily_goal}ml** ({daily_goal // 250} glasses)")
        
        family_mode = st.checkbox("Enable Family/Group mode", 
                                 value=st.session_state.family_mode)
        
        st.markdown("")
        if st.button("Start My Journey! 🚀", use_container_width=True):
            if name.strip():
                st.session_state.name = name
                st.session_state.daily_goal = daily_goal
                st.session_state.family_mode = family_mode
                st.session_state.current_screen = 'dashboard'
                st.session_state.show_onboarding = False
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter your name!")

def dashboard_screen():
    """Main dashboard"""
    check_streak()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(get_age_specific_message('greeting'))
        st.caption(f"👋 {st.session_state.name} • {datetime.now().strftime('%A, %B %d')}")
    
    with col2:
        drop_html = create_water_drop_image()
        st.markdown(drop_html, unsafe_allow_html=True)
    
    st.divider()
    
    # Progress section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💧 Today's Progress")
        progress_pct = (st.session_state.current_intake / st.session_state.daily_goal) * 100
        st.progress(min(progress_pct / 100, 1.0))
        
        st.markdown(f"""
        <h2 style='text-align: center; margin: 1rem 0;'>
            {st.session_state.current_intake}ml / {st.session_state.daily_goal}ml
        </h2>
        """, unsafe_allow_html=True)
        
        st.info(get_age_specific_message('encouragement'))
    
    with col2:
        bottle_progress = create_bottle_progress_bar(progress_pct)
        st.markdown(bottle_progress, unsafe_allow_html=True)
    
    st.divider()
    
    # Water intake buttons
    st.markdown("### 💧 Log Water Intake")
    cols = st.columns(4)
    for idx, water in enumerate(WATER_SIZES):
        with cols[idx]:
            if st.button(f"{water['icon']}\n\n**{water['label']}**\n\n{water['amount']}ml",
                        key=f"water_{water['amount']}", use_container_width=True):
                add_water_intake(water['amount'])
                st.rerun()
    
    # Custom amount
    with st.expander("➕ Custom Amount"):
        col1, col2 = st.columns([3, 1])
        with col1:
            custom = st.number_input("Amount (ml)", 1, 2000, 250, 50)
        with col2:
            st.markdown("")
            st.markdown("")
            if st.button("Add", key="add_custom"):
                add_water_intake(custom)
                st.rerun()
    
    st.divider()
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 3rem;'>🔥</div>
            <div style='font-size: 2rem; font-weight: 700;'>{st.session_state.streak}</div>
            <div>Day Streak</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 3rem;'>🏆</div>
            <div style='font-size: 2rem; font-weight: 700;'>{len(st.session_state.badges)}</div>
            <div>Badges</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        last_time = st.session_state.last_drink.strftime("%H:%M") if st.session_state.last_drink else "--:--"
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 3rem;'>⏰</div>
            <div style='font-size: 2rem; font-weight: 700;'>{last_time}</div>
            <div>Last Drink</div>
        </div>
        """, unsafe_allow_html=True)

def profile_screen():
    """Profile screen"""
    st.title(f"👤 {st.session_state.name}'s Profile")
    
    # Profile header
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Static droplet image
        colors = AGE_THEME_COLORS[st.session_state.age_group]
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="
                width: 100px;
                height: 120px;
                background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
                border-radius: 50% 50% 50% 0;
                transform: rotate(-45deg);
                margin: 10px auto;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            "></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### {st.session_state.name}")
        st.write(f"🎯 {AGE_GROUPS[st.session_state.age_group]['label']}")
        st.write(f"💧 Goal: {st.session_state.daily_goal}ml")
        days_active = max((datetime.now() - st.session_state.join_date).days, 1)
        st.write(f"📅 Active: {days_active} days")
    
    with col3:
        level = min(len(st.session_state.badges) + (st.session_state.streak // 5), 20)
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); border-radius: 12px; color: white;'>
            <div style='font-size: 2.5rem; font-weight: 800;'>{level}</div>
            <div>Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Water", f"{st.session_state.total_intake:,}ml",
                 delta=f"+{st.session_state.current_intake}ml today")
    
    with col2:
        today_count = len([e for e in st.session_state.intake_history if e['date'] == date.today()])
        st.metric("Total Glasses", st.session_state.total_glasses,
                 delta=f"+{today_count} today")
    
    with col3:
        st.metric("Current Streak", f"{st.session_state.streak} days",
                 delta=f"Best: {st.session_state.best_streak}")
    
    with col4:
        completion = int((len(st.session_state.badges) / len(BADGES)) * 100)
        st.metric("Badges", f"{len(st.session_state.badges)}/{len(BADGES)}",
                 delta=f"{completion}%")
    
    st.divider()
    
    # Badges
    st.markdown("### 🏆 Badges")
    tab1, tab2 = st.tabs(["Earned", "All Badges"])
    
    with tab1:
        if st.session_state.badges:
            cols = st.columns(4)
            for idx, badge_key in enumerate(st.session_state.badges):
                with cols[idx % 4]:
                    badge = BADGES[badge_key]
                    st.markdown(f"""
                    <div class='badge-item'>
                        <div style='font-size: 3rem;'>{badge['emoji']}</div>
                        <div style='font-weight: 700;'>{badge['title']}</div>
                        <div style='font-size: 0.85rem; opacity: 0.8;'>{badge['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🌟 Start logging to earn badges!")
    
    with tab2:
        cols = st.columns(4)
        for idx, (key, badge) in enumerate(BADGES.items()):
            with cols[idx % 4]:
                earned = key in st.session_state.badges
                opacity = "1" if earned else "0.4"
                st.markdown(f"""
                <div style='opacity: {opacity}; text-align: center; padding: 1rem;'>
                    <div style='font-size: 2.5rem;'>{badge['emoji']}</div>
                    <div style='font-weight: 600;'>{badge['title']}</div>
                    <div style='font-size: 0.8rem;'>{badge['description']}</div>
                    {'<div style="color: green;">✓ Earned</div>' if earned else '<div style="color: gray;">🔒 Locked</div>'}
                </div>
                """, unsafe_allow_html=True)

def charts_screen():
    """Analytics screen"""
    st.title("📊 Analytics & Charts")
    
    # Weekly chart
    st.markdown("### Weekly Progress")
    fig = create_weekly_chart()
    st.plotly_chart(fig, use_container_width=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    
    weekly_total = sum(d['intake'] for d in st.session_state.weekly_data[:-1])
    weekly_avg = int(weekly_total / 6) if len(st.session_state.weekly_data) > 1 else 0
    days_met = sum(1 for d in st.session_state.weekly_data if d['intake'] >= d['goal'])
    
    with col1:
        st.metric("Weekly Total", f"{weekly_total:,}ml")
    with col2:
        st.metric("Weekly Average", f"{weekly_avg}ml")
    with col3:
        st.metric("Goals Met", f"{days_met}/7")
    
    st.divider()
    
    # Recent activity
    if st.session_state.intake_history:
        st.markdown("### Recent Activity")
        recent = sorted(st.session_state.intake_history, 
                       key=lambda x: x['timestamp'], reverse=True)[:10]
        for entry in recent:
            st.markdown(f"💧 **{entry['amount']}ml** - {entry['timestamp'].strftime('%I:%M %p')}")
    else:
        st.info("No activity yet. Start logging!")

def settings_screen():
    """Settings screen"""
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Profile", "Notifications", "Appearance", "Advanced"])
    
    with tab1:
        st.markdown("### Profile Settings")
        
        new_name = st.text_input("Name", value=st.session_state.name)
        
        st.markdown("**Age Group:**")
        cols = st.columns(2)
        for idx, (key, value) in enumerate(AGE_GROUPS.items()):
            with cols[idx % 2]:
                selected = st.session_state.age_group == key
                if st.button(f"{value['icon']} {value['label']}", 
                           key=f"set_age_{key}",
                           use_container_width=True,
                           type="primary" if selected else "secondary"):
                    st.session_state.age_group = key
                    st.rerun()
        
        new_goal = st.slider("Daily Goal (ml)", 1000, 4000, 
                            st.session_state.daily_goal, 250)
        
        weight = st.number_input("Weight (kg)", 30, 200, st.session_state.weight)
        
        activity = st.selectbox("Activity Level", 
                               ['sedentary', 'light', 'moderate', 'active', 'very_active'],
                               index=['sedentary', 'light', 'moderate', 'active', 'very_active'].index(st.session_state.activity_level))
        
        if st.button("Save Profile", use_container_width=True):
            st.session_state.name = new_name
            st.session_state.daily_goal = new_goal
            st.session_state.weight = weight
            st.session_state.activity_level = activity
            st.success("✅ Profile updated!")
            st.rerun()
    
    with tab2:
        st.markdown("### Notification Settings")
        
        notif_enabled = st.checkbox("Enable Notifications", 
                                    value=st.session_state.notifications_enabled)
        st.session_state.notifications_enabled = notif_enabled
        
        if notif_enabled:
            freq = st.slider("Reminder Frequency (minutes)", 15, 180, 
                           st.session_state.notification_frequency, 15)
            st.session_state.notification_frequency = freq
            
            tone = st.selectbox("Notification Tone",
                              ['gentle', 'cheerful', 'motivational', 'silent'],
                              index=['gentle', 'cheerful', 'motivational', 'silent'].index(st.session_state.notification_tone))
            st.session_state.notification_tone = tone
        
        sound = st.checkbox("Enable Sounds", value=st.session_state.sound_enabled)
        st.session_state.sound_enabled = sound
    
    with tab3:
        st.markdown("### Appearance Settings")
        
        dark = st.checkbox("Dark Mode", value=st.session_state.dark_mode)
        st.session_state.dark_mode = dark
        
        high_contrast = st.checkbox("High Contrast", 
                                   value=st.session_state.high_contrast)
        st.session_state.high_contrast = high_contrast
        
        if st.button("Apply Theme", use_container_width=True):
            st.success("✅ Theme updated!")
            st.rerun()
    
    with tab4:
        st.markdown("### Advanced Settings")
        
        family = st.checkbox("Family/Group Mode", 
                           value=st.session_state.family_mode)
        st.session_state.family_mode = family
        
        st.divider()
        st.markdown("### Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Data", use_container_width=True):
                data = {
                    'name': st.session_state.name,
                    'total_intake': st.session_state.total_intake,
                    'streak': st.session_state.streak,
                    'badges': st.session_state.badges
                }
                st.download_button(
                    "Download JSON",
                    data=json.dumps(data, indent=2),
                    file_name=f"waterbuddy_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Reset Data", use_container_width=True, type="secondary"):
                if st.checkbox("⚠️ Confirm reset"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.success("Data reset!")
                    st.rerun()

def summary_screen():
    """Summary screen"""
    st.title("📋 Today's Summary")
    
    goal_met = st.session_state.current_intake >= st.session_state.daily_goal
    emoji = '🎉' if goal_met else '😊'
    st.markdown(f"<div style='text-align: center; font-size: 5rem;'>{emoji}</div>", 
               unsafe_allow_html=True)
    
    if goal_met:
        st.success("### 🎯 Fantastic work today!")
        st.write("You've crushed your hydration goal!")
    else:
        st.info("### 😊 Great progress today!")
        remaining = st.session_state.daily_goal - st.session_state.current_intake
        st.write(f"Just {remaining}ml more to reach your goal!")
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Today's Intake", f"{st.session_state.current_intake}ml")
    
    with col2:
        progress = int((st.session_state.current_intake / st.session_state.daily_goal) * 100)
        st.metric("Progress", f"{progress}%")
    
    with col3:
        today_glasses = len([e for e in st.session_state.intake_history 
                           if e['date'] == date.today()])
        st.metric("Glasses Today", today_glasses)
    
    with col4:
        st.metric("Streak", f"{st.session_state.streak} days")
    
    st.divider()
    
    st.markdown("### 📊 Progress")
    progress_pct = (st.session_state.current_intake / st.session_state.daily_goal) * 100
    fig = create_progress_gauge(progress_pct)
    st.plotly_chart(fig, use_container_width=True)

def leaderboard_screen():
    """Leaderboard screen"""
    st.title("🏆 Leaderboard")
    
    if not st.session_state.family_mode:
        st.info("Enable Family/Group mode in Settings!")
        return
    
    st.markdown("### Today's Standings")
    
    sorted_users = sorted(st.session_state.leaderboard_users, 
                         key=lambda x: x.get('intake', 0), reverse=True)
    
    for idx, user in enumerate(sorted_users):
        medals = {0: '🥇', 1: '🥈', 2: '🥉'}
        position = medals.get(idx, f"{idx + 1}.")
        
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        
        with col1:
            st.markdown(f"### {position}")
        with col2:
            st.markdown(f"### {user.get('name', 'Unknown')}")
        with col3:
            st.metric("Intake", f"{user.get('intake', 0)}ml")
        with col4:
            st.metric("Streak", f"{user.get('streak', 0)} days")
        
        st.divider()

def reminders_screen():
    """Reminders screen"""
    st.title("⏰ Reminders")
    
    if st.session_state.notifications_enabled:
        st.info("💧 Reminders are enabled!")
        st.write(f"Frequency: Every {st.session_state.notification_frequency} minutes")
    else:
        st.warning("Reminders are disabled. Enable in Settings!")

def help_screen():
    """Help screen"""
    st.title("❓ Help & Support")
    
    st.markdown("""
    ### Quick Start Guide
    
    **1. Log Water** 🥤
    - Use buttons to log drinks quickly
    
    **2. Track Progress** 📊
    - Watch your progress bar fill up
    
    **3. Build Streaks** 🔥
    - Maintain daily goals
    
    **4. Earn Badges** 🏆
    - Complete challenges
    
    ### FAQ
    
    **Q: Is data safe?**  
    A: Yes! Stored locally in your browser.
    
    **Q: How do streaks work?**  
    A: Reach your goal daily to maintain streak.
    """)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    
    init_session_state()
    apply_custom_css()
    
    if st.session_state.show_onboarding:
        if st.session_state.current_screen == 'splash':
            splash_screen()
        else:
            onboarding_screen()
    else:
        # Sidebar navigation using selectbox instead of buttons
        with st.sidebar:
            st.markdown("### 💧 WaterBuddy")
            st.caption(f"Hello, {st.session_state.name}!")
            
            st.divider()
            
            # Navigation using selectbox (more reliable in Streamlit)
            screen_options = {
                'Dashboard': 'dashboard',
                'Profile': 'profile',
                'Analytics': 'charts',
                'Leaderboard': 'leaderboard',
                'Reminders': 'reminders',
                'Summary': 'summary',
                'Help': 'help',
                'Settings': 'settings'
            }
            
            # Find current screen index
            current_index = list(screen_options.values()).index(st.session_state.current_screen) if st.session_state.current_screen in screen_options.values() else 0
            
            selected_screen = st.selectbox(
                "Navigate to:",
                options=list(screen_options.keys()),
                index=current_index,
                key="nav_selector"
            )
            
            # Update current screen
            st.session_state.current_screen = screen_options[selected_screen]
            
            st.divider()
            
            st.markdown("### Today")
            st.metric("Intake", f"{st.session_state.current_intake}ml")
            st.metric("Goal", f"{st.session_state.daily_goal}ml")
            progress = (st.session_state.current_intake / st.session_state.daily_goal) * 100
            st.progress(min(progress / 100, 1.0))
            
            st.divider()
            st.caption("🔒 Your data stays local")
        
        # Main content based on current screen
        if st.session_state.current_screen == 'dashboard':
            dashboard_screen()
        elif st.session_state.current_screen == 'profile':
            profile_screen()
        elif st.session_state.current_screen == 'charts':
            charts_screen()
        elif st.session_state.current_screen == 'leaderboard':
            leaderboard_screen()
        elif st.session_state.current_screen == 'reminders':
            reminders_screen()
        elif st.session_state.current_screen == 'summary':
            summary_screen()
        elif st.session_state.current_screen == 'help':
            help_screen()
        elif st.session_state.current_screen == 'settings':
            settings_screen()

if __name__ == "__main__":
    main()
