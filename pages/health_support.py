

import streamlit as st
import os
import sys
import json
import requests
import datetime
import calendar
import pandas as pd
import seaborn as sb
import openai
import google.generativeai as genai
import africastalking
import pyttsx3 as pt
from gtts import gTTS



from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_chat import message


from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


st.image('./src/health-wellness-talks-og.jpg', width=800)

body = st.container()



def get_chat_response(prompt):

        model = genai.GenerativeModel("gemini-1.5-flash", 
            system_instruction="You are JasiriFit, an expert wellness and fitness assistant for women. Your role is to Generate a personalized engaging chat with the user and respond accordingly, make it localized conversation tailored to meet specific user needs"
            )  
        response = model.generate_content(
        prompt + ' in Kenya',
        generation_config = genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.1,
        )
    )

        st.write(response.text)



with body:
    with st.form(key = 'user_submit'):
    	ai_bot = st.write('JasiriFit: Hi There!!! How may I help you', '''
    		''')

    	human = st.text_area('Human: ', '''
    		''')

    	submit = st.form_submit_button(label = 'submit')

    response = get_chat_response(human)

    speech = st.button('Talking Buddy')

if speech:
    audio = pt.init()
    audio.say(get_chat_response(human))
    audio.runAndWait()

