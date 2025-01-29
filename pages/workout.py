

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



from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_chat import message


from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime

st.write('''
			# Workout & Fitness
		''')

st.image('./src/health-wellness.jpg', width=800)

st.write(''' Weight Loss Tracker''')
with st.form(key='form2'):
	df = pd.DataFrame(columns = ['Date', 'Target_weight', 'Period'])
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		current_weight = st.number_input('Current weight (kgs)', value=10, min_value=5, max_value=300)

	with col2:
		target_weight = st.number_input('Target weight(kgs)', value=5, min_value=5, max_value=300)

	with col3:
		avg_wk_loss = st.slider('Average week loss(kgs)', value=1.5, min_value=0.0, max_value=3.0)

	with col4:
		startDate = st.date_input("Exercise start date", datetime.today())

	weight_submit_btn = st.form_submit_button('Calculate')


	def get_workout_plan(prompt):

		model = genai.GenerativeModel("gemini-1.5-flash", 
	    	system_instruction="You are JasiriFit, an expert wellness and fitness assistant for women. Your role is to provide personalized guidance on workouts, nutrition, mental well-being, and healthy lifestyle habits. Offer practical, science-backed, and easy-to-follow advice in a friendly and motivating tone."
	)
		response = model.generate_content(
	    prompt + ' in Kenya',
	    generation_config = genai.GenerationConfig(
	        max_output_tokens=1000,
	        temperature=0.1,
	    )
	)

		st.write(response.text)


	prompt = f'''
		"Generate a personalized Week 1 Workout and Fitness Plan in a tabular format based on the following details:

		Current weight: {current_weight} kg
		Target weight: {target_weight} kg
		Average weekly weight loss goal: {avg_wk_loss} kg
		Start date: {startDate}
		
		The table should include:

		Day (e.g., Day 1, Day 2...)
		Time of workout (Morning, Afternoon, Evening)
		Workout type (e.g., Cardio, Strength Training, Yoga, Rest, etc.)
		Workout details (e.g., exercises, reps, duration)
		Recommended Kenyan localized meals (from morning to evening, including snacks)
	'''
	
	if weight_submit_btn not in st.session_state:
		
		# startDate = datetime.today()
		wk_count = 0
		data = []
		loss = 0
		
		while current_weight > target_weight:
			startDate += timedelta(days = 7)
			current_weight -= avg_wk_loss
			wk_count += 1
			loss += current_weight
			data.append([startDate, current_weight, 'week '+ str(wk_count)])
			print(startDate, round(current_weight, 2))
			print("takes", wk_count, "weeks to complete the target")
		# except Exception as e:
		# 	st.error("An error occurred. Halting the program.", str(e))
		# 	st.exception("System error:", sys.exc_info()[0])
		# 	st.stop()




col1, col2 = st.columns(2)
with col1:
	df = pd.DataFrame(data, columns=['Date', 'Target_weight', 'Period'])
	st.dataframe(df, use_container_width=True)

with col2:
	st.write('Statistics say')
	# st.metric("", str(df['Date'].iloc[-1])[0:4], " yrs")
	col1, col2, col3 = st.columns(3)
	col1.metric("achieve by", str(df['Date'].iloc[-1])[:4], str(pd.to_datetime(df['Date']).dt.month_name().iloc[-1]))
	with col2:
		if wk_count <= 1:
			col2.metric("total of", str(wk_count), " Week")
		else:
			col2.metric("total of", str(wk_count), " Weeks")
	col3.metric("weight lost", str(avg_wk_loss * wk_count), "-Kgs")
	
	col1, col2 = st.columns(2)
	with col1:
		calories = 7700 # avg calories burnt per kg
		st.metric('total burnt', str(calories * (avg_wk_loss * wk_count)), "-Calories")






get_workout_plan(prompt)

with st.popover("Send to SMS", icon=":material/sms:"):

	with st.form(key="report"):
		phone_number = st.number_input('Phone Number', value=0, min_value=0, max_value=int(10e10))

		submit_report = st.form_submit_button("Send")

		def send_report():
			amount = "10"
			currency_code = "KES"


			recipients = [f"+254{str(phone_number)}"]
			# airtime_rec = "+254" + str(phone_number)
			print(recipients)
			print(phone_number)

			# Set your message
			message = f"Welcome to JasiriFit! Revolutionizing your wellness and fitness with personalized workouts, nutrition guidance, and holistic well-being support. Let's embark on a healthier, stronger, and more balanced journey together! #StrongerWithJasiriFit";
			# Set your shortCode or senderId
			sender = 20880
			try:
				# responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)
				response = sms.send(message, recipients, sender)
				
				print(response)
				# print(responses)
			except Exception as e:
				print(f'Houston, we have a problem: {e}')

	if submit_report not in st.session_state:
		send_report()
