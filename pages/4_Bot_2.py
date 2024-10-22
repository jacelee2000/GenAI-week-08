# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
# from helper_functions import llm
from logics.customer_query_handler import process_user_message_2
from helper_functions.utility import check_password


# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Ngee Ann Polytechnic DAE International Qualificacation Bot"
)
# endregion <--------- Streamlit App Configuration --------->


st.title("DAE International Qualificacation Bot")

if not check_password():  
    st.stop()


form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area('''Enter your prompt here related to DAE International Qualification entry qualification, course fee or financial aid.
                             e.g. My qualification is Sijil Pelajaran Malaysia (SPM) and I am from Malaysia. What is the entry requirement to Ngee Ann poly course?
                             ''', height=200)

if form.form_submit_button("Submit"):
    
    st.toast(f"User Input Submitted - {user_prompt}")

    st.divider()

    response = process_user_message_2(user_prompt)
    st.write(response)

    st.divider()

    print(response)
   
    st.write('''
            #### IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

            #### Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

            #### Always consult with qualified professionals for accurate and personalized advice.
            ''')
