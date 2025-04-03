# InBloom '25 Dashboard

Hey there, fellow coder! Welcome to the **InBloom '25 Dashboard**—your one-stop Streamlit app for visualizing participation data from the InBloom Inter-College Cultural Events. This project was built for the Advanced Python lab (MCA372A) and covers everything from dataset generation to interactive visualizations, text analysis with word clouds, and even custom image processing. No cap—this app is designed to be both functional and lit!

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview

**InBloom '25 Dashboard** is a data-driven web application built with Streamlit. It generates a simulated dataset of 250 participants across 5 days and 10 cultural events, allowing you to:
- Visualize participation trends via multiple interactive charts.
- Analyze participant feedback through a word cloud.
- Process and showcase event-related images with custom filters.

This project was developed as a lab test and is now ready for deployment. No more excuses—deploy and flex your data analysis skills!

---

## Features

- **Dataset Generation:** Automatically generates a dataset with 10 columns (including participant ID, name, college, state, event, day, time, and feedback) for 250 participants.
- **Interactive Dashboard:** Provides visualizations including:
  - Day-wise, Event-wise, College-wise, and State-wise participation charts.
  - Participation time histogram.
- **Text Analysis:** Generates a word cloud from event-specific feedback to spotlight trending keywords.
- **Image Processing:** Upload images and apply filters like grayscale, blur, edge enhancement, or invert.
- **User-friendly UI:** Filters, sidebars, and a responsive design that makes the app both aesthetic and super easy to use.

---

## Prerequisites

Make sure you have these installed:
- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [WordCloud](https://github.com/amueller/word_cloud)
- [Pillow (PIL)](https://python-pillow.org/)

You can install the dependencies using pip (see [Installation](#installation)).

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/inbloom-dashboard.git
   cd inbloom-dashboard
