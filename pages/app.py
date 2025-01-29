import streamlit as st 
import africastalking
import os

from dotenv import load_dotenv

load_dotenv()

# genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime

col1, col2 = st.columns(2)

with col1:
	with st.form("user_registration"):
	    st.subheader("User Self Registration")
	    names = st.text_input("Enter Full Names")
	    username = st.text_input('Username:')
	    email = st.text_input("Email: ")
	    phone_number = st.number_input("Phone Number:", value=0, min_value=0, max_value=int(10e10))
	    checkbox_val = st.checkbox("Subscribe to our Newsletter")

	    # Every form must have a submit button.
	    submitted = st.form_submit_button("Submit")

	    if submitted:

	        amount = "10"
	        currency_code = "KES"

	        recipients = [f"+254{str(phone_number)}"]

	        airtime_rec = "+254" + str(phone_number)

	        print(recipients)
	        print(phone_number)

	        # Set your message
	        message = f"Welcome to JasiriFit! Revolutionizing your wellness and fitness with personalized workouts, nutrition guidance, and holistic well-being support. Let's embark on a healthier, stronger, and more balanced journey together! #StrongerWithJasiriFit";

	        # Set your shortCode or senderId
	        sender = 20880

	        try:
	        	responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)
	        	response = sms.send(message, recipients, sender)

	        	print(response)

	        	print(responses)

	        except Exception as e:
	        	print(f'Houston, we have a problem: {e}')

	

	# st.write("Outside the form")

with col2:
	st.image('./src/58019_1733224304.png', width=700)