# 💧 WaterBuddy - Age-Adaptive Hydration Tracking App

<div align="center">

![WaterBuddy Banner](https://img.shields.io/badge/WaterBuddy-💧-70D6FF?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)


**A next-generation hydration companion that adapts to your age group** 🌈

[Quick Start](#-quick-start) • [Features](#-features) • [Deploy](#-deployment) • [Documentation](#-documentation)

</div>

---

## 🌟 Overview

WaterBuddy is a comprehensive hydration tracking application built with Python and Streamlit. It features age-adaptive design, gamification, smart reminders, and beautiful visualizations to help you stay hydrated throughout the day.

**What makes WaterBuddy special?**
- 🎨 **Age-Adaptive Design** - Automatically adjusts for children, teens, adults, and seniors
- 🏆 **Gamification** - Earn badges, maintain streaks, compete with family
- 📊 **Beautiful Visualizations** - Animated bottle fills, progress rings, weekly charts
- ♿ **Accessibility First** - High contrast mode, adjustable fonts, screen reader friendly
- 🔒 **Privacy-Focused** - All data stays local, no cloud storage required
- 🚀 **Easy Deployment** - Deploy to Streamlit Cloud in minutes (FREE!)

---

## 🎯 Features

### Core Functionality

✅ **Smart Water Logging**
- Quick buttons: Glass (250ml), Can (330ml), Bottle (500ml), Large Bottle (750ml)
- Custom amount input (1-2000ml)
- Real-time progress tracking
- Intake history with timestamps

✅ **Age-Adaptive Themes**
Four distinct designs that automatically adjust:
- **Children (2-12)**: Playful colors, large fonts, rounded corners
- **Teens (13-18)**: Sleek design, modern aesthetic, gamification focus
- **Adults (19-64)**: Clean, minimal, professional interface
- **Seniors (65+)**: High contrast, larger text (20px), simplified layout

✅ **Gamification System**
- 9 unique badges to earn
- Streak tracking (current & best)
- Daily goal achievements
- Celebration effects
- Leaderboard (family mode)

✅ **Comprehensive Analytics**
- Weekly progress charts
- Daily/weekly/lifetime statistics
- Activity history
- Goal tracking
- Performance insights

✅ **Accessibility Features**
- High contrast mode toggle
- Age-appropriate font sizing
- Keyboard navigation
- Screen reader support
- Mobile responsive

✅ **Family/Group Mode**
- Multiple user profiles
- Leaderboard with rankings
- Friendly competition
- Individual stats tracking

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install streamlit plotly
```

### 2. Run the App

```bash
streamlit run streamlit_app.py
```

### 3. Open Browser

The app automatically opens at `http://localhost:8501` 🎉

---

## 📦 Installation Options

### Option A: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/waterbuddy.git
cd waterbuddy

# Run setup script
python setup.py
```

The setup script will:
- ✅ Check Python version
- ✅ Install dependencies
- ✅ Verify files
- ✅ Launch the app

### Option B: Manual Setup

```bash
# Install requirements
pip install -r requirements.txt

# Run app
streamlit run streamlit_app.py
```

### Option C: Docker

```bash
# Build image
docker build -t waterbuddy .

# Run container
docker run -p 8501:8501 waterbuddy

# Access at http://localhost:8501
```

---

## 🌈 Age Group Themes

### 👶 Children (2-12)
```
Colors: Playful Pink (#FF6B9D), Sunshine Yellow (#FFE66D)
Fonts: 18px, rounded, friendly
Style: Rounded corners (1.5rem), bright & cheerful
Features: Simple language, fun mascot, colorful badges
```

### 🧑‍🎓 Teens (13-18)
```
Colors: Electric Purple (#7C3AED), Neon Orange (#F59E0B)
Fonts: 16px, modern, sleek
Style: Sharp corners (0.75rem), gradient effects
Features: Streak focus, social elements, achievements
```

### 👨‍💼 Adults (19-64)
```
Colors: Aqua (#70D6FF), Deep Teal (#1E9BC7)
Fonts: 16px, clean, professional
Style: Minimal corners (0.5rem), sophisticated
Features: Productivity focus, analytics, insights
```

### 👴 Seniors (65+)
```
Colors: Calming Teal (#1E9BC7), Soft Coral (#FFB3A7)
Fonts: 20px, clear, readable
Style: Gentle curves (1rem), high contrast
Features: Larger buttons, simplified UI, health focus
```

---

## 🏆 Badge System

Earn achievements as you track your hydration:

| Badge | Name | Requirement |
|-------|------|-------------|
| 🌟 | First Splash | Log your first glass |
| 🎯 | Daily Champion | Reach daily goal |
| 🔥 | Week Warrior | 7-day streak |
| ⚡ | Consistency King | 10-day streak |
| 🏆 | Monthly Master | 30-day streak |
| 💪 | Hydration Hero | Log 100 glasses |
| 🌅 | Early Bird | Morning hydration |
| 🦉 | Night Owl | Evening hydration |
| 🚀 | Overachiever | 150% of goal |

---

## 📊 Screenshots


<img width="555" height="903" alt="image" src="https://github.com/user-attachments/assets/c72152b7-6d03-4ae2-bf20-6a7e3ad5af85" />


---

## 🚢 Deployment

### Streamlit Cloud (FREE, Recommended)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "WaterBuddy Streamlit app"
git remote add origin https://github.com/yourusername/waterbuddy.git
git push -u origin main

# 2. Deploy
# Visit share.streamlit.io
# Sign in with GitHub
# Select your repository
# Click "Deploy"

# 3. Done!
# Your app is live at: yourusername-waterbuddy.streamlit.app
```

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions**

### Other Deployment Options
- Heroku (Free tier available)
- Docker (AWS, GCP, Azure, DigitalOcean)
- PythonAnywhere
- See full deployment guide for more options

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Get started in 2 minutes |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Complete deployment instructions |
| [README_STREAMLIT.md](README_STREAMLIT.md) | Detailed Streamlit documentation |
| [CONVERSION_SUMMARY.md](CONVERSION_SUMMARY.md) | React to Streamlit conversion details |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | Migrate from React version |

---

## 🛠️ Tech Stack

**Frontend Framework**
- [Streamlit](https://streamlit.io) - Python web framework

**Visualizations**
- [Plotly](https://plotly.com) - Interactive charts
- Custom SVG animations

**Styling**
- Custom CSS with age-adaptive themes
- SVG graphics for mascot & bottle

**State Management**
- Streamlit Session State

**Data Format**
- JSON for export/import

---

## 📋 Requirements

**System Requirements**
- Python 3.8 or higher
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

**Python Packages**
```
streamlit>=1.28.0
plotly>=5.17.0
```

Optional:
```
pandas>=2.0.0
numpy>=1.24.0
```

---

## 🎮 Usage Guide

### First Time Setup

1. **Launch the app** - Run `streamlit run streamlit_app.py`
2. **Create profile** - Enter name, select age group, set daily goal
3. **Start tracking** - Click water buttons to log intake
4. **Watch progress** - See bottle fill and progress bar update
5. **Earn badges** - Complete challenges to unlock achievements
6. **View analytics** - Check weekly charts and statistics

### Daily Workflow

1. **Morning** - Open app, set goal if needed
2. **Throughout day** - Log water after drinking
3. **Check progress** - View dashboard to stay on track
4. **Evening** - Review summary, check streak
5. **Repeat** - Come back tomorrow to maintain streak!

### Tips for Success

✅ Log water immediately after drinking  
✅ Set realistic daily goals  
✅ Enable reminders to stay consistent  
✅ Check analytics to optimize timing  
✅ Use family mode for accountability  
✅ Export data regularly as backup  

---

## 🔧 Configuration

### Theme Customization

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#70D6FF"
backgroundColor = "#FFF7EE"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#123743"
font = "sans serif"
```

### App Settings

Within the app:
- Settings → Profile (adjust goals, age group)
- Settings → Notifications (reminder frequency, tones)
- Settings → Preferences (high contrast, family mode)






<div align="center">

**Made with 💙 and 💧 by the WaterBuddy Team**

[Website](https://yourusername-waterbuddy.streamlit.app) • [GitHub](https://github.com/yourusername/waterbuddy) • [Documentation](./docs)

**Stay Hydrated! 💧**

</div>
