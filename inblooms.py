import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import random
from wordcloud import WordCloud
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import base64
from io import BytesIO
import datetime
import altair as alt
import zipfile

# Force dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #262730;
    }

    /* Tables */
    .stDataFrame {
        background-color: #1F2937;
    }

    /* DataTable background and text */
    .dataframe {
        background-color: #1F2937;
        color: #FAFAFA;
    }

    /* Table cells */
    .dataframe td, .dataframe th {
        background-color: #1F2937 !important;
        color: #FAFAFA !important;
    }

    /* Table header */
    .dataframe thead th {
        background-color: #374151 !important;
        color: #FAFAFA !important;
    }

    /* Table hover */
    .dataframe tr:hover {
        background-color: #374151 !important;
    }

    /* Pagination buttons */
    .st-emotion-cache-1y4p8pa {
        background-color: #1F2937;
        color: #FAFAFA;
    }

    /* Inputs and selectboxes */
    .stSelectbox, .stTextInput {
        background-color: #1F2937;
        color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)

# Set page config with dark theme
st.set_page_config(
    page_title="InBloom '25",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Define color scheme
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#1E88E5"
ACCENT_COLOR = "#FF5722"
BG_COLOR = "#f9f9f9"
CARD_BG_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
MUTED_TEXT = "#6c757d"

# Custom CSS for styling with enhanced aesthetics
custom_css = f"""
<style>
    /* Main container styling */
    .main {{
        padding: 1.5rem;
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Custom title styling */
    .title-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, {PRIMARY_COLOR}22, {SECONDARY_COLOR}22);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    
    .title-text {{
        color: {PRIMARY_COLOR};
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        background: linear-gradient(90deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }}
    
    /* Section headers */
    .section-header {{
        color: {PRIMARY_COLOR};
        font-size: 2rem;
        font-weight: 600;
        padding: 0.75rem 1.25rem;
        margin: 1.5rem 0 1rem 0;
        border-radius: 8px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}22, transparent);
        display: inline-block;
        position: relative;
    }}
    
    .section-header::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, transparent);
    }}
    
    /* Dashboard metrics */
    .metric-card {{
        background-color: {CARD_BG_COLOR};
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid {PRIMARY_COLOR};
        margin: 0.75rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }}
    
    /* Beautified metrics */
    .metrics-container {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 20px;
    }}
    
    .metric-box {{
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }}
    
    .metric-box:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }}
    
    .metric-box h3 {{
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 12px;
    }}
    
    .metric-box h2 {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .metric-box p {{
        margin-top: 8px;
        color: {MUTED_TEXT};
        font-size: 0.9rem;
    }}
    
    .blue-metric {{
        background: linear-gradient(135deg, #e6f2ff, #ffffff);
        border-bottom: 4px solid {SECONDARY_COLOR};
    }}
    
    .blue-metric h3 {{
        color: {SECONDARY_COLOR};
    }}
    
    .green-metric {{
        background: linear-gradient(135deg, #e6fff2, #ffffff);
        border-bottom: 4px solid {PRIMARY_COLOR};
    }}
    
    .green-metric h3 {{
        color: {PRIMARY_COLOR};
    }}
    
    .orange-metric {{
        background: linear-gradient(135deg, #fff2e6, #ffffff);
        border-bottom: 4px solid {ACCENT_COLOR};
    }}
    
    .orange-metric h3 {{
        color: {ACCENT_COLOR};
    }}
    
    /* Table styling */
    .styled-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 20px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    
    .styled-table thead th {{
        background-color: {PRIMARY_COLOR};
        color: white;
        font-weight: 600;
        text-align: left;
        padding: 12px 15px;
    }}
    
    .styled-table tbody tr {{
        border-bottom: 1px solid #dddddd;
        transition: background-color 0.3s;
    }}
    
    .styled-table tbody tr:nth-of-type(even) {{
        background-color: #f3f3f3;
    }}
    
    .styled-table tbody tr:last-of-type {{
        border-bottom: 2px solid {PRIMARY_COLOR};
    }}
    
    .styled-table tbody tr:hover {{
        background-color: #e6f7ff;
    }}
    
    .styled-table td {{
        padding: 12px 15px;
    }}
    
    /* Sidebar styling */
    .sidebar-content {{
        padding: 1rem;
        background: linear-gradient(180deg, #ffffff 0%, #f5f7fa 100%);
        border-radius: 8px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.03);
    }}
    
    /* Filter sections in sidebar */
    .filter-section {{
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #eaeaea;
    }}
    
    .filter-label {{
        color: {PRIMARY_COLOR};
        font-weight: 600;
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
    }}
    
    .filter-label svg {{
        margin-right: 8px;
    }}
    
    /* Custom buttons */
    .custom-button {{
        display: inline-block;
        padding: 10px 20px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, {PRIMARY_COLOR}dd);
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-decoration: none;
        margin: 10px 0;
    }}
    
    .custom-button:hover {{
        background: linear-gradient(90deg, {PRIMARY_COLOR}dd, {PRIMARY_COLOR});
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        background-color: #f5f5f5;
        border: none;
        color: {TEXT_COLOR};
        font-weight: 500;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {PRIMARY_COLOR}22 !important;
        color: {PRIMARY_COLOR} !important;
        font-weight: 600;
        border-bottom: 3px solid {PRIMARY_COLOR};
    }}
    
    /* Loading animation */
    @keyframes pulse {{
        0% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.6; }}
    }}
    
    .loading-animation {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        background-color: #f9f9f9;
        border-radius: 8px;
        animation: pulse 1.5s infinite;
    }}
    
    /* Card Grid */
    .card-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }}
    
    .event-card {{
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .event-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }}
    
    .event-card-header {{
        padding: 15px;
        background: linear-gradient(90deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
        color: white;
        font-weight: 600;
    }}
    
    .event-card-body {{
        padding: 15px;
    }}
    
    .event-card-footer {{
        padding: 10px 15px;
        background-color: #f5f7fa;
        border-top: 1px solid #eaeaea;
        font-size: 0.9rem;
        color: {MUTED_TEXT};
    }}
</style>
"""

# Add the custom CSS to the page
st.markdown(custom_css, unsafe_allow_html=True)

# Display the custom title
st.markdown('<div class="title-container"><h1 class="title-text">InBloom Festival 2025</h1></div>', unsafe_allow_html=True)

# Helper function to convert an image to base64
def get_image_as_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        # Return a default image if file not found
        return None

# Try to load logo, fallback to a text header if image not found
try:
    logo_base64 = get_image_as_base64("inbloom_logo.png")
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="width:100%; max-width:200px; margin-bottom:15px;">'
    else:
        logo_html = '<h2 style="text-align:center; color:#4CAF50; margin-top:10px;">InBloom</h2>'
except:
    logo_html = '<h2 style="text-align:center; color:#4CAF50; margin-top:10px;">InBloom</h2>'

# ------------------ Dataset Generation Function ------------------
def generate_dataset():
    events = ["Solo Dance", "Group Dance", "Singing", "Drama", "Debate", 
              "Photography", "Poetry", "Fashion Show", "Quiz", "Treasure Hunt"]
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    colleges = ["College A", "College B", "College C", "College D", "College E"]
    states = [
        "Maharashtra", "Karnataka", "Tamil Nadu", "Kerala", 
        "Gujarat", "Delhi", "Uttar Pradesh", "West Bengal",
        "Rajasthan", "Madhya Pradesh", "Punjab", "Telangana"
    ]
    feedback_options = [
        "Amazing event, really enjoyed it!",
        "Could be better organized.",
        "Loved the performance!",
        "Not up to the mark.",
        "Had a great time with friends.",
        "The event was too long.",
        "Well organized and fun.",
        "Disappointing experience.",
        "Incredible talent showcased.",
        "Needs improvement in planning."
    ]
    
    first_names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Drew", "Jamie", "Robin", "Riley", "Cameron",
                   "Aditya", "Priya", "Raj", "Neha", "Vikram", "Anjali", "Arjun", "Divya", "Karthik", "Meera"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
                  "Sharma", "Patel", "Kumar", "Singh", "Gupta", "Reddy", "Verma", "Shah", "Joshi", "Nair"]

    data = []
    for i in range(250):
        participant_id = f"P{i+1:03d}"
        name = random.choice(first_names) + " " + random.choice(last_names)
        college = random.choice(colleges)
        state = random.choice(states)
        event = random.choice(events)
        day = random.choice(days)
        hour = random.randint(10, 18)
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        feedback = random.choice(feedback_options)
        age = random.randint(18, 25)  # Typical college age
        score = random.randint(60, 100)  # Performance/participation score
        gender = random.choice(["Male", "Female", "Non-binary"])
        registration_type = random.choice(["Online", "On-site"])
        satisfaction = random.randint(1, 5)  # 5-point scale
        
        data.append({
            "ParticipantID": participant_id,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "College": college,
            "State": state,
            "Event": event,
            "Day": day,
            "Time": time_str,
            "Score": score,
            "Registration": registration_type,
            "Satisfaction": satisfaction,
            "Feedback": feedback,
            "TotalUsers": random.randint(2500, 3500)
        })
    df = pd.DataFrame(data)
    return df

# Initialize session state and dataset at the very beginning
if 'dataset' not in st.session_state:
    st.session_state['dataset'] = generate_dataset()

# Get the dataset
df = st.session_state['dataset']

# Define filter options globally
all_events = sorted(df["Event"].unique())
all_states = sorted(df["State"].unique())
all_colleges = sorted(df["College"].unique())
all_days = sorted(df["Day"].unique())

# Enhanced Sidebar with custom styling
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown(logo_html, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #4CAF50; font-size: 1.8rem; margin-bottom:20px;'>Cultural Festival '25</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<p class="filter-label">📊 Navigation</p>', unsafe_allow_html=True)
    page = st.radio("", ["Home", "Dataset", "Dashboard", "Text Analysis", "Image Processing", "Event Schedule"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Only show filters if on Dashboard page
    if page == "Dashboard":
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<p class="filter-label">🔍 Filters</p>', unsafe_allow_html=True)
        
        # Event filter with search and select all option
        selected_event = st.multiselect(
            "Select Event", 
            options=["All"] + all_events,
            default=["All"]
        )
        if "All" in selected_event:
            selected_event = all_events
            
        # State filter with search
        selected_state = st.multiselect(
            "Select State", 
            options=["All"] + all_states,
            default=["All"]
        )
        if "All" in selected_state:
            selected_state = all_states
            
        # College filter
        all_colleges = list(df["College"].unique())
        selected_college = st.multiselect(
            "Select College", 
            options=["All"] + all_colleges,
            default=["All"]
        )
        if "All" in selected_college:
            selected_college = all_colleges
            
        # Day filter
        all_days = list(df["Day"].unique())
        selected_day = st.multiselect(
            "Select Day", 
            options=["All"] + all_days,
            default=["All"]
        )
        if "All" in selected_day:
            selected_day = all_days
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current time
    now = datetime.datetime.now()
    st.markdown(f"<p style='text-align:center; color:{MUTED_TEXT}; font-size:0.9rem; margin-top:30px;'>📅 {now.strftime('%B %d, %Y')}<br>⏰ {now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<hr style='margin:30px 0 15px 0; opacity:0.3;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888; font-size:0.8rem;'>© 2025 InBloom Festival<br>All rights reserved</p>", unsafe_allow_html=True)

# ------------------ Home Section ------------------
if page == "Home":
    # Welcome message and stats overview
    st.markdown('<h2 class="section-header">Welcome to InBloom Festival 2025</h2>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box blue-metric">
            <h3 style="color: #1E88E5;">Total Participants</h3>
            <h2 style="color: #000000;">{len(df)}</h2>
            <p style="color: #666666;">From {df['College'].nunique()} colleges</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-box green-metric">
            <h3 style="color: #4CAF50;">Events</h3>
            <h2 style="color: #000000;">{df['Event'].nunique()}</h2>
            <p style="color: #666666;">Across {df['Day'].nunique()} days</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-box orange-metric">
            <h3 style="color: #FF9800;">States Represented</h3>
            <h2 style="color: #000000;">{df['State'].nunique()}</h2>
            <p style="color: #666666;">Pan-India participation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # About the festival
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("""
    ### About InBloom '25
    
    InBloom is an annual cultural festival that celebrates artistic expression, cultural diversity, and creative talent across colleges nationwide. This year's festival features a rich lineup of events including dance, music, drama, literary arts, and more.
    
    ### Highlights
    
    - **Pan-India Participation**: Students from across 12 states
    - **Diverse Events**: 10 unique categories of cultural events
    - **5-Day Extravaganza**: Comprehensive schedule of competitions
    - **Professional Judging**: Industry experts evaluating performances
    - **Amazing Prizes**: Recognition for top talents
    
    Use the navigation panel to explore participant data, visualize trends, analyze feedback, and process event imagery.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Featured events section
    st.markdown('<h2 class="section-header">Featured Events</h2>', unsafe_allow_html=True)

    featured_events = ["Solo Dance", "Group Dance", "Singing", "Drama"]
    event_descriptions = {
        "Solo Dance": "Showcase individual dance talents across various styles from classical to contemporary.",
        "Group Dance": "Team performances highlighting coordination, choreography, and creative expression.",
        "Singing": "Vocal performances spanning genres from classical to modern pop and rock.",
        "Drama": "Theatrical presentations including one-act plays, mono-acting, and improvisations."
    }

    for event in featured_events:
        event_data = df[df["Event"] == event]
        participants = len(event_data)
        avg_score = round(event_data["Score"].mean(), 1)
        
        st.markdown(f"""
        <div style="background: white; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <div style="padding: 15px; background: linear-gradient(90deg, #4CAF50, #1E88E5); color: white; font-weight: 600; border-radius: 10px 10px 0 0;">
                {event}
            </div>
            <div style="padding: 15px; background: white;">
                <p style="color: #333333; margin-bottom: 10px;">{event_descriptions[event]}</p>
                <p style="color: #333333; margin-bottom: 10px;"><strong>Participants:</strong> {participants}</p>
                <p style="color: #333333; margin-bottom: 10px;"><strong>Average Score:</strong> {avg_score}/100</p>
            </div>
            <div style="padding: 10px 15px; background-color: #f5f7fa; border-top: 1px solid #eaeaea; color: #666666; font-size: 0.9rem; border-radius: 0 0 10px 10px;">
                Featured on {', '.join(event_data['Day'].unique())}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Upcoming highlights
    st.markdown('<h2 class="section-header">Festival Highlights</h2>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    # Create tabs for different content
    tab1, tab2, tab3 = st.tabs(["📈 Participation Trends", "🏆 Top Performers", "📅 Schedule"])
    
    with tab1:
        # Participant distribution by state
        state_counts = df["State"].value_counts().reset_index()
        state_counts.columns = ["State", "Count"]
        
        fig = px.choropleth(
            state_counts,
            locations="State",
            locationmode="country names",
            color="Count",
            hover_name="State",
            color_continuous_scale="Viridis",
            title="Participant Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Top scores by event
        top_scores = df.sort_values("Score", ascending=False).head(10)
        
        fig = px.bar(
            top_scores,
            x="Name",
            y="Score",
            color="Event",
            text="Score",
            labels={"Score": "Performance Score", "Name": "Participant"},
            title="Top 10 Performers Across All Events"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Event schedule
        event_schedule = df.groupby(["Day", "Event"]).size().reset_index(name="Participants")
        event_schedule = event_schedule.sort_values(["Day", "Participants"], ascending=[True, False])
        
        # Custom styling for the table
        st.markdown("""
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Day</th>
                    <th>Event</th>
                    <th>Participants</th>
                </tr>
            </thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        for _, row in event_schedule.iterrows():
            st.markdown(f"""
                <tr>
                    <td>{row['Day']}</td>
                    <td>{row['Event']}</td>
                    <td>{row['Participants']}</td>
                </tr>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            </tbody>
        </table>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Dataset Section ------------------
elif page == "Dataset":
    st.markdown('<h2 class="section-header">Dataset Explorer</h2>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    # Tabs for different views of the data
    tab1, tab2, tab3 = st.tabs(["📋 Raw Data", "📊 Summary Statistics", "🔍 Search"])
    
    with tab1:
        st.write("Complete participant data from InBloom '25")
        st.dataframe(df, use_container_width=True)
        
        # Download options
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download as CSV",
                data=csv,
                file_name="inbloom_dataset.csv",
                mime="text/csv",
                help="Download the complete dataset as CSV file",
            )
        
        with col2:
            # Convert to Excel
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='InBloom_Data', index=False)
            excel_data = buffer.getvalue()
            
            st.download_button(
                "Download as Excel",
                data=excel_data,
                file_name="inbloom_dataset.xlsx",
                mime="application/vnd.ms-excel",
                help="Download the complete dataset as Excel file",
            )
    
    with tab2:
        # Summary statistics
        st.write("Key statistical measures for numerical columns")
        st.dataframe(df.describe().round(2), use_container_width=True)
        
        # Distribution of categorical variables
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Event Distribution")
            event_counts = df["Event"].value_counts().reset_index()
            event_counts.columns = ["Event", "Count"]
            
            fig = px.pie(
                event_counts, 
                values="Count", 
                names="Event", 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Day-wise Distribution")
            day_counts = df["Day"].value_counts().reset_index()
            day_counts.columns = ["Day", "Count"]
            
            fig = px.bar(
                day_counts,
                x="Day",
                y="Count",
                color="Day",
                text="Count"
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        # Gender distribution
        st.subheader("Participant Demographics")
        col1, col2 = st.columns(2)
        
        with col1:
            gender_counts = df["Gender"].value_counts().reset_index()
            gender_counts.columns = ["Gender", "Count"]
            
            fig = px.pie(
                gender_counts,
                values="Count",
                names="Gender",
                title="Gender Distribution",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age distribution
            fig = px.histogram(
                df,
                x="Age",
                nbins=8,
                title="Age Distribution",
                color_discrete_sequence=["#4CAF50"]
            )
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Search functionality
        st.write("Search for specific participants or filter by criteria")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            search_term = st.text_input("Search by name or ID", "")
        
        with col2:
            search_event = st.selectbox("Filter by event", ["All"] + list(df["Event"].unique()))
        
        # Apply filters
        filtered_results = df.copy()
        if search_term:
            filtered_results = filtered_results[
                filtered_results["Name"].str.contains(search_term, case=False) | 
                filtered_results["ParticipantID"].str.contains(search_term, case=False)
            ]
        
        if search_event != "All":
            filtered_results = filtered_results[filtered_results["Event"] == search_event]
        
        # Display filtered results
        st.write(f"Found {len(filtered_results)} matching results:")
        st.dataframe(filtered_results, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Dashboard Section ------------------
elif page == "Dashboard":
    st.markdown('<h2 class="section-header">Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Apply filters to dataset
    filtered_df = df[
        (df["Event"].isin(selected_event)) &
        (df["State"].isin(selected_state))
    ]
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box primary-metric">
            <h3>Total Participants</h3>
            <h2>{len(filtered_df)}</h2>
            <p>From {filtered_df['College'].nunique()} colleges</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_score = filtered_df['Score'].mean()
        st.markdown(f"""
        <div class="metric-box secondary-metric">
            <h3>Average Score</h3>
            <h2>{avg_score:.1f}</h2>
            <p>Out of 100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        satisfaction = filtered_df['Satisfaction'].mean()
        st.markdown(f"""
        <div class="metric-box accent-metric">
            <h3>Satisfaction Rate</h3>
            <h2>{satisfaction:.1f}%</h2>
            <p>Based on feedback</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_events = filtered_df['Event'].nunique()
        st.markdown(f"""
        <div class="metric-box info-metric">
            <h3>Active Events</h3>
            <h2>{total_events}</h2>
            <p>Across {filtered_df['Day'].nunique()} days</p>
        </div>
        """, unsafe_allow_html=True)

    # Create tabs for different visualizations
    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["📊 Participation", "📈 Performance", "🎯 Demographics"])
    
    with viz_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Event-wise participation
            event_participation = filtered_df['Event'].value_counts()
            fig = px.bar(
                x=event_participation.index,
                y=event_participation.values,
                title="Event-wise Participation",
                labels={'x': 'Event', 'y': 'Participants'},
                color=event_participation.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Day-wise trend
            day_trend = filtered_df.groupby('Day').size().reset_index(name='count')
            fig = px.line(
                day_trend,
                x='Day',
                y='count',
                title="Daily Participation Trend",
                markers=True,
                line_shape='spline'
            )
            st.plotly_chart(fig, use_container_width=True)

    with viz_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Score distribution
            fig = px.histogram(
                filtered_df,
                x='Score',
                nbins=20,
                title="Score Distribution",
                color_discrete_sequence=['#1E88E5']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Event-wise average scores
            avg_scores = filtered_df.groupby('Event')['Score'].mean().sort_values(ascending=True)
            fig = px.bar(
                x=avg_scores.values,
                y=avg_scores.index,
                orientation='h',
                title="Average Scores by Event",
                color=avg_scores.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)

    with viz_tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution
            gender_dist = filtered_df['Gender'].value_counts()
            fig = px.pie(
                values=gender_dist.values,
                names=gender_dist.index,
                title="Gender Distribution",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age distribution
            fig = px.box(
                filtered_df,
                y='Age',
                x='Event',
                title="Age Distribution by Event",
                color='Event',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# ------------------ Text Analysis Section ------------------
elif page == "Text Analysis":
    st.markdown('<h2 class="section-header">Feedback Analysis</h2>', unsafe_allow_html=True)
    
    # Create tabs for different text analysis views
    text_tab1, text_tab2 = st.tabs(["🔤 Word Cloud", "📊 Sentiment Analysis"])
    
    with text_tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_event_feedback = st.selectbox(
                "Select Event",
                options=df["Event"].unique(),
                key="wordcloud_event"
            )
            
            min_word_length = st.slider(
                "Minimum Word Length",
                min_value=3,
                max_value=10,
                value=4
            )
            
            background_color = st.color_picker(
                "Background Color",
                value="#ffffff"
            )
        
        with col2:
            event_feedback = df[df["Event"] == selected_event_feedback]["Feedback"].str.cat(sep=" ")
            if event_feedback.strip():
                wc = WordCloud(
                    width=800,
                    height=400,
                    background_color=background_color,
                    min_word_length=min_word_length,
                    colormap='viridis'
                ).generate(event_feedback)
                
                fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
                ax_wc.imshow(wc, interpolation="bilinear")
                ax_wc.axis("off")
                st.pyplot(fig_wc)
            else:
                st.info("No feedback available for this event.")
    
    with text_tab2:
        # Simple sentiment analysis based on predefined positive/negative words
        positive_words = set(['excellent', 'amazing', 'great', 'good', 'wonderful', 'fantastic'])
        negative_words = set(['poor', 'bad', 'disappointing', 'terrible', 'awful', 'horrible'])
        
        def analyze_sentiment(text):
            words = set(text.lower().split())
            pos_count = len(words.intersection(positive_words))
            neg_count = len(words.intersection(negative_words))
            return 'Positive' if pos_count > neg_count else 'Negative' if neg_count > pos_count else 'Neutral'
        
        sentiment_results = df['Feedback'].apply(analyze_sentiment).value_counts()
        
        fig = px.pie(
            values=sentiment_results.values,
            names=sentiment_results.index,
            title="Overall Feedback Sentiment",
            color_discrete_sequence=['#4CAF50', '#FFC107', '#F44336']
        )
        st.plotly_chart(fig)

# ------------------ Image Processing Section ------------------
elif page == "Image Processing":
    st.markdown('<h2 class="section-header">Event Image Processing</h2>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload Event Images",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # Image processing options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_option = st.selectbox(
                "Select Filter",
                ["Original", "Grayscale", "Blur", "Edge Enhance", "Sharpen", "Emboss"]
            )
        
        with col2:
            brightness = st.slider("Brightness", 0.0, 2.0, 1.0, 0.1)
        
        with col3:
            contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1)
        
        # Display images in grid
        cols = st.columns(3)
        for idx, uploaded_file in enumerate(uploaded_files):
            with cols[idx % 3]:
                img = Image.open(uploaded_file)
                
                # Apply selected filter
                if filter_option == "Grayscale":
                    img = ImageOps.grayscale(img)
                elif filter_option == "Blur":
                    img = img.filter(ImageFilter.BLUR)
                elif filter_option == "Edge Enhance":
                    img = img.filter(ImageFilter.EDGE_ENHANCE)
                elif filter_option == "Sharpen":
                    img = img.filter(ImageFilter.SHARPEN)
                elif filter_option == "Emboss":
                    img = img.filter(ImageFilter.EMBOSS)
                
                # Apply brightness and contrast
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
                
                st.image(img, caption=f"Processed Image {idx+1}", use_column_width=True)
        
        # Add download button for processed images
        if st.button("Download Processed Images"):
            # Create a ZIP file containing all processed images
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for idx, uploaded_file in enumerate(uploaded_files):
                    img = Image.open(uploaded_file)
                    # Apply the same processing as above
                    # Save to zip
                    img_buffer = BytesIO()
                    img.save(img_buffer, format="PNG")
                    zip_file.writestr(f"processed_image_{idx+1}.png", img_buffer.getvalue())
            
            st.download_button(
                "Download ZIP",
                data=zip_buffer.getvalue(),
                file_name="processed_images.zip",
                mime="application/zip"
            )
    else:
        st.info("Upload some images to get started!")

# ------------------ Event Schedule Section ------------------
elif page == "Event Schedule":
    st.markdown('<h2 class="section-header">Event Schedule</h2>', unsafe_allow_html=True)
    
    # Create schedule dataframe
    schedule_df = df.groupby(['Day', 'Event', 'Time']).size().reset_index(name='Participants')
    schedule_df = schedule_df.sort_values(['Day', 'Time'])
    
    # Custom CSS for better timeline visualization
    st.markdown("""
    <style>
    .timeline-container {
        margin: 20px 0;
        padding: 20px;
        background: #1a1a1a;
        border-radius: 10px;
    }
    
    .schedule-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: #2d2d2d;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .schedule-table th {
        background: #4CAF50;
        color: white;
        padding: 12px;
        text-align: left;
    }
    
    .schedule-table td {
        padding: 12px;
        border-bottom: 1px solid #3d3d3d;
        color: #ffffff;
    }
    
    .schedule-table tr:hover {
        background: #363636;
    }
    
    .event-dot {
        height: 12px;
        width: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create tabs for different days
    day_tabs = st.tabs([f"Day {day.split()[-1]}" for day in sorted(schedule_df['Day'].unique())])
    
    # Color palette for different events
    color_palette = {
        "Solo Dance": "#FF6B6B",
        "Group Dance": "#4ECDC4",
        "Singing": "#45B7D1",
        "Drama": "#96CEB4",
        "Debate": "#FFEEAD",
        "Photography": "#D4A5A5",
        "Poetry": "#9B9B9B",
        "Fashion Show": "#FFD93D",
        "Quiz": "#6C5B7B",
        "Treasure Hunt": "#FF8C42"
    }
    
    for idx, day in enumerate(sorted(schedule_df['Day'].unique())):
        with day_tabs[idx]:
            st.markdown(f"<h3 style='color: #4CAF50;'>{day} Schedule</h3>", unsafe_allow_html=True)
            
            day_schedule = schedule_df[schedule_df['Day'] == day].sort_values('Time')
            
            # Create timeline visualization
            fig = go.Figure()
            
            for event in day_schedule['Event'].unique():
                event_data = day_schedule[day_schedule['Event'] == event]
                fig.add_trace(go.Scatter(
                    x=event_data['Time'],
                    y=[event] * len(event_data),
                    mode='markers+text',
                    name=event,
                    text=event_data['Participants'].apply(lambda x: f'{x} participants'),
                    marker=dict(
                        size=20,
                        color=color_palette[event],
                        symbol='circle'
                    ),
                    textposition="top center"
                ))
            
            fig.update_layout(
                plot_bgcolor='#1a1a1a',
                paper_bgcolor='#1a1a1a',
                font=dict(color='white'),
                showlegend=True,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#2d2d2d',
                    title='Time',
                    title_font=dict(color='white')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#2d2d2d',
                    title='Event',
                    title_font=dict(color='white')
                ),
                legend=dict(
                    bgcolor='#2d2d2d',
                    bordercolor='#3d3d3d'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed schedule in a table
            st.markdown("<div class='timeline-container'>", unsafe_allow_html=True)
            st.markdown("""
            <table class="schedule-table">
                <tr>
                    <th>Time</th>
                    <th>Event</th>
                    <th>Participants</th>
                </tr>
            """, unsafe_allow_html=True)
            
            for _, row in day_schedule.iterrows():
                event_color = color_palette[row['Event']]
                st.markdown(f"""
                <tr>
                    <td>{row['Time']}</td>
                    <td>
                        <span class="event-dot" style="background-color: {event_color}"></span>
                        {row['Event']}
                    </td>
                    <td>{row['Participants']}</td>
                </tr>
                """, unsafe_allow_html=True)
            
            st.markdown("</table>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
