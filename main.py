import streamlit as st 
import pandas as pd 
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 
import os
import csv
import sys



registration = st.Page("./pages/app.py", title="Registration", icon=":material/login:")
smart_coaching = st.Page("./pages/smart_coaching.py", title="Smart Coaching", icon=":material/monitor_weight_gain:")
work_out_and_fitness = st.Page("./pages/workout.py", title="Workout & Fitness", icon=":material/fitness_center:")
health_support = st.Page("./pages/health_support.py", title="Health Support", icon=":material/monitor_heart:")
community_engagement = st.Page("./pages/community.py", title="Community Engagement", icon=":material/communities:")




pg = st.navigation([registration, smart_coaching, work_out_and_fitness, health_support, community_engagement])

st.set_page_config(
    page_title="JasiriFit",
    page_icon="🧘‍♀️🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.echominds.africa',
        'Report a bug': "https://www.echominds.africa",
        'About': "# We are a leading insights and predicting big data application, Try *JasiriFit* and experience reality!"
    }
)


pg.run()
