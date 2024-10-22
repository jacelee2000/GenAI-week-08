# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
# from helper_functions import llm
from logics.customer_query_handler import process_user_message
from helper_functions.utility import check_password



# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Ngee Ann Polytechnic Course Counseling Bot"
)


st.title("Course Counseling Bot")

if not check_password():  
    st.stop()
    
form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here related to course counseling e.g. What skills can I acquired after graduated from accountancy course?", height=200)

if form.form_submit_button("Submit"):
    
    st.toast(f"User Input Submitted - {user_prompt}")

    st.divider()

    response, course_details = process_user_message(user_prompt)
    st.write(response)

    st.divider()

    print(course_details)
    df = pd.DataFrame(course_details)
    df 
