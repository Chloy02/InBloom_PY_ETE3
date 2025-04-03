import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud
from PIL import Image, ImageFilter, ImageOps

# Set up the Streamlit page configuration
st.set_page_config(page_title="InBloom", page_icon=":tulip:", layout="wide")

# Custom CSS for styling
custom_css = """
<style>
    /* Main container styling */
    .main {
        padding: 1rem;
    }
    
    /* Custom title styling */
    .title-text {
        color: #1E88E5;
        font-size: 3rem;
        font-weight: 600;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    /* Section headers */
    .section-header {
        color: #2E7D32;
        font-size: 1.8rem;
        padding: 0.5rem 0;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
        padding-left: 1rem;
    }
    
    /* Dashboard metrics */
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1E88E5;
        margin: 0.5rem 0;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        /* Reduce the padding to minimize white space */
        padding: 0.5rem;
        /* Optionally, remove or reduce top margin:
           margin-top: -10px; 
        */
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Filter labels */
    .filter-label {
        color: #424242;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Download button */
    .download-btn {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .download-btn:hover {
        background-color: #45a049;
    }
</style>
"""

# Add the custom CSS to the page
st.markdown(custom_css, unsafe_allow_html=True)

# Update the title styling
st.markdown('<p class="title-text">InBloom</p>', unsafe_allow_html=True)

# Enhanced Sidebar with custom styling
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.image("inbloom_logo.png", use_container_width=True)
    st.markdown("<h1 style='text-align: center; color: #4CAF50; font-size: 2rem;'>InBloom '25</h1>", unsafe_allow_html=True)
    st.markdown('<p class="filter-label">Navigation</p>', unsafe_allow_html=True)
    page = st.radio("Go to", ["Dataset", "Dashboard", "Text Analysis", "Image Processing"])
    st.markdown("---")

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
    
    first_names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Drew", "Jamie", "Robin", "Riley", "Cameron"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]

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
        
        data.append({
            "ParticipantID": participant_id,
            "Name": name,
            "Age": age,
            "College": college,
            "State": state,
            "Event": event,
            "Day": day,
            "Time": time_str,
            "Score": score,
            "Feedback": feedback
        })
    df = pd.DataFrame(data)
    return df

# Generate and store dataset in session state for persistence
if "dataset" not in st.session_state:
    st.session_state["dataset"] = generate_dataset()
df = st.session_state["dataset"]

# ------------------ Dataset Section ------------------
if page == "Dataset":
    st.markdown('<h2 class="section-header">Dataset</h2>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.write("Generated Dataset for InBloom '25")
    st.dataframe(df)
    st.markdown('</div>', unsafe_allow_html=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="inbloom_dataset.csv",
        mime="text/csv",
        help="Click to download the dataset as CSV",
    )

# ------------------ Dashboard Section ------------------
elif page == "Dashboard":
    st.markdown('<h2 class="section-header">Dashboard</h2>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.write("Visualize participation trends with interactive filters.")

    # --- FIRST, define your filters and filtered_df ---
    selected_event = st.sidebar.multiselect("Select Event", options=df["Event"].unique(), default=df["Event"].unique())
    selected_state = st.sidebar.multiselect("Select State", options=df["State"].unique(), default=df["State"].unique())
    selected_college = st.sidebar.multiselect("Select College", options=df["College"].unique(), default=df["College"].unique())
    selected_day = st.sidebar.multiselect("Select Day", options=df["Day"].unique(), default=df["Day"].unique())

    filtered_df = df[
        (df["Event"].isin(selected_event)) &
        (df["State"].isin(selected_state)) &
        (df["College"].isin(selected_college)) &
        (df["Day"].isin(selected_day))
    ]

    # --- THEN, display your metrics that use filtered_df ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="padding:1.2rem; background-color:#f0f8ff; border-radius:8px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color:#1E88E5; margin-bottom:8px; font-size:1.1rem;">Total Participants</h3>
            <h2 style="color:#000000; margin:0; font-size:2rem;">{len(filtered_df)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_score = filtered_df["Score"].mean() if not filtered_df.empty else 0
        st.markdown(f"""
        <div style="padding:1.2rem; background-color:#f0fff0; border-radius:8px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color:#2E7D32; margin-bottom:8px; font-size:1.1rem;">Average Score</h3>
            <h2 style="color:#000000; margin:0; font-size:2rem;">{avg_score:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        event_count = filtered_df["Event"].nunique() if not filtered_df.empty else 0
        st.markdown(f"""
        <div style="padding:1.2rem; background-color:#fff0f0; border-radius:8px; text-align:center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color:#C62828; margin-bottom:8px; font-size:1.1rem;">Events Count</h3>
            <h2 style="color:#000000; margin:0; font-size:2rem;">{event_count}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("Filtered Dataset:", filtered_df.shape)
    st.dataframe(filtered_df)

    # ------------------ Chart Layout in Columns ------------------
    # 1. Day-wise Participation and 2. Event-wise Participation
    colA, colB = st.columns(2)
    with colA:
        day_counts = filtered_df["Day"].value_counts().sort_index()
        fig1, ax1 = plt.subplots()
        ax1.bar(day_counts.index, day_counts.values, color="skyblue")
        ax1.set_title("Day-wise Participation")
        ax1.set_xlabel("Day")
        ax1.set_ylabel("Number of Participants")
        st.pyplot(fig1)

    with colB:
        event_counts = filtered_df["Event"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.bar(event_counts.index, event_counts.values, color="coral")
        ax2.set_title("Event-wise Participation")
        ax2.set_xlabel("Event")
        ax2.set_ylabel("Number of Participants")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    # 3. College-wise Participation and 4. State-wise Participation
    colC, colD = st.columns(2)
    with colC:
        college_counts = filtered_df["College"].value_counts()
        fig3, ax3 = plt.subplots()
        ax3.bar(college_counts.index, college_counts.values, color="lightgreen")
        ax3.set_title("College-wise Participation")
        ax3.set_xlabel("College")
        ax3.set_ylabel("Number of Participants")
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    with colD:
        state_counts = filtered_df["State"].value_counts()
        fig4, ax4 = plt.subplots()
        ax4.bar(state_counts.index, state_counts.values, color="plum")
        ax4.set_title("State-wise Participation")
        ax4.set_xlabel("State")
        ax4.set_ylabel("Number of Participants")
        st.pyplot(fig4)

    # 5. Participation Time Distribution & 6. Age Distribution
    colE, colF = st.columns(2)
    with colE:
        times = pd.to_datetime(filtered_df["Time"], format="%H:%M").dt.hour
        fig5, ax5 = plt.subplots()
        ax5.hist(times, bins=range(10, 20), color="gold", edgecolor="black")
        ax5.set_title("Participation Time Distribution")
        ax5.set_xlabel("Hour of the Day")
        ax5.set_ylabel("Frequency")
        st.pyplot(fig5)

    with colF:
        fig6, ax6 = plt.subplots()
        ax6.hist(filtered_df["Age"], bins=8, color="lightblue", edgecolor="black")
        ax6.set_title("Age Distribution of Participants")
        ax6.set_xlabel("Age")
        ax6.set_ylabel("Frequency")
        st.pyplot(fig6)

    # 7. Score Distribution & 8. Average Score by Event
    colG, colH = st.columns(2)
    with colG:
        fig7, ax7 = plt.subplots()
        ax7.hist(filtered_df["Score"], bins=10, color="salmon", edgecolor="black")
        ax7.set_title("Score Distribution")
        ax7.set_xlabel("Score")
        ax7.set_ylabel("Frequency")
        st.pyplot(fig7)

    with colH:
        if not filtered_df.empty:
            avg_scores = filtered_df.groupby("Event")["Score"].mean().sort_values(ascending=False)
            fig8, ax8 = plt.subplots()
            ax8.bar(avg_scores.index, avg_scores.values, color="lightgreen")
            ax8.set_title("Average Score by Event")
            ax8.set_xlabel("Event")
            ax8.set_ylabel("Average Score")
            plt.xticks(rotation=45)
            st.pyplot(fig8)
        else:
            st.write("No data available for selected filters.")

# ------------------ Text Analysis Section ------------------
elif page == "Text Analysis":
    st.markdown('<h2 class="section-header">Text Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.write("Generate a word cloud based on event-wise feedback.")
    st.markdown('</div>', unsafe_allow_html=True)

    event_option = st.selectbox("Select Event for Feedback Analysis", options=df["Event"].unique())
    event_feedback = df[df["Event"] == event_option]["Feedback"].str.cat(sep=" ")

    if event_feedback.strip():
        wc = WordCloud(width=800, height=400, background_color='white').generate(event_feedback)
        fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
        ax_wc.imshow(wc, interpolation="bilinear")
        ax_wc.axis("off")
        ax_wc.set_title(f"Word Cloud for {event_option}")
        st.pyplot(fig_wc)
    else:
        st.write("No feedback available for this event.")

# ------------------ Image Processing Section ------------------
elif page == "Image Processing":
    st.markdown('<h2 class="section-header">Image Processing</h2>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.write("Upload event-related images and apply custom processing.")
    st.markdown('</div>', unsafe_allow_html=True)

    selected_gallery_day = st.selectbox("Select Day for Image Gallery", options=df["Day"].unique())
    uploaded_images = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_images:
        st.subheader("Original Images")
        cols = st.columns(3)
        for i, img_file in enumerate(uploaded_images):
            image = Image.open(img_file)
            cols[i % 3].image(image, caption="Original", use_container_width=True)
        
        st.subheader("Apply Custom Image Processing")
        processing_option = st.selectbox(
            "Select Processing Option", 
            options=["Grayscale", "Blur", "Edge Enhance", "Invert"]
        )
        processed_images = []
        for img_file in uploaded_images:
            image = Image.open(img_file)
            if processing_option == "Grayscale":
                processed = ImageOps.grayscale(image)
            elif processing_option == "Blur":
                processed = image.filter(ImageFilter.BLUR)
            elif processing_option == "Edge Enhance":
                processed = image.filter(ImageFilter.EDGE_ENHANCE)
            elif processing_option == "Invert":
                processed = ImageOps.invert(image.convert("RGB"))
            processed_images.append(processed)
        
        st.subheader("Processed Images")
        cols_proc = st.columns(3)
        for i, proc_img in enumerate(processed_images):
            cols_proc[i % 3].image(proc_img, caption=processing_option, use_container_width=True)
    else:
        st.write("No images uploaded.")
