import streamlit as st
import pandas as pd
import json
import os

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Ngee Ann Polytechnic Course Counseling Bot"
)



with st.expander("Problem Statement"):
    st.write('''
             Ngee Ann Polytechnic admits students through various admission exercises. 
             However, the admissions team faces a significant challenge in managing the high volume of daily inquiries, which often exceed 100 per day. 
             With a small team of only two service representatives, response times are slow, leading to delays in addressing students' questions. 
             
             The majority of these inquiries revolve around understanding:
             1. course detail
             2. skills acquired
             3. exploring potential career paths after graduation. 
             
             This influx of inquiries strains the resources available and hinders the ability to provide timely and effective guidance to prospective students, impacting the overall admissions experience.
    ''')


with st.expander("Project Scope"):
    st.write('''
            To streamline the course counseling process and improve the efficiency of the customer service team, we propose the development of an internal application powered by a Large Language Model (LLM). 
             This application will serve as a bot to reply public enquiries related to course detail, skills acquired from a course and career paths. 
             Enquirer can input their queries related to course to the LLM. The model will process these inputs. 
             The LLM will then assess and provide a clear, text-based explanation or justification for each enquiry, referring to the relevant client information.
    ''')

with st.expander("Objective"):
    st.write('''
            The bot will provide comprehensive guidance on the course, including details below along with relevant course-specific information and data.
             1. course detail
             2. skills acquired
             3. potential career path 
             ''')

# Load the JSON file
filepath = './data/course_coaching_2.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_courses = json.loads(json_string)
    print(dict_of_courses)

# Extract the value of the `dict_of_courses` dictionary
# If you are not sure what the dictionary looks like, you can print it out
list_of_dict = []
for course_name, details_dict in dict_of_courses.items():
    list_of_dict.append(details_dict)

# display the `dict_of_course` as a Pandas DataFrame
df = pd.json_normalize(list_of_dict)

with st.expander("Available Data Source"):
    st.write('''
            A json file related to the course coaching detail.
             ''')
    st.dataframe(df)


current_directory = os.getcwd()
image_path = os.path.join(current_directory, "pages", "methodology1.png")
with st.expander("Methodology"):
    st.image(image_path, caption="Methodology")


with st.expander("GITHUB Link"):
    st.write("https://github.com/jacelee2000/GenAI-week-08")
          