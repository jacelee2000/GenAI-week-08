import streamlit as st
import pandas as pd
import json
import os

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Ngee Ann Polytechnic DAE International Qualification Bot"
)
# endregion <--------- Streamlit App Configuration --------->



with st.expander("Problem Statement"):
    st.write('''
             Ngee Ann Polytechnic admits International Qualifcation students through DAE admission exercises. 
             However, the admissions team faces a significant challenge in managing the high volume of daily inquiries, which often exceed 100 per day. 
             With a small team of only two service representatives, response times are slow, leading to delays in addressing students' questions. 
             
             The majority of these inquiries revolve around understanding:
             1. entry requirement based on nationality, entry qualification 
             2. course fee 
             3. financial aid. 

             This influx of inquiries strains the resources available and hinders the ability to provide timely and effective guidance to prospective students, impacting the overall admissions experience.


    ''')


with st.expander("Project Scope"):
    st.write('''
            To improve the efficiency of the customer service team, we propose the development of an internal application powered by a Large Language Model (LLM). 
             This application will serve as a bot to reply public enquiries related to entry requirement, course fee or financial aid. 
             Enquirer can input their queries related to course to the LLM. The model will process these inputs. 
             The LLM will then assess and provide a clear, text-based explanation or justification for each enquiry, referring to the relevant client information.
    ''')

with st.expander("Objective"):
    st.write('''
            The bot will direct enquirer to the correct Ngee Ann Polytechnic website when enquirer enquiries on:
             1. DAE International Qualification website - for enquiry related to minimum entry requirement for DAE admission exercise.
             2. Course Minimum Entry Requirement website - for enquiry related to course minimum entry requirement 
             3. Course Fee website - for enquiry related to course fee
             4. Financial Aid website - for enquiry related to financial aid
             ''')


with st.expander("Available Data Source"):
    st.write('''
            
             #### DAE International Qualification minimum entry requirement link
             - https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/international-qualification-holder 

            #### Course Minimum Entry REquirement link
             - https://www.np.edu.sg/schools-courses/full-time-courses
            
             #### Course Fee link         
             - https://www.np.edu.sg/admissions-enrolment/academic-matters/course-fees.
            
             #### Financial Aid link      
             - https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/aid 
            
             ''')
 


current_directory = os.getcwd()
image_path = os.path.join(current_directory, "pages", "methodology2.png")
with st.expander("Methodology"):
    st.image(image_path, caption="Methodology")


with st.expander("GITHUB Link"):
    st.write("https://github.com/davidseowccc/AIBC2024_Project/blob/main/README.md ")
          