"""
WaterBuddy – Age-Adaptive Hydration Tracking App
Single-file Streamlit version with local CSV persistence
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date, time as dtime
import json
from typing import List, Dict
import base64
import os

# ------------------------------------------------------------------
# CONFIG & CONSTANTS
# ------------------------------------------------------------------
CSV_FILE = "waterbuddy_data.csv"          # local storage
AGE_GROUPS = {
    'children': {'label': 'Kids (2-12)', 'icon': '🌈', 'min': 2, 'max': 12},
    'teen': {'label': 'Teens (13-18)', 'icon': '🧑‍🎓', 'min': 13, 'max': 18},
    'adult': {'label': 'Adults (19-64)', 'icon': '👨‍💼', 'min': 19, 'max': 64},
    'senior': {'label': 'Seniors (65+)', 'icon': '👴', 'min': 65, 'max': 120}
}
BADGES = { ... }  # (unchanged – paste your original dict here)
COLORS = { ... }  # (unchanged)
AGE_THEME_COLORS = { ... }  # (unchanged)
WATER_SIZES = [ ... ]  # (unchanged)
MASCOT_EXPRESSIONS = { ... }  # (unchanged)

# ------------------------------------------------------------------
# CSV I/O  (NEW)
# ------------------------------------------------------------------
def init_csv():
    """Create empty CSV if it does not exist."""
    if not os.path.exists(CSV_FILE):
        pd.DataFrame(columns=["user", "amount", "timestamp", "date"]).to_csv(CSV_FILE, index=False)

def append_intake_to_csv(user: str, amount: int, ts: datetime):
    """Append a single water log to CSV."""
    init_csv()
    df = pd.DataFrame([{
        "user": user,
        "amount": amount,
        "timestamp": ts.isoformat(),
        "date": ts.date().isoformat()
    }])
    df.to_csv(CSV_FILE, mode="a", header=False, index=False)

def load_csv() -> pd.DataFrame:
    """Return pandas DF of all logs."""
    init_csv()
    return pd.read_csv(CSV_FILE, parse_dates=["timestamp", "date"])

def today_intake_from_csv(user: str) -> int:
    """Sum of today’s intake for a user."""
    df = load_csv()
    today = date.today()
    return df[(df.user == user) & (df.date == today)]["amount"].sum()

def weekly_df_for_charts(user: str) -> pd.DataFrame:
    """Return 7-row DF (day, intake, goal) for Plotly."""
    df = load_csv()
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday
    days = pd.date_range(week_start, week_start + timedelta(days=6))
    goal = st.session_state.daily_goal
    res = []
    for d in days:
        day_str = d.strftime("%a")
        intake = df[(df.user == user) & (df.date == d.date())]["amount"].sum()
        res.append({"day": day_str, "intake": int(intake), "goal": goal})
    return pd.DataFrame(res)

def leaderboard_df() -> pd.DataFrame:
    """Build leaderboard DF from CSV (last 24 h intake + best streak)."""
    df = load_csv()
    today = date.today()
    users = df["user"].unique().tolist()
    if not users:
        users = [st.session_state.name or "You"]
    rows = []
    for u in users:
        last24 = df[(df.user == u) & (df.date >= today)]["amount"].sum()
        streak = compute_streak_for_user(u)
        rows.append({"name": u, "intake": int(last24), "streak": streak})
    return pd.DataFrame(rows).sort_values("intake", ascending=False)

def compute_streak_for_user(user: str) -> int:
    """Compute current streak for a user from CSV."""
    df = load_csv()
    dfu = df[df.user == user].copy()
    if dfu.empty:
        return 0
    dfu = dfu.groupby("date")["amount"].sum().reset_index()
    dfu["met"] = dfu["amount"] >= st.session_state.daily_goal
    dfu["date"] = pd.to_datetime(dfu["date"])
    dfu = dfu.sort_values("date", ascending=False)
    streak = 0
    for _, row in dfu.iterrows():
        if row["met"]:
            streak += 1
        else:
            break
    return streak

# ------------------------------------------------------------------
# SESSION-STATE HELPERS  (tweaked)
# ------------------------------------------------------------------
def init_session_state():
    # ---- user profile ----
    for k, default in [
        ("name", ""),
        ("age_group", "adult"),
        ("daily_goal", 2000),
        ("join_date", datetime.now().date()),
    ]:
        if k not in st.session_state:
            st.session_state[k] = default

    # ---- today’s intake / streak ----
    if "current_intake" not in st.session_state:
        st.session_state.current_intake = today_intake_from_csv(st.session_state.name or "You")
    if "streak" not in st.session_state:
        st.session_state.streak = compute_streak_for_user(st.session_state.name or "You")
    if "best_streak" not in st.session_state:
        st.session_state.best_streak = st.session_state.streak

    # ---- gamification ----
    for k, default in [
        ("badges", []),
        ("total_intake", 0),
        ("total_glasses", 0),
        ("last_drink", None),
    ]:
        if k not in st.session_state:
            st.session_state[k] = default

    # ---- UI ----
    if "screen" not in st.session_state:
        st.session_state.screen = "dashboard" if st.session_state.name else "splash"
    if "show_onboarding" not in st.session_state:
        st.session_state.show_onboarding = not st.session_state.name
    if "today_date" not in st.session_state:
        st.session_state.today_date = date.today()

    # ---- settings ----
    for k, default in [
        ("notifications_enabled", True),
        ("notification_frequency", 60),
        ("notification_tone", "gentle"),
        ("sound_enabled", True),
        ("high_contrast", False),
        ("family_mode", False),
    ]:
        if k not in st.session_state:
            st.session_state[k] = default

# ------------------------------------------------------------------
# LOG WATER  (tweaked – writes to CSV)
# ------------------------------------------------------------------
def add_water_intake(amount: int):
    user = st.session_state.name or "You"
    ts = datetime.now()
    append_intake_to_csv(user, amount, ts)

    # update session mirrors
    st.session_state.current_intake += amount
    st.session_state.total_intake += amount
    st.session_state.total_glasses += 1
    st.session_state.last_drink = ts

    # badges
    if "first-glass" not in st.session_state.badges and st.session_state.total_glasses == 1:
        st.session_state.badges.append("first-glass")
        st.success("🌟 Badge Earned: First Splash!")
    if st.session_state.current_intake >= st.session_state.daily_goal:
        if "daily-goal" not in st.session_state.badges:
            st.session_state.badges.append("daily-goal")
        st.balloons()
        st.success("🎉 Goal achieved!")
    # (add more badge checks as desired)

# ------------------------------------------------------------------
# STREAK LOGIC  (bug-fixed)
# ------------------------------------------------------------------
def check_streak():
    """Midnight rollover: update streak only if yesterday was met."""
    today = date.today()
    if st.session_state.today_date == today:
        return
    yesterday = today - timedelta(days=1)
    yesterday_met = (
        load_csv()
        .query("user == @st.session_state.name and date == @yesterday")
        ["amount"]
        .sum()
        >= st.session_state.daily_goal
    )
    if yesterday_met:
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
    else:
        st.session_state.streak = 0
    st.session_state.today_date = today
    st.session_state.current_intake = 0  # reset for new day

# ------------------------------------------------------------------
# VISUAL COMPONENTS  (unchanged – paste your originals here)
# ------------------------------------------------------------------
def create_weekly_chart():
    age_colors = AGE_THEME_COLORS[st.session_state.age_group]
    df = weekly_df_for_charts(st.session_state.name or "You")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.day, y=df.goal, mode='lines', name='Goal', line=dict(dash='dash')))
    fig.add_trace(go.Bar(x=df.day, y=df.intake, name='Intake'))
    fig.update_layout(title="Weekly Hydration Progress", xaxis_title="Day", yaxis_title="Water (ml)", height=400)
    return fig

# ------------------------------------------------------------------
# SCREEN FUNCTIONS  (unchanged – paste your originals here)
# ------------------------------------------------------------------
def dashboard_screen():
    check_streak()
    st.title(get_age_specific_message('greeting'))
    # ... (rest of your dashboard code – no changes needed except call create_weekly_chart() above)

# ------------------------------------------------------------------
# MAIN APP  (unchanged flow)
# ------------------------------------------------------------------
def main():
    init_session_state()
    apply_custom_css()  # paste your original CSS helper here

    if st.session_state.show_onboarding:
        onboarding_screen()  # paste your original
    else:
        with st.sidebar:
            st.markdown("### 💧 WaterBuddy")
            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.screen = "dashboard"
            if st.button("👤 Profile", use_container_width=True):
                st.session_state.screen = "profile"
            if st.button("📊 Analytics", use_container_width=True):
                st.session_state.screen = "charts"
            if st.button("🏆 Leaderboard", use_container_width=True):
                st.session_state.screen = "leaderboard"
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.screen = "settings"

        if st.session_state.screen == "dashboard":
            dashboard_screen()
        elif st.session_state.screen == "profile":
            profile_screen()
        elif st.session_state.screen == "charts":
            charts_screen()
        elif st.session_state.screen == "leaderboard":
            leaderboard_screen()
        elif st.session_state.screen == "settings":
            settings_screen()

if __name__ == "__main__":
    main()
