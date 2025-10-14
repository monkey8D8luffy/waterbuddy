"""
WaterBuddy - Age-Adaptive Hydration Tracking App
A comprehensive hydration companion built with Streamlit
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
import json
from typing import List, Dict
import pandas as pd
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
    'teen': {'label': 'Teens (13-18)', 'icon': '🧑‍🎓', 'min': 13, 'max': 18},
    'adult': {'label': 'Adults (19-64)', 'icon': '👨‍💼', 'min': 19, 'max': 64},
    'senior': {'label': 'Seniors (65+)', 'icon': '👴', 'min': 65, 'max': 120}
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

COLORS = {
    'aqua_primary': '#70D6FF',
    'deep_teal': '#1E9BC7',
    'soft_coral': '#FFB3A7',
    'pale_sand': '#FFF7EE',
    'dark_slate': '#123743',
}

AGE_THEME_COLORS = {
    'children': {'primary': '#FF6B9D', 'secondary': '#FFE66D', 'accent': '#4ECDC4'},
    'teen': {'primary': '#7C3AED', 'secondary': '#F59E0B', 'accent': '#EF4444'},
    'adult': {'primary': '#70D6FF', 'secondary': '#1E9BC7', 'accent': '#FFB3A7'},
    'senior': {'primary': '#1E9BC7', 'secondary': '#FFB3A7', 'accent': '#70D6FF'}
}

WATER_SIZES = [
    {'amount': 250, 'label': 'Glass', 'icon': '🥛'},
    {'amount': 330, 'label': 'Can', 'icon': '🥤'},
    {'amount': 500, 'label': 'Bottle', 'icon': '🍶'},
    {'amount': 750, 'label': 'Large Bottle', 'icon': '🚰'}
]

# ============================================================================
# STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    
    # User profile
    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'age_group' not in st.session_state:
        st.session_state.age_group = 'adult'
    if 'daily_goal' not in st.session_state:
        st.session_state.daily_goal = 2000
    if 'join_date' not in st.session_state:
        st.session_state.join_date = datetime.now()
    
    # Tracking data
    if 'current_intake' not in st.session_state:
        st.session_state.current_intake = 0
    if 'intake_history' not in st.session_state:
        st.session_state.intake_history = []
    if 'last_drink' not in st.session_state:
        st.session_state.last_drink = None
    
    # Gamification
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'best_streak' not in st.session_state:
        st.session_state.best_streak = 0
    if 'badges' not in st.session_state:
        st.session_state.badges = []
    if 'total_intake' not in st.session_state:
        st.session_state.total_intake = 0
    if 'total_glasses' not in st.session_state:
        st.session_state.total_glasses = 0
    
    # Settings
    if 'notifications_enabled' not in st.session_state:
        st.session_state.notifications_enabled = True
    if 'notification_frequency' not in st.session_state:
        st.session_state.notification_frequency = 60
    if 'notification_tone' not in st.session_state:
        st.session_state.notification_tone = 'gentle'
    if 'sound_enabled' not in st.session_state:
        st.session_state.sound_enabled = True
    if 'high_contrast' not in st.session_state:
        st.session_state.high_contrast = False
    if 'family_mode' not in st.session_state:
        st.session_state.family_mode = False
    
    # UI state
    if 'screen' not in st.session_state:
        st.session_state.screen = 'splash' if not st.session_state.name else 'dashboard'
    if 'show_onboarding' not in st.session_state:
        st.session_state.show_onboarding = not st.session_state.name
    if 'today_date' not in st.session_state:
        st.session_state.today_date = date.today()
    
    # Weekly data for charts
    if 'weekly_data' not in st.session_state:
        st.session_state.weekly_data = generate_weekly_data()
    
    # Load leaderboard from CSV if available
    if 'leaderboard_users' not in st.session_state:
        st.session_state.leaderboard_users = load_leaderboard_data()
    
    # Celebration state
    if 'show_celebration' not in st.session_state:
        st.session_state.show_celebration = False
    
    # Reminder state
    if 'last_reminder_time' not in st.session_state:
        st.session_state.last_reminder_time = datetime.now()

def load_leaderboard_data():
    """Load leaderboard data from CSV if exists"""
    try:
        if os.path.exists('data/leaderboard.csv'):
            df = pd.read_csv('data/leaderboard.csv')
            return df.to_dict('records')
    except:
        pass
    
    # Default mock data
    return [
        {'name': st.session_state.get('name', 'You'), 'intake': 0, 'streak': 0},
        {'name': 'Family Member 1', 'intake': 1800, 'streak': 5},
        {'name': 'Family Member 2', 'intake': 2200, 'streak': 8},
        {'name': 'Family Member 3', 'intake': 1500, 'streak': 3}
    ]

def generate_weekly_data():
    """Generate sample weekly data"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    data = []
    for i, day in enumerate(days):
        if i < 6:
            intake = 1700 + (i * 100)
        else:
            intake = st.session_state.get('current_intake', 0)
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
            'encouragement': "You're doing amazing! Keep it up, champ! 🌟",
            'goal_reached': "🎉 WOW! You're a water superhero! Amazing job! 🎉"
        },
        'teen': {
            'greeting': "Hey! Ready to level up? 🚀",
            'encouragement': "Crushing those goals! Don't break the streak! 🔥",
            'goal_reached': "Goal Crushed! 🔥 Daily target achieved! Your streak game is strong!"
        },
        'adult': {
            'greeting': "Good day! Let's stay hydrated 💼",
            'encouragement': "Great progress — you're boosting your focus! 🎯",
            'goal_reached': "Goal Achieved! 🎯 Excellent work! You've reached your daily hydration target."
        },
        'senior': {
            'greeting': "Hello! Time to stay refreshed 🌸",
            'encouragement': "Wonderful progress — keep up the gentle pace! 🌿",
            'goal_reached': "Well Done! 🌿 Wonderful! You've completed your daily hydration goal."
        }
    }
    
    age_group = st.session_state.get('age_group', 'adult')
    return messages[age_group].get(message_type, '')

def create_mascot_svg(expression: str = 'smile', size: str = 'medium'):
    """Create animated SVG mascot - optimized for Streamlit"""
    
    age_colors = AGE_THEME_COLORS[st.session_state.age_group]
    
    # Size mapping
    sizes = {
        'small': '120px',
        'medium': '180px',
        'large': '220px'
    }
    svg_size = sizes.get(size, '180px')
    
    # Eye expressions
    eyes = {
        'neutral': '<circle cx="45" cy="48" r="4" fill="#123743"/><circle cx="65" cy="48" r="4" fill="#123743"/>',
        'smile': '<circle cx="45" cy="46" r="5" fill="#123743"/><circle cx="65" cy="46" r="5" fill="#123743"/><path d="M40 58 Q55 68 70 58" stroke="#123743" stroke-width="4" fill="none" stroke-linecap="round"/>',
        'cheer': '<circle cx="45" cy="44" r="6" fill="#123743"/><circle cx="65" cy="44" r="6" fill="#123743"/><path d="M35 58 Q55 75 75 58" stroke="#123743" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="42" cy="41" r="2" fill="white"/><circle cx="62" cy="41" r="2" fill="white"/>',
        'excited': '<circle cx="45" cy="45" r="6" fill="#123743"/><circle cx="65" cy="45" r="6" fill="#123743"/><path d="M38 58 Q55 72 72 58" stroke="#123743" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="43" cy="42" r="2" fill="white"/><circle cx="63" cy="42" r="2" fill="white"/>',
    }
    
    eye_svg = eyes.get(expression, eyes['neutral'])
    
    svg = f"""
    <div style="text-align: center; padding: 1rem;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 140" style="width: {svg_size}; height: {svg_size};">
            <defs>
                <linearGradient id="mascotGrad_{expression}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{age_colors['primary']};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{age_colors['secondary']};stop-opacity:0.9" />
                </linearGradient>
            </defs>
            
            <!-- Shadow -->
            <ellipse cx="55" cy="125" rx="25" ry="5" fill="#00000020"/>
            
            <!-- Main droplet body -->
            <path d="M55 20 C35 42, 22 62, 22 82 C22 100, 36 118, 55 118 C74 118, 88 100, 88 82 C88 62, 75 42, 55 20 Z"
                  fill="url(#mascotGrad_{expression})" 
                  stroke="{age_colors['primary']}" 
                  stroke-width="3">
            </path>
            
            <!-- Highlight shine -->
            <ellipse cx="42" cy="50" rx="12" ry="18" fill="#FFFFFF" opacity="0.5"/>
            <ellipse cx="47" cy="55" rx="6" ry="10" fill="#FFFFFF" opacity="0.7"/>
            
            <!-- Face -->
            {eye_svg}
            
            {'<!-- Celebration sparkles -->' if expression == 'cheer' else ''}
            {f'<circle cx="15" cy="35" r="3" fill="{age_colors["accent"]}" opacity="0.9"/>' if expression == 'cheer' else ''}
            {f'<circle cx="95" cy="45" r="3" fill="{age_colors["accent"]}" opacity="0.9"/>' if expression == 'cheer' else ''}
            {f'<circle cx="10" cy="70" r="2.5" fill="{age_colors["secondary"]}" opacity="0.9"/>' if expression == 'cheer' else ''}
            {f'<circle cx="100" cy="75" r="2.5" fill="{age_colors["primary"]}" opacity="0.9"/>' if expression == 'cheer' else ''}
        </svg>
    </div>
    """
    
    return svg

def create_bottle_visualization(percentage: float):
    """Create bottle fill visualization - optimized for Streamlit"""
    
    age_colors = AGE_THEME_COLORS[st.session_state.age_group]
    fill_height = max(0, min(100, percentage))
    
    # Calculate water level (inverted - higher percentage = higher water)
    water_level = 130 - (fill_height * 1.05)  # Max height 130, scales with percentage
    
    svg = f"""
    <div style="text-align: center; padding: 1rem;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 160" style="width: 160px; height: 240px;">
            <defs>
                <linearGradient id="waterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:{age_colors['primary']};stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:{age_colors['secondary']};stop-opacity:1" />
                </linearGradient>
                <clipPath id="bottleShape">
                    <path d="M28 28 L72 28 L72 135 C72 140 68 145 63 145 L37 145 C32 145 28 140 28 135 Z"/>
                </clipPath>
            </defs>
            
            <!-- Bottle outline -->
            <path d="M32 22 L32 18 C32 12 36 8 42 8 L58 8 C64 8 68 12 68 18 L68 22 L72 28 L72 135 C72 140 68 145 63 145 L37 145 C32 145 28 140 28 135 L28 28 Z"
                  fill="rgba(255,255,255,0.95)" 
                  stroke="{age_colors['primary']}" 
                  stroke-width="3"/>
            
            <!-- Bottle cap -->
            <rect x="38" y="8" width="24" height="12" rx="6" 
                  fill="{age_colors['secondary']}" 
                  stroke="{age_colors['primary']}" 
                  stroke-width="2"/>
            
            <!-- Water fill -->
            <g clip-path="url(#bottleShape)">
                {f'''
                <!-- Water body -->
                <rect x="28" y="{water_level}" width="44" height="{145 - water_level}" 
                      fill="url(#waterGrad)"/>
                
                <!-- Water surface line -->
                <line x1="28" y1="{water_level}" x2="72" y2="{water_level}" 
                      stroke="{age_colors['primary']}" 
                      stroke-width="2" 
                      opacity="0.6"/>
                
                <!-- Bubbles -->
                <circle cx="42" cy="{min(water_level + 25, 135)}" r="3" fill="white" opacity="0.6"/>
                <circle cx="58" cy="{min(water_level + 40, 135)}" r="2.5" fill="white" opacity="0.5"/>
                <circle cx="48" cy="{min(water_level + 15, 135)}" r="2" fill="white" opacity="0.7"/>
                ''' if fill_height > 5 else ''}
            </g>
            
            <!-- Measurement lines -->
            <line x1="20" y1="50" x2="25" y2="50" stroke="#999" stroke-width="1"/>
            <line x1="20" y1="85" x2="25" y2="85" stroke="#999" stroke-width="1"/>
            <line x1="20" y1="120" x2="25" y2="120" stroke="#999" stroke-width="1"/>
            
            <!-- Percentage display -->
            <text x="50" y="80" font-size="24" font-weight="bold" text-anchor="middle" fill="{age_colors['primary']}">
                {int(fill_height)}%
            </text>
            
            <!-- Labels -->
            <text x="50" y="157" font-size="10" text-anchor="middle" fill="#666">
                {st.session_state.current_intake}ml / {st.session_state.daily_goal}ml
            </text>
        </svg>
    </div>
    """
    
    return svg

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
    
    # Update weekly data
    st.session_state.weekly_data = generate_weekly_data()
    
    # Update leaderboard
    update_leaderboard()

def check_badges(new_intake, old_intake):
    """Check and award badges"""
    # First glass badge
    if 'first-glass' not in st.session_state.badges and st.session_state.total_glasses == 1:
        st.session_state.badges.append('first-glass')
        st.success(f"🌟 Badge Earned: {BADGES['first-glass']['title']}!")
    
    # Daily goal achievement
    if new_intake >= st.session_state.daily_goal and old_intake < st.session_state.daily_goal:
        if 'daily-goal' not in st.session_state.badges:
            st.session_state.badges.append('daily-goal')
        st.session_state.show_celebration = True
        st.balloons()
        st.success(get_age_specific_message('goal_reached'))
    
    # Hydration hero (100 glasses)
    if st.session_state.total_glasses >= 100 and 'hydration-hero' not in st.session_state.badges:
        st.session_state.badges.append('hydration-hero')
        st.success(f"💪 Badge Earned: {BADGES['hydration-hero']['title']}!")
    
    # Early bird (morning drink)
    current_hour = datetime.now().hour
    if 5 <= current_hour < 9 and 'early-bird' not in st.session_state.badges:
        st.session_state.badges.append('early-bird')
        st.success(f"🌅 Badge Earned: {BADGES['early-bird']['title']}!")
    
    # Night owl (evening drink)
    if 20 <= current_hour < 24 and 'night-owl' not in st.session_state.badges:
        st.session_state.badges.append('night-owl')
        st.success(f"🦉 Badge Earned: {BADGES['night-owl']['title']}!")
    
    # Overachiever
    if new_intake >= st.session_state.daily_goal * 1.5 and 'overachiever' not in st.session_state.badges:
        st.session_state.badges.append('overachiever')
        st.success(f"🚀 Badge Earned: {BADGES['overachiever']['title']}!")

def update_leaderboard():
    """Update leaderboard with current user's data"""
    if st.session_state.family_mode:
        for user in st.session_state.leaderboard_users:
            if user.get('name') == st.session_state.name or user.get('name') == 'You':
                user['intake'] = st.session_state.current_intake
                user['streak'] = st.session_state.streak

def check_streak():
    """Check and update streak"""
    today = date.today()
    if st.session_state.today_date != today:
        # New day - check if goal was met yesterday
        if st.session_state.current_intake >= st.session_state.daily_goal:
            st.session_state.streak += 1
            if st.session_state.streak > st.session_state.best_streak:
                st.session_state.best_streak = st.session_state.streak
        else:
            st.session_state.streak = 0
        
        # Reset daily intake
        st.session_state.current_intake = 0
        st.session_state.today_date = today
        
        # Check streak badges
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
    """Apply custom CSS based on age group and settings"""
    
    age_colors = AGE_THEME_COLORS[st.session_state.age_group]
    
    # Font sizes by age group
    font_sizes = {
        'children': '18px',
        'teen': '16px',
        'adult': '16px',
        'senior': '22px'
    }
    
    # Border radius by age group
    border_radius = {
        'children': '1.5rem',
        'teen': '0.75rem',
        'adult': '0.5rem',
        'senior': '1rem'
    }
    
    base_font = font_sizes[st.session_state.age_group]
    radius = border_radius[st.session_state.age_group]
    
    high_contrast = st.session_state.high_contrast
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Base styling */
    .stApp {{
        background: {'#000000' if high_contrast else 'linear-gradient(135deg, ' + COLORS['pale_sand'] + ' 0%, #E8F4F8 100%)'};
        color: {'#ffffff' if high_contrast else COLORS['dark_slate']};
        font-size: {base_font};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Headers */
    h1, h2, h3 {{
        color: {age_colors['primary']};
        font-weight: 700;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {age_colors['primary']} 0%, {age_colors['secondary']} 100%);
        color: white;
        border-radius: {radius};
        border: none;
        padding: 0.85rem 1.75rem;
        font-size: {base_font};
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }}
    
    /* Progress bars */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {age_colors['secondary']} 0%, {age_colors['primary']} 100%);
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: {age_colors['primary']};
        font-size: 2.2rem;
        font-weight: 800;
    }}
    
    /* Sidebar with glassmorphism */
    [data-testid="stSidebar"] {{
        background: {'#111111' if high_contrast else 'rgba(255, 255, 255, 0.85)'};
        backdrop-filter: blur(10px);
        border-right: {'2px solid #ffffff' if high_contrast else f"2px solid {age_colors['primary']}33"};
    }}
    
    /* Stat cards with hover effect */
    .stat-card {{
        background: {'#222222' if high_contrast else 'rgba(255, 255, 255, 0.9)'};
        border-radius: {radius};
        padding: 1.5rem;
        text-align: center;
        border: {'2px solid #ffffff' if high_contrast else f"3px solid {age_colors['primary']}22"};
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }}
    
    .stat-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-color: {age_colors['primary']};
    }}
    
    /* Badge container */
    .badge-container {{
        display: inline-block;
        background: linear-gradient(135deg, {age_colors['primary']}22 0%, {age_colors['secondary']}22 100%);
        border: 3px solid {age_colors['primary']};
        border-radius: {radius};
        padding: 1rem 1.5rem;
        margin: 0.5rem;
        transition: all 0.2s ease;
    }}
    
    .badge-container:hover {{
        transform: scale(1.08);
        box-shadow: 0 6px 20px {age_colors['primary']}55;
    }}
    
    /* Input styling */
    .stTextInput > div > div > input {{
        border-radius: {radius};
        border: {'2px solid #ffffff' if high_contrast else f"2px solid {age_colors['primary']}44"};
        font-size: {base_font};
        padding: 0.75rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {age_colors['primary']};
        box-shadow: 0 0 0 3px {age_colors['primary']}33;
    }}
    
    /* Slider */
    .stSlider > div > div > div {{
        background: {age_colors['primary']};
    }}
    
    /* Tabs with smooth transitions */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.75rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: {'#222222' if high_contrast else age_colors['primary']}22;
        border-radius: {radius};
        color: {age_colors['primary']};
        padding: 0.85rem 1.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {age_colors['primary']} 0%, {age_colors['secondary']} 100%);
        color: white;
        box-shadow: 0 4px 15px {age_colors['primary']}44;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['pale_sand']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {age_colors['primary']};
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {age_colors['secondary']};
    }}
    
    /* Mascot class */
    .mascot {{
        display: inline-block;
    }}
    
    /* Metric card */
    .metric-card {{
        opacity: 1;
    }}
    
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# VISUALIZATION COMPONENTS
# ============================================================================

def create_weekly_chart():
    """Create weekly intake chart with enhanced styling"""
    
    age_colors = AGE_THEME_COLORS[st.session_state.age_group]
    weekly_data = st.session_state.weekly_data
    
    days = [d['day'] for d in weekly_data]
    intakes = [d['intake'] for d in weekly_data]
    goals = [d['goal'] for d in weekly_data]
    
    fig = go.Figure()
    
    # Goal line
    fig.add_trace(go.Scatter(
        x=days,
        y=goals,
        mode='lines',
        name='Goal',
        line=dict(color='#94a3b8', width=3, dash='dash'),
        hovertemplate='Goal: %{y}ml<extra></extra>'
    ))
    
    # Actual intake bars
    colors = [age_colors['primary'] if intake >= goal else age_colors['secondary'] 
              for intake, goal in zip(intakes, goals)]
    
    fig.add_trace(go.Bar(
        x=days,
        y=intakes,
        name='Intake',
        marker=dict(
            color=colors,
            line=dict(color=age_colors['primary'], width=2)
        ),
        text=[f"{intake}ml" for intake in intakes],
        textposition='outside',
        hovertemplate='%{x}<br>Intake: %{y}ml<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Weekly Hydration Progress",
            'font': {'size': 24, 'color': age_colors['primary'], 'family': 'Inter'}
        },
        xaxis_title="Day",
        yaxis_title="Water (ml)",
        height=450,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=14)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    
    return fig

def create_progress_ring(percentage: float):
    """Create a circular progress indicator"""
    
    age_colors = AGE_THEME_COLORS[st.session_state.age_group]
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Daily Goal Progress", 'font': {'size': 24, 'family': 'Inter', 'color': age_colors['primary']}},
        delta={'reference': 100, 'suffix': '%'},
        number={'suffix': '%', 'font': {'size': 48, 'family': 'Inter'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': age_colors['primary']},
            'bar': {'color': age_colors['primary'], 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': age_colors['secondary'],
            'steps': [
                {'range': [0, 50], 'color': age_colors['secondary'] + '22'},
                {'range': [50, 75], 'color': age_colors['primary'] + '33'},
                {'range': [75, 100], 'color': age_colors['accent'] + '44'}
            ],
            'threshold': {
                'line': {'color': age_colors['accent'], 'width': 5},
                'thickness': 0.85,
                'value': 100
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter')
    )
    
    return fig

# ============================================================================
# SCREEN COMPONENTS
# ============================================================================

def splash_screen():
    """Display splash screen"""
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem;'>
        <div style='font-size: 8rem;'>
            💧
        </div>
        <h1 style='font-size: 3.5rem; margin-top: 2rem; color: #70D6FF;'>WaterBuddy</h1>
        <p style='font-size: 1.5rem; opacity: 0.9; margin-top: 1rem;'>Your personal hydration companion</p>
        <p style='margin-top: 2rem; opacity: 0.7; font-size: 1rem;'>🔒 Privacy-first • No account needed<br/>Your data stays on your device</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started →", key="splash_start", use_container_width=True):
            st.session_state.screen = 'onboarding'
            st.rerun()

def onboarding_screen():
    """Onboarding flow for new users"""
    
    st.markdown("<div style='text-align: center; font-size: 5rem;' class='mascot'>💧</div>", unsafe_allow_html=True)
    st.title("Let's get started!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Name input
        name = st.text_input("What's your name?", value=st.session_state.name, key="onboard_name", placeholder="Enter your name...")
        
        # Age group selection
        st.write("### Choose your age group:")
        
        cols = st.columns(2)
        for idx, (key, value) in enumerate(AGE_GROUPS.items()):
            with cols[idx % 2]:
                if st.button(
                    f"{value['icon']} {value['label']}", 
                    key=f"age_{key}",
                    use_container_width=True,
                    type="primary" if st.session_state.age_group == key else "secondary"
                ):
                    st.session_state.age_group = key
                    st.rerun()
        
        st.info(f"**Selected:** {AGE_GROUPS[st.session_state.age_group]['label']}")
        
        # Daily goal
        st.write("### Set your daily goal:")
        daily_goal = st.slider(
            "Daily goal (ml)",
            min_value=1000,
            max_value=4000,
            value=st.session_state.daily_goal,
            step=250,
            key="onboard_goal"
        )
        st.success(f"Your daily goal: **{daily_goal}ml** ({daily_goal // 250} glasses)")
        
        # Family mode
        family_mode = st.checkbox("Enable Family/Group mode", value=st.session_state.family_mode)
        
        # Start button
        st.write("")
        if st.button("Start My Journey! 🚀", key="start_journey", use_container_width=True):
            if name.strip():
                st.session_state.name = name
                st.session_state.daily_goal = daily_goal
                st.session_state.family_mode = family_mode
                st.session_state.screen = 'dashboard'
                st.session_state.show_onboarding = False
                st.session_state.join_date = datetime.now()
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter your name to continue!")

def dashboard_screen():
    """Main dashboard screen"""
    
    # Check streak on page load
    check_streak()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(get_age_specific_message('greeting'))
        st.caption(f"👋 {st.session_state.name}")
        st.caption(datetime.now().strftime("%A, %B %d, %Y"))
    
    with col2:
        mascot_expression = 'smile' if st.session_state.current_intake > 0 else 'neutral'
        if st.session_state.current_intake >= st.session_state.daily_goal:
            mascot_expression = 'cheer'
        elif st.session_state.current_intake >= st.session_state.daily_goal * 0.75:
            mascot_expression = 'excited'
        
        mascot_svg = create_mascot_svg(mascot_expression, 'large')
        st.markdown(mascot_svg, unsafe_allow_html=True)
    
    st.divider()
    
    # Progress section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Today's Progress")
        
        progress_pct = (st.session_state.current_intake / st.session_state.daily_goal) * 100
        
        st.progress(min(progress_pct / 100, 1.0))
        
        st.markdown(f"""
        <div style='font-size: 2rem; font-weight: 700; margin: 1.5rem 0; color: {AGE_THEME_COLORS[st.session_state.age_group]['primary']};'>
            {st.session_state.current_intake}ml / {st.session_state.daily_goal}ml
        </div>
        """, unsafe_allow_html=True)
        
        st.info(get_age_specific_message('encouragement'))
    
    with col2:
        bottle_svg = create_bottle_visualization(progress_pct)
        st.markdown(bottle_svg, unsafe_allow_html=True)
    
    st.divider()
    
    # Water intake buttons
    st.markdown("### 💧 Log Water Intake")
    
    cols = st.columns(4)
    for idx, water_size in enumerate(WATER_SIZES):
        with cols[idx]:
            if st.button(
                f"{water_size['icon']}\n\n**{water_size['label']}**\n\n{water_size['amount']}ml",
                key=f"water_{water_size['amount']}",
                use_container_width=True
            ):
                add_water_intake(water_size['amount'])
                st.rerun()
    
    # Custom amount
    with st.expander("➕ Add Custom Amount"):
        col1, col2 = st.columns([3, 1])
        with col1:
            custom_amount = st.number_input(
                "Enter amount (ml)", 
                min_value=1, 
                max_value=2000, 
                value=250,
                step=50,
                key="custom_amount"
            )
        with col2:
            st.write("")
            st.write("")
            if st.button("Add", key="add_custom"):
                add_water_intake(custom_amount)
                st.rerun()
    
    st.divider()
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card metric-card'>
            <div style='font-size: 3rem;'>🔥</div>
            <div style='font-size: 2rem; font-weight: 800; margin: 0.5rem 0;'>{st.session_state.streak}</div>
            <div style='opacity: 0.85; font-size: 1.1rem;'>Day Streak</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card metric-card'>
            <div style='font-size: 3rem;'>🏆</div>
            <div style='font-size: 2rem; font-weight: 800; margin: 0.5rem 0;'>{len(st.session_state.badges)}</div>
            <div style='opacity: 0.85; font-size: 1.1rem;'>Badges Earned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        last_time = st.session_state.last_drink.strftime("%H:%M") if st.session_state.last_drink else "--:--"
        st.markdown(f"""
        <div class='stat-card metric-card'>
            <div style='font-size: 3rem;'>⏰</div>
            <div style='font-size: 2rem; font-weight: 800; margin: 0.5rem 0;'>{last_time}</div>
            <div style='opacity: 0.85; font-size: 1.1rem;'>Last Drink</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Hydration tips
    st.markdown("### 💡 Daily Hydration Tip")
    
    tips = {
        'children': [
            "🌟 Water helps you think better in school!",
            "🏃 Drink water before playing to have more energy!",
            "🎨 Your brain is 75% water - keep it happy!",
            "⚽ Athletes drink lots of water to be their best!"
        ],
        'teen': [
            "🧠 Proper hydration improves concentration by up to 30%!",
            "💪 Drinking water before meals can help with healthy weight management.",
            "🎯 Dehydration can affect your mood and energy levels.",
            "⚡ Start your day with a glass of water to boost metabolism!"
        ],
        'adult': [
            "💼 Staying hydrated improves workplace productivity by 14%.",
            "🎯 Water helps reduce stress and maintain focus during long meetings.",
            "⚡ Proper hydration supports healthy blood pressure levels.",
            "🧘 Drinking water can help prevent afternoon fatigue."
        ],
        'senior': [
            "🌿 Adequate hydration supports healthy joint function.",
            "💊 Water helps your body absorb medications properly.",
            "🧠 Staying hydrated supports memory and cognitive function.",
            "❤️ Proper hydration is vital for heart health and circulation."
        ]
    }
    
    import random
    tip_of_day = random.choice(tips[st.session_state.age_group])
    st.info(tip_of_day)

def profile_screen():
    """Enhanced user profile with useful statistics and insights"""
    
    st.title(f"👤 {st.session_state.name}'s Profile")
    
    # Profile header with avatar and quick stats
    col_avatar, col_info, col_level = st.columns([1, 2, 1])
    
    with col_avatar:
        mascot_svg = create_mascot_svg('smile', 'large')
        st.markdown(mascot_svg, unsafe_allow_html=True)
    
    with col_info:
        st.markdown(f"### {st.session_state.name}")
        st.write(f"🎯 {AGE_GROUPS[st.session_state.age_group]['label']}")
        st.write(f"💧 Daily Goal: {st.session_state.daily_goal}ml")
        days_active = max((datetime.now() - st.session_state.join_date).days, 1)
        st.write(f"📅 Active for {days_active} days")
    
    with col_level:
        level = min(len(st.session_state.badges) + (st.session_state.streak // 5), 20)
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, {AGE_THEME_COLORS[st.session_state.age_group]['primary']} 0%, {AGE_THEME_COLORS[st.session_state.age_group]['secondary']} 100%); border-radius: 1rem; color: white;'>
            <div style='font-size: 2.5rem; font-weight: 800;'>{level}</div>
            <div style='font-size: 0.9rem; opacity: 0.9;'>Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Key metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Water", f"{st.session_state.total_intake:,}ml", 
                  delta=f"+{st.session_state.current_intake}ml today")
    
    with col2:
        st.metric("Total Glasses", st.session_state.total_glasses,
                  delta=f"+{len([e for e in st.session_state.intake_history if e['date'] == date.today()])} today")
    
    with col3:
        st.metric("Current Streak", f"{st.session_state.streak} days",
                  delta=f"Best: {st.session_state.best_streak}")
    
    with col4:
        completion = (len(st.session_state.badges) / len(BADGES)) * 100
        st.metric("Achievements", f"{len(st.session_state.badges)}/{len(BADGES)}",
                  delta=f"{int(completion)}%")
    
    st.divider()
    
    # Insights section
    st.markdown("### 💡 Your Hydration Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate average daily intake
        if st.session_state.intake_history:
            avg_daily = st.session_state.total_intake / max(days_active, 1)
            st.metric("Average Daily Intake", f"{int(avg_daily)}ml")
            
            # Calculate success rate
            if days_active > 0:
                success_rate = (st.session_state.streak / days_active) * 100
                st.metric("Goal Success Rate", f"{int(success_rate)}%")
        else:
            st.info("Start logging water to see your insights!")
    
    with col2:
        # Most active time
        if st.session_state.intake_history:
            hours = [entry['timestamp'].hour for entry in st.session_state.intake_history]
            if hours:
                most_active_hour = max(set(hours), key=hours.count)
                st.metric("Most Active Hour", f"{most_active_hour:02d}:00")
            
            # Weekly average
            weekly_avg = (st.session_state.total_intake / max(days_active, 1)) * 7
            st.metric("Weekly Average", f"{int(weekly_avg):,}ml")
    
    st.divider()
    
    # Badges section
    st.markdown("### 🏆 Badges & Achievements")
    
    tab1, tab2 = st.tabs(["Earned Badges", "All Badges"])
    
    with tab1:
        if st.session_state.badges:
            badge_cols = st.columns(4)
            for idx, badge_key in enumerate(st.session_state.badges):
                with badge_cols[idx % 4]:
                    badge = BADGES[badge_key]
                    st.markdown(f"""
                    <div class='badge-container'>
                        <div style='font-size: 3rem;'>{badge['emoji']}</div>
                        <div style='font-weight: 700; margin-top: 0.5rem;'>{badge['title']}</div>
                        <div style='font-size: 0.85rem; opacity: 0.8;'>{badge['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🌟 Start logging water to earn your first badge!")
    
    with tab2:
        all_badge_cols = st.columns(4)
        for idx, (badge_key, badge) in enumerate(BADGES.items()):
            with all_badge_cols[idx % 4]:
                earned = badge_key in st.session_state.badges
                opacity = "1" if earned else "0.3"
                st.markdown(f"""
                <div style='opacity: {opacity}; text-align: center; padding: 1rem; margin: 0.5rem;'>
                    <div style='font-size: 2.5rem;'>{badge['emoji']}</div>
                    <div style='font-weight: 600; margin-top: 0.5rem;'>{badge['title']}</div>
                    <div style='font-size: 0.8rem; opacity: 0.8;'>{badge['description']}</div>
                    {'<div style="color: green; margin-top: 0.5rem;">✓ Earned</div>' if earned else '<div style="color: gray; margin-top: 0.5rem;">🔒 Locked</div>'}
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Progress visualization
    st.markdown("### 📊 Today's Progress")
    progress_pct = (st.session_state.current_intake / st.session_state.daily_goal) * 100
    
    col1, col2 = st.columns([2, 1])
    with col1:
        ring_fig = create_progress_ring(progress_pct)
        st.plotly_chart(ring_fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Quick Actions")
        if st.button("📥 Export My Data", use_container_width=True):
            data = {
                'name': st.session_state.name,
                'age_group': st.session_state.age_group,
                'daily_goal': st.session_state.daily_goal,
                'total_intake': st.session_state.total_intake,
                'total_glasses': st.session_state.total_glasses,
                'streak': st.session_state.streak,
                'best_streak': st.session_state.best_streak,
                'badges': st.session_state.badges,
                'join_date': st.session_state.join_date.isoformat()
            }
            json_str = json.dumps(data, indent=2)
            st.download_button(
                "Download JSON",
                data=json_str,
                file_name=f"waterbuddy_{st.session_state.name}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        if st.button("⚙️ Edit Profile", use_container_width=True):
            st.session_state.screen = 'settings'
            st.rerun()
        
        if st.button("📈 View Analytics", use_container_width=True):
            st.session_state.screen = 'charts'
            st.rerun()

def charts_screen():
    """Analytics and charts"""
    
    st.title("📊 Analytics & Charts")
    
    # Weekly chart
    st.markdown("### Weekly Progress")
    weekly_fig = create_weekly_chart()
    st.plotly_chart(weekly_fig, use_container_width=True)
    
    # Stats summary
    col1, col2, col3 = st.columns(3)
    
    weekly_total = sum(d['intake'] for d in st.session_state.weekly_data[:-1])
    weekly_avg = weekly_total / 6 if len(st.session_state.weekly_data) > 1 else 0
    
    with col1:
        st.metric("Weekly Total", f"{weekly_total:,}ml", delta=f"{st.session_state.current_intake}ml today")
    
    with col2:
        st.metric("Weekly Average", f"{int(weekly_avg)}ml")
    
    with col3:
        days_met = sum(1 for d in st.session_state.weekly_data if d['intake'] >= d['goal'])
        st.metric("Goals Met This Week", f"{days_met}/7")
    
    st.divider()
    
    # Intake history
    if st.session_state.intake_history:
        st.markdown("### Recent Activity")
        
        # Show last 10 entries
        recent_entries = sorted(
            st.session_state.intake_history, 
            key=lambda x: x['timestamp'], 
            reverse=True
        )[:10]
        
        for entry in recent_entries:
            st.markdown(f"💧 **{entry['amount']}ml** - {entry['timestamp'].strftime('%I:%M %p')}")
    else:
        st.info("No activity recorded yet. Start logging to see your history!")

def settings_screen():
    """Settings and preferences"""
    
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["Profile", "Notifications", "Preferences"])
    
    with tab1:
        st.markdown("### Profile Settings")
        
        new_name = st.text_input("Name", value=st.session_state.name)
        
        st.write("**Age Group:**")
        age_cols = st.columns(2)
        for idx, (key, value) in enumerate(AGE_GROUPS.items()):
            with age_cols[idx % 2]:
                if st.button(
                    f"{value['icon']} {value['label']}", 
                    key=f"settings_age_{key}",
                    use_container_width=True,
                    type="primary" if st.session_state.age_group == key else "secondary"
                ):
                    st.session_state.age_group = key
                    st.rerun()
        
        new_goal = st.slider(
            "Daily Goal (ml)",
            min_value=1000,
            max_value=4000,
            value=st.session_state.daily_goal,
            step=250
        )
        
        if st.button("Save Profile Changes", use_container_width=True):
            st.session_state.name = new_name
            st.session_state.daily_goal = new_goal
            st.success("Profile updated successfully!")
            st.rerun()
    
    with tab2:
        st.markdown("### Notification Settings")
        
        st.session_state.notifications_enabled = st.checkbox(
            "Enable Notifications",
            value=st.session_state.notifications_enabled
        )
        
        if st.session_state.notifications_enabled:
            st.session_state.notification_frequency = st.slider(
                "Reminder Frequency (minutes)",
                min_value=15,
                max_value=180,
                value=st.session_state.notification_frequency,
                step=15
            )
            
            st.session_state.notification_tone = st.selectbox(
                "Notification Tone",
                options=['gentle', 'cheerful', 'motivational', 'silent'],
                index=['gentle', 'cheerful', 'motivational', 'silent'].index(st.session_state.notification_tone)
            )
        
        st.session_state.sound_enabled = st.checkbox(
            "Enable Sound Effects",
            value=st.session_state.sound_enabled
        )
    
    with tab3:
        st.markdown("### Display Preferences")
        
        st.session_state.high_contrast = st.checkbox(
            "High Contrast Mode",
            value=st.session_state.high_contrast,
            help="Increases contrast for better visibility"
        )
        
        st.session_state.family_mode = st.checkbox(
            "Family/Group Mode",
            value=st.session_state.family_mode,
            help="Enable multiple user profiles"
        )
        
        st.divider()
        
        st.markdown("### Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Data", use_container_width=True):
                data = {
                    'name': st.session_state.name,
                    'age_group': st.session_state.age_group,
                    'daily_goal': st.session_state.daily_goal,
                    'current_intake': st.session_state.current_intake,
                    'total_intake': st.session_state.total_intake,
                    'streak': st.session_state.streak,
                    'badges': st.session_state.badges,
                    'intake_history': [
                        {
                            'timestamp': entry['timestamp'].isoformat(),
                            'amount': entry['amount'],
                            'date': entry['date'].isoformat()
                        }
                        for entry in st.session_state.intake_history
                    ]
                }
                json_str = json.dumps(data, indent=2)
                st.download_button(
                    "Download JSON",
                    data=json_str,
                    file_name=f"waterbuddy_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("Reset All Data", use_container_width=True, type="secondary"):
                if st.checkbox("I confirm I want to reset all data"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.success("Data reset! Reloading...")
                    st.rerun()

def summary_screen():
    """End of day summary"""
    
    st.title("📋 Today's Summary")
    
    mascot = '🎉' if st.session_state.current_intake >= st.session_state.daily_goal else '😊'
    st.markdown(f"<div style='text-align: center; font-size: 6rem;'>{mascot}</div>", unsafe_allow_html=True)
    
    if st.session_state.current_intake >= st.session_state.daily_goal:
        st.success("### Fantastic work today!")
        st.write("You've crushed your hydration goal! 🎯")
    else:
        st.info("### Great progress today!")
        st.write("You've made excellent hydration progress! Keep it up!")
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Today's Intake", f"{st.session_state.current_intake}ml")
    
    with col2:
        progress_pct = int((st.session_state.current_intake / st.session_state.daily_goal) * 100)
        st.metric("Goal Progress", f"{progress_pct}%")
    
    with col3:
        today_glasses = len([e for e in st.session_state.intake_history if e['date'] == date.today()])
        st.metric("Glasses Today", today_glasses)
    
    with col4:
        st.metric("Current Streak", f"{st.session_state.streak} days")
    
    st.divider()
    
    # Progress visualization
    progress_pct = (st.session_state.current_intake / st.session_state.daily_goal) * 100
    ring_fig = create_progress_ring(progress_pct)
    st.plotly_chart(ring_fig, use_container_width=True)

def leaderboard_screen():
    """Leaderboard for family/group mode"""
    
    st.title("🏆 Leaderboard")
    
    if not st.session_state.family_mode:
        st.info("Enable Family/Group mode in Settings to view the leaderboard!")
        return
    
    st.markdown("### Today's Standings")
    
    # Sort by intake
    sorted_users = sorted(st.session_state.leaderboard_users, key=lambda x: x.get('intake', 0), reverse=True)
    
    # Display leaderboard
    for idx, user in enumerate(sorted_users):
        position_emoji = {0: '🥇', 1: '🥈', 2: '🥉'}.get(idx, f"{idx + 1}.")
        
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        
        with col1:
            st.markdown(f"### {position_emoji}")
        
        with col2:
            is_current_user = user.get('name') == st.session_state.name or user.get('name') == 'You'
            name_display = f"**{user.get('name', 'Unknown')}**" if is_current_user else user.get('name', 'Unknown')
            st.markdown(f"### {name_display}")
        
        with col3:
            st.metric("Intake", f"{user.get('intake', 0)}ml")
        
        with col4:
            st.metric("Streak", f"{user.get('streak', 0)} days")
        
        st.divider()
    
    # Streak leaderboard
    st.markdown("### Longest Streaks")
    sorted_by_streak = sorted(st.session_state.leaderboard_users, key=lambda x: x.get('streak', 0), reverse=True)
    
    cols = st.columns(min(len(sorted_by_streak), 4))
    for idx, user in enumerate(sorted_by_streak[:4]):
        with cols[idx]:
            st.markdown(f"""
            <div class='stat-card'>
                <div style='font-size: 2.5rem;'>🔥</div>
                <div style='font-weight: 700; margin-top: 0.5rem;'>{user.get('name', 'Unknown')}</div>
                <div style='font-size: 2rem; font-weight: 800; margin: 0.5rem 0;'>{user.get('streak', 0)}</div>
                <div style='opacity: 0.85;'>days</div>
            </div>
            """, unsafe_allow_html=True)

def help_screen():
    """Help and tutorial screen"""
    
    st.title("❓ Help & Tutorial")
    
    tab1, tab2, tab3 = st.tabs(["Getting Started", "Features Guide", "FAQ"])
    
    with tab1:
        st.markdown("""
        ## Welcome to WaterBuddy! 💧
        
        ### Quick Start Guide
        
        **1. Log Your Water Intake** 🥤
        - Use the dashboard buttons to log different drink sizes
        - Choose from: Glass (250ml), Can (330ml), Bottle (500ml), or Large Bottle (750ml)
        - Or enter a custom amount
        
        **2. Track Your Progress** 📊
        - Watch the bottle fill up as you drink
        - Your mascot buddy gets happier as you progress
        - See your progress percentage in real-time
        
        **3. Build Your Streak** 🔥
        - Log water every day to maintain your streak
        - Reach your daily goal to keep the streak alive
        - Compete with yourself or family members
        
        **4. Earn Badges** 🏆
        - Complete challenges to unlock achievements
        - Each badge represents a milestone
        - Collect them all!
        
        **5. View Analytics** 📈
        - Check your weekly progress
        - See patterns in your hydration
        - Optimize your water drinking schedule
        """)
        
        st.success("💡 Pro Tip: Log water regularly throughout the day for best results!")
    
    with tab2:
        st.markdown("""
        ## Features Guide
        
        ### 🏠 Dashboard
        - **Main hub** for logging water intake
        - View today's progress and goals
        - Quick access to intake buttons
        - See current streak and badges
        - Get daily hydration tips
        
        ### 👤 Profile
        - View your **lifetime statistics**
        - See all earned badges
        - Check current and best streak
        - View achievement completion rate
        
        ### 📊 Analytics
        - **Weekly progress chart** showing daily intake
        - Compare against your goal
        - View recent activity history
        - Track weekly averages and totals
        
        ### 🏆 Leaderboard
        - Available in **Family/Group mode**
        - See rankings by daily intake
        - View longest streaks
        - Friendly competition with family
        
        ### 📋 Summary
        - **End-of-day review**
        - See today's achievements
        - Progress visualization
        - Goal completion status
        
        ### ⚙️ Settings
        - **Customize your profile**
        - Adjust daily goal
        - Change age group
        - Configure notifications
        - Enable high contrast mode
        - Export/import data
        """)
    
    with tab3:
        st.markdown("""
        ## Frequently Asked Questions
        
        ### General
        
        **Q: Is my data safe and private?**  
        A: Yes! All data is stored locally in your browser session. We don't collect or send any personal information to external servers.
        
        **Q: Can I use this on my phone?**  
        A: Absolutely! WaterBuddy works great on mobile browsers. Just bookmark the page for quick access.
        
        **Q: How do I save my progress?**  
        A: Use the "Export Data" feature in Settings to download your progress as a JSON file.
        
        ### Tracking
        
        **Q: What if I forget to log my water?**  
        A: You can add it anytime during the day. Try to log regularly for the most accurate tracking.
        
        **Q: What happens at midnight?**  
        A: The app automatically resets your daily intake at midnight and updates your streak.
        
        ### Goals & Streaks
        
        **Q: How is my streak calculated?**  
        A: You maintain your streak by reaching your daily goal each day. Missing a day resets it to 0.
        
        **Q: Can I change my daily goal?**  
        A: Yes! Go to Settings → Profile to adjust your goal anytime.
        
        **Q: What's a good daily water goal?**  
        A: Generally 2000-2500ml for adults, but this varies by age, activity level, and climate.
        
        ### Badges
        
        **Q: How do I earn badges?**  
        A: Badges are earned automatically by completing specific challenges (first glass, daily goals, streaks, etc.).
        
        ### Family Mode
        
        **Q: How does Family Mode work?**  
        A: Enable it in Settings to view a leaderboard. Each family member should use their own profile or browser session.
        """)
        
        st.divider()
        
        st.info("📧 Still have questions? Open an issue on GitHub or reach out to the community!")

def reminders_screen():
    """Smart reminder system"""
    
    st.title("⏰ Smart Reminders")
    
    st.markdown("### Reminder Settings")
    
    # Check if it's time for a reminder
    if st.session_state.notifications_enabled:
        time_since_last = (datetime.now() - st.session_state.last_reminder_time).total_seconds() / 60
        
        if time_since_last >= st.session_state.notification_frequency:
            st.warning("💧 Time for your next glass of water!")
            st.session_state.last_reminder_time = datetime.now()
    
    # Reminder schedule
    st.markdown("### Today's Reminder Schedule")
    
    reminder_times = []
    start_hour = 7
    end_hour = 22
    frequency_hours = st.session_state.notification_frequency / 60
    
    current_hour = start_hour
    while current_hour < end_hour:
        reminder_times.append(f"{int(current_hour):02d}:{int((current_hour % 1) * 60):02d}")
        current_hour += frequency_hours
    
    cols = st.columns(min(len(reminder_times), 5))
    for idx, time_str in enumerate(reminder_times):
        with cols[idx % 5]:
            st.markdown(f"""
            <div class='stat-card'>
                <div style='font-size: 2.5rem;'>⏰</div>
                <div style='font-weight: 700; font-size: 1.2rem; margin-top: 0.5rem;'>{time_str}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Motivational quotes
    quotes = {
        'children': [
            "Water makes you grow big and strong! 💪",
            "Drink up, champion! You're doing great! 🌟",
            "Your body loves water - keep it happy! 😊"
        ],
        'teen': [
            "Stay hydrated, stay focused! 🎯",
            "Water = Better performance! 💯",
            "Keep crushing it - one glass at a time! 🔥"
        ],
        'adult': [
            "Hydration boosts productivity and focus. 💼",
            "Water: Your secret weapon for success. 🎯",
            "Stay sharp. Stay hydrated. ⚡"
        ],
        'senior': [
            "Gentle reminder: Time for your water break! 🌸",
            "Stay refreshed and healthy! 🌿",
            "Your wellness matters - drink up! ✨"
        ]
    }
    
    import random
    age_group = st.session_state.age_group
    quote = random.choice(quotes[age_group])
    
    st.info(quote)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point"""
    
    # Initialize session state
    init_session_state()
    
    # Apply custom styling
    apply_custom_css()
    
    # Show onboarding or main app
    if st.session_state.show_onboarding:
        if st.session_state.screen == 'splash':
            splash_screen()
        else:
            onboarding_screen()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown("### 💧 WaterBuddy")
            st.caption(f"Hello, {st.session_state.name}!")
            
            st.divider()
            
            # Navigation menu
            menu_items = {
                'dashboard': {'label': '🏠 Dashboard', 'icon': '🏠'},
                'profile': {'label': '👤 Profile', 'icon': '👤'},
                'charts': {'label': '📊 Analytics', 'icon': '📊'},
                'leaderboard': {'label': '🏆 Leaderboard', 'icon': '🏆'},
                'reminders': {'label': '⏰ Reminders', 'icon': '⏰'},
                'summary': {'label': '📋 Summary', 'icon': '📋'},
                'help': {'label': '❓ Help', 'icon': '❓'},
                'settings': {'label': '⚙️ Settings', 'icon': '⚙️'}
            }
            
            for key, item in menu_items.items():
                if st.button(item['label'], key=f"nav_{key}", use_container_width=True):
                    st.session_state.screen = key
                    st.rerun()
            
            st.divider()
            
            # Quick stats in sidebar
            st.markdown("### Today")
            st.metric("Intake", f"{st.session_state.current_intake}ml")
            st.metric("Goal", f"{st.session_state.daily_goal}ml")
            progress_pct = (st.session_state.current_intake / st.session_state.daily_goal) * 100
            st.progress(min(progress_pct / 100, 1.0))
            
            st.divider()
            
            st.caption("🔒 Privacy-first hydration tracking")
            st.caption("Your data stays on your device")
        
        # Main content area
        if st.session_state.screen == 'dashboard':
            dashboard_screen()
        elif st.session_state.screen == 'profile':
            profile_screen()
        elif st.session_state.screen == 'charts':
            charts_screen()
        elif st.session_state.screen == 'leaderboard':
            leaderboard_screen()
        elif st.session_state.screen == 'reminders':
            reminders_screen()
        elif st.session_state.screen == 'summary':
            summary_screen()
        elif st.session_state.screen == 'help':
            help_screen()
        elif st.session_state.screen == 'settings':
            settings_screen()

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
