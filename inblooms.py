import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud
from PIL import Image, ImageFilter, ImageOps

st.set_page_config(page_title="InBloom", page_icon=":tulip:", layout="wide")
st.title("InBloom")
st.write("This is a web app that allows you to visualize the data from the InBloom dataset.")

# Dataset generation
def generate_dataset():
    # Predefined lists for dataset generation
    events = ["Solo Dance", "Group Dance", "Singing", "Drama", "Debate", 
              "Photography", "Poetry", "Fashion Show", "Quiz", "Treasure Hunt"]
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    colleges = ["College A", "College B", "College C", "College D", "College E"]
    states = ["State X", "State Y", "State Z", "State W"]
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
    
    # Generate random names from sample first and last names
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
        # Generate a random time between 10:00 and 18:00
        hour = random.randint(10, 18)
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        feedback = random.choice(feedback_options)
        data.append({
            "ParticipantID": participant_id,
            "Name": name,
            "College": college,
            "State": state,
            "Event": event,
            "Day": day,
            "Time": time_str,
            "Feedback": feedback
        })
    df = pd.DataFrame(data)
    return df

# Generate the dataset and store it in session state for persistence
if "dataset" not in st.session_state:
    st.session_state["dataset"] = generate_dataset()
df = st.session_state["dataset"]

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dataset", "Dashboard", "Text Analysis", "Image Processing"])

# ------------------ Dataset Section ------------------
if page == "Dataset":
    st.header("Dataset")
    st.write("Generated Dataset for InBloom '25")
    st.dataframe(df)
    # Provide an option to download the dataset as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="inbloom_dataset.csv", mime="text/csv")

# ------------------ Dashboard Section ------------------
elif page == "Dashboard":
    st.header("Dashboard")
    st.write("Visualize participation trends with interactive filters.")

    # Dashboard Filters in Sidebar
    st.sidebar.subheader("Dashboard Filters")
    selected_event = st.sidebar.multiselect("Select Event", options=df["Event"].unique(), default=df["Event"].unique())
    selected_state = st.sidebar.multiselect("Select State", options=df["State"].unique(), default=df["State"].unique())
    selected_college = st.sidebar.multiselect("Select College", options=df["College"].unique(), default=df["College"].unique())
    selected_day = st.sidebar.multiselect("Select Day", options=df["Day"].unique(), default=df["Day"].unique())

    # Filter the dataset based on the selections
    filtered_df = df[
        (df["Event"].isin(selected_event)) &
        (df["State"].isin(selected_state)) &
        (df["College"].isin(selected_college)) &
        (df["Day"].isin(selected_day))
    ]

    st.write("Filtered Dataset:", filtered_df.shape)
    st.dataframe(filtered_df)

    # 1. Day-wise Participation Chart
    day_counts = filtered_df["Day"].value_counts().sort_index()
    fig1, ax1 = plt.subplots()
    ax1.bar(day_counts.index, day_counts.values, color="skyblue")
    ax1.set_title("Day-wise Participation")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Number of Participants")
    st.pyplot(fig1)

    # 2. Event-wise Participation Chart
    event_counts = filtered_df["Event"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.bar(event_counts.index, event_counts.values, color="coral")
    ax2.set_title("Event-wise Participation")
    ax2.set_xlabel("Event")
    ax2.set_ylabel("Number of Participants")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # 3. College-wise Participation Chart
    college_counts = filtered_df["College"].value_counts()
    fig3, ax3 = plt.subplots()
    ax3.bar(college_counts.index, college_counts.values, color="lightgreen")
    ax3.set_title("College-wise Participation")
    ax3.set_xlabel("College")
    ax3.set_ylabel("Number of Participants")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # 4. State-wise Participation Chart
    state_counts = filtered_df["State"].value_counts()
    fig4, ax4 = plt.subplots()
    ax4.bar(state_counts.index, state_counts.values, color="plum")
    ax4.set_title("State-wise Participation")
    ax4.set_xlabel("State")
    ax4.set_ylabel("Number of Participants")
    st.pyplot(fig4)

    # 5. Participation Time Distribution Histogram
    times = pd.to_datetime(filtered_df["Time"], format="%H:%M").dt.hour
    fig5, ax5 = plt.subplots()
    ax5.hist(times, bins=range(10, 20), color="gold", edgecolor="black")
    ax5.set_title("Participation Time Distribution")
    ax5.set_xlabel("Hour of the Day")
    ax5.set_ylabel("Frequency")
    st.pyplot(fig5)

# ------------------ Text Analysis Section ------------------
elif page == "Text Analysis":
    st.header("Text Analysis")
    st.write("Generate a word cloud based on event-wise feedback.")

    # Select an event for feedback analysis
    event_option = st.selectbox("Select Event for Feedback Analysis", options=df["Event"].unique())
    event_feedback = df[df["Event"] == event_option]["Feedback"].str.cat(sep=" ")

    # Generate and display the word cloud
    if event_feedback:
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
    st.header("Image Processing")
    st.write("Upload event-related images and apply custom processing.")

    # Option to choose a day for image gallery (optional filter)
    selected_gallery_day = st.selectbox("Select Day for Image Gallery", options=df["Day"].unique())

    # File uploader for images (multiple allowed)
    uploaded_images = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_images:
        st.subheader("Original Images")
        cols = st.columns(3)
        for i, img_file in enumerate(uploaded_images):
            image = Image.open(img_file)
            cols[i % 3].image(image, caption="Original", use_container_width=True)

        st.subheader("Apply Custom Image Processing")
        processing_option = st.selectbox("Select Processing Option", 
                                         options=["Grayscale", "Blur", "Edge Enhance", "Invert"])
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

