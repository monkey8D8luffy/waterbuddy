# WaterBuddy - Streamlit Version

A comprehensive, age-adaptive hydration tracking application built with Python and Streamlit.

## Features

### Core Functionality
- **Water Intake Tracking**: Log water consumption with preset sizes or custom amounts
- **Daily Goals**: Set and track personalized daily hydration goals
- **Progress Visualization**: Real-time progress bars, bottle fill animations, and circular gauges
- **History Tracking**: View detailed intake history and patterns

### Age-Adaptive Design
The app automatically adjusts its design for four age groups:
- **Children (2-12)**: Playful colors, larger fonts, rounded corners
- **Teens (13-18)**: Sleek design with gamification elements
- **Adults (19-64)**: Clean, minimal professional interface
- **Seniors (65+)**: High contrast, larger text, simplified layout

### Gamification
- **Badges & Achievements**: Earn badges for milestones
- **Streak Tracking**: Maintain daily consistency
- **Leaderboard Ready**: Track personal bests
- **Celebration Effects**: Visual feedback for achievements

### Accessibility
- **High Contrast Mode**: For improved visibility
- **Adjustable Font Sizes**: Based on age group
- **Simple Navigation**: Easy-to-use sidebar menu
- **Privacy-First**: All data stored locally in session

## Installation & Running Locally

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone or download this repository**
   ```bash
   cd waterbuddy-streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open in browser**
   The app will automatically open at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Quick Deploy (Recommended)

1. **Push code to GitHub**
   - Create a new GitHub repository
   - Push `streamlit_app.py` and `requirements.txt` to the repository

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Main file: `streamlit_app.py`
   - Click "Deploy"

### Manual Deploy Steps

1. **Create Streamlit Cloud Account**
   - Visit [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign up with GitHub

2. **Connect Repository**
   - Link your GitHub account
   - Select the repository containing WaterBuddy

3. **Configure Deployment**
   ```
   Main file path: streamlit_app.py
   Python version: 3.9
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (usually 2-3 minutes)
   - Your app will be available at a public URL

## Alternative Deployment Options

### Heroku

1. **Create Procfile**
   ```
   web: streamlit run streamlit_app.py --server.port $PORT
   ```

2. **Deploy**
   ```bash
   heroku create your-waterbuddy-app
   git push heroku main
   ```

### Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY streamlit_app.py .
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t waterbuddy .
   docker run -p 8501:8501 waterbuddy
   ```

### AWS/GCP/Azure

Deploy using standard Python web app deployment methods. Streamlit works on any platform that supports Python web applications.

## Usage Guide

### First Time Setup

1. **Onboarding**
   - Enter your name
   - Select your age group
   - Set daily hydration goal
   - Enable family mode (optional)

2. **Dashboard**
   - View today's progress
   - Log water intake using quick buttons
   - Track your streak and badges

### Daily Usage

1. **Log Water**
   - Click quick action buttons (Glass, Bottle, etc.)
   - Or use custom amount for precise tracking

2. **View Progress**
   - Check dashboard for real-time progress
   - View bottle fill visualization
   - Monitor streak counter

3. **Analytics**
   - Navigate to Charts screen
   - View weekly progress
   - Analyze patterns

### Profile Management

1. **View Profile**
   - See all earned badges
   - Check lifetime statistics
   - View progress rings

2. **Settings**
   - Adjust age group and goals
   - Configure notifications
   - Enable high contrast mode
   - Export or reset data

## Features by Screen

### 🏠 Dashboard
- Real-time progress tracking
- Water logging buttons
- Quick stats (streak, badges, last drink)
- Mascot with mood expressions
- Custom amount input

### 👤 Profile
- Personal information
- Lifetime statistics
- Badge showcase
- Progress ring visualization
- Member since date

### 📊 Analytics
- Weekly intake chart
- Goal achievement tracking
- Recent activity log
- Statistical summaries

### 📋 Summary
- End of day review
- Achievement celebrations
- Progress metrics
- Visual progress indicators

### ⚙️ Settings
- Profile customization
- Notification preferences
- Display options
- Data management (export/reset)

## Customization

### Color Themes
Each age group has unique colors defined in `AGE_THEME_COLORS`:
- Children: Pink, Yellow, Teal
- Teen: Purple, Orange, Red
- Adult: Aqua, Teal, Coral
- Senior: Teal, Coral, Aqua

### Font Sizes
Automatically adjusted by age group:
- Children: 18px
- Teen: 16px
- Adult: 16px
- Senior: 20px

### Border Radius
Age-appropriate rounding:
- Children: 1.5rem (very rounded)
- Teen: 0.75rem (slightly rounded)
- Adult: 0.5rem (minimal rounding)
- Senior: 1rem (moderate rounding)

## Data Privacy

- **Local Storage**: All data stored in Streamlit session state
- **No Backend**: No external database or API calls
- **Export Option**: Download your data anytime
- **Reset Option**: Clear all data when needed

## Technical Details

### Architecture
- **Frontend**: Streamlit Python framework
- **Visualizations**: Plotly for interactive charts
- **State Management**: Streamlit session_state
- **Styling**: Custom CSS injected via st.markdown

### Performance
- Lightweight and fast
- Minimal dependencies
- Efficient state management
- Optimized reruns

### Browser Support
Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## Troubleshooting

### App won't start
- Check Python version (3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Clear cache: `streamlit cache clear`

### Styles not appearing
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Clear browser cache
- Check browser console for errors

### Data not saving
- Data is session-based; will reset on page refresh
- Use "Export Data" to save permanently
- For persistent storage, implement database backend

### Deployment issues
- Ensure `requirements.txt` is in root directory
- Check Streamlit Cloud logs for errors
- Verify Python version compatibility

## Future Enhancements

Potential features to add:
- Database integration for persistent storage
- Multi-user support with authentication
- Social features and challenges
- Mobile app version
- Apple Health / Google Fit integration
- Advanced analytics and insights
- Reminder notifications
- Dark mode toggle
- Multiple language support

## Support

For issues or questions:
1. Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
2. Review Plotly docs: [plotly.com/python](https://plotly.com/python)
3. Open an issue on GitHub

## License

This project is open source and available for personal and educational use.

## Credits

- Built with [Streamlit](https://streamlit.io)
- Charts powered by [Plotly](https://plotly.com)
- Inspired by the original React version of WaterBuddy

---

**Happy Hydrating! 💧**
