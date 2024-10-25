import os
import json
import openai
from helper_functions import llm
import requests

school_n_course_name = {'School of Business & Accountancy':['Accountancy',
                                                              'Banking & Finance'],
                            'School of Design & Environment':['Design',
                                                              'Hotel & Leisure Facilities Management'],
                            'School of Engineering':['Aerospace Engineering',
                                                     'Biomedical Engineering'],
                            'School of Film & Media Study':'Mass Communication'}


# Load the JSON file
filepath = './data/course_coaching_2.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_courses = json.loads(json_string)


def identify_category_and_courses(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be enclosed in
    the pair of {delimiter}.

    Decide if the query is relevant to any specific courses
    in the Python dictionary below, which each key is a `school`
    and the value is a list of `course_name`.

    If there are any relevant course(s) found, output the pair(s) of a) `course_name` the relevant courses and b) the associated `school` into a
    list of dictionary object, where each item in the list is a relevant course
    and each course is a dictionary that contains two keys:
    1) school
    2) course_name

    {school_n_course_name}

    If are no relevant courses are found, output an empty list.

    Ensure your response contains only the list of dictionary objects or an empty list, \
    without any enclosing tags or delimiters.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    category_and_product_response_str = llm.get_completion_by_messages(messages)
    category_and_product_response_str = category_and_product_response_str.replace("'", "\"")
    category_and_product_response = json.loads(category_and_product_response_str)
    return category_and_product_response
    

def get_course_details(list_of_relevant_category_n_course: list[dict]):
    course_names_list = []
    for x in list_of_relevant_category_n_course:
        course_names_list.append(x.get('course_name')) # x["course_name"]

    list_of_course_details = []
    for course_name in course_names_list:
        list_of_course_details.append(dict_of_courses.get(course_name))
    return list_of_course_details


def generate_response_based_on_course_details(user_message, product_details):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} If the user is asking about course, \
    understand the relevant course(s) from the following list.
    All available courses shown in the json data below:
    {product_details}

    Step 2:{delimiter} Use the information about the course to \
    generate the answer for the customer's query.
    You must only rely on the facts or information in the course information.
    Your response should be as detail as possible and \
    include information that is useful for customer to better understand the course.

    Step 3:{delimiter}: Answer the customer in a friendly tone.
    Make sure the statements are factually accurate.
    Your response should be comprehensive and informative to help the \
    the customers to make their decision.
    Complete with details such course code, abbreviation, school, poly course code, course name, course description, skills and career to be learnt.
    Use Neural Linguistic Programming to construct your response.

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to customer>

    Make sure to include {delimiter} to separate every step.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_by_messages(messages)
    response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer


def process_user_message(user_input):
    delimiter = "```"

    # Process 1: If Courses are found, look them up
    school_n_course_name = identify_category_and_courses(user_input)
    print("school_n_course_name : ", school_n_course_name)

    # Process 2: Get the Course Details
    course_details = get_course_details(school_n_course_name)

    # Process 3: Generate Response based on Course Details
    reply = generate_response_based_on_course_details(user_input, course_details)


    return reply, course_details


def fetch_website_content(website_url):
    try:
        response = requests.get(website_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text  # Return the website content
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None
    
def generate_response_based_on_course_details_2(user_message):
    delimiter = "####"

    dae_int_qual_url = "https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/international-qualification-holder"
    dae_int_qual_website = fetch_website_content(dae_int_qual_url)

    course_mer_url = "https://www.np.edu.sg/schools-courses/full-time-courses"
    course_mer_website = fetch_website_content(course_mer_url)

    course_fee_url = "https://www.np.edu.sg/admissions-enrolment/academic-matters/course-fees"
    course_fee_website = fetch_website_content(course_fee_url)

    financial_aid_url = "https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/aid  "
    financial_aid_website = fetch_website_content(financial_aid_url)

    system_message = f"""
    You are an AI assistant who drafts replies to queries on the Direct Admissions Exercise (DAE) 
    which is administered by Ngee Ann Polytechnic to allow applicants whose qualification types are 
    ineligible under JAE (Joint Admission Exercise) and JPAE (Joint-Poly Admission Exercise) 
    to apply for admission to our full-time diploma courses.

    - The school is Ngee Ann Polytechnic (NP). The enquirers are mainly prospective or current students and parents.

    ### Important Business Rules
- The replies should be comprehensive to include as much relevant details as possible, in a clear and professional manner, as replied by a staff in the admissions department of the school. Include the relevant hyperlinks if they are mentioned in the data source.
- Answer questions related to minimum entry requirement truthfully based on the data source from the [DAE International Qualification] link whose content in html. The link provides the minimum entry requirements for different qualification. Strictly use the provided info from the {dae_int_qual_website} for your response. From the entry requirement details in the link, think through the steps required to arrive at the correct response. Strickly extract the minimum entry requirements from the {dae_int_qual_website} link only. If you are unsure on how to answer, please direct enquirer to the [DAE International Qualification] link instead.
- For queries related to Course Fees, direct the enquirer to refer to [course fee] link with a hyperlink.  
- For queries related to Financial Aid, direct the enquirer to refer to [financial aid] link with a hyperlink.  
[DAE International Qualification] is website for minimum entry requirement for DAE International Qualification - https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/international-qualification-holder
[course fee] is website for course fee - https://www.np.edu.sg/admissions-enrolment/academic-matters/course-fees
[financial aid] is website for financial aid - https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/aid  
- Examples of qualifications are below for your reference.  
•	International General Certificate of Secondary Education (IGCSE) 
•	International Baccalaureate (IB) Diploma
•	Unified Examination Certificate (UEC)
•	Sijil Pelajaran Malaysia (SPM)
•	Sijil Tinggi Persekolahan Malaysia (STPM)
•	Brunei-Cambridge General Certificate of Education Ordinary Level
•	National College Entrance Examination (NCEE) ‘Gaokao’
•	Year 12 Senior Middle School Graduation Examination Results
•	Year 11 Senior Middle 2 Semester 2 Results
•	Hong Kong Diploma of Secondary Education (HKDSE)
•	Year 10 of Central Board of Secondary Education (CBSE) 
•	Indian Certificate of Secondary Education (ICSE)
•	Higher Secondary School Certificate (Year 12)  
- **Important** The minimum entry requirements details are different depending on enquirer's qualification and nationality country. Do not indicate whether the enqurier can meet the minimum entry requirement, simply extract the minimum entry requirement and direct the enquirer to refer to [DAE International Qualification] link for the minimum entry requirement details. 
- For course minimum entry requirement, direct enquirer to [Course Minimum Entry Requirement].
    

    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_by_messages(messages)
    return response_to_customer


def generate_response_based_on_course_details_3(user_message):
    delimiter = "####"

    system_message = f"""
    You are an AI assistant who drafts replies to queries on the Direct Admissions Exercise (DAE) 
    which is administered by Ngee Ann Polytechnic to allow applicants whose qualification types are 
    ineligible under JAE (Joint Admission Exercise) and JPAE (Joint-Poly Admission Exercise) 
    to apply for admission to our full-time diploma courses.

    - The school is Ngee Ann Polytechnic (NP). The enquirers are mainly prospective or current students and parents.

    ### Important Business Rules
- The replies should be comprehensive to include as much relevant details as possible, in a clear and professional manner, as replied by a staff in the admissions department of the school. Include the relevant hyperlinks if they are mentioned in the data source.
- Answer questions related to minimum entry requirement truthfully based on the data source from the [DAE International Qualification] link whose content in html. The link provides the minimum entry requirements for different qualification. Strictly use the provided info from the [DAE International Qualification] link for your response. From the entry requirement details in the link, think through the steps required to arrive at the correct response. Strickly extract the minimum entry requirements from the [DAE International Qualification] link only. If you are unsure on how to answer, please direct enquirer to the [DAE International Qualification] link instead.
- For queries related to Course Fees, direct the enquirer to refer to [course fee] link with a hyperlink.  
- For queries related to Financial Aid, direct the enquirer to refer to [financial aid] link with a hyperlink.  
[DAE International Qualification] is website for minimum entry requirement for DAE International Qualification - https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/international-qualification-holder
[Course Minimum Entry Requirement] is website for course minimum entyr requirement - https://www.np.edu.sg/schools-courses/full-time-courses
[course fee] is website for course fee - https://www.np.edu.sg/admissions-enrolment/academic-matters/course-fees
[financial aid] is website for financial aid - https://www.np.edu.sg/admissions-enrolment/guide-for-prospective-students/aid  
- Examples of qualifications are below for your reference.  
•	International General Certificate of Secondary Education (IGCSE) 
•	International Baccalaureate (IB) Diploma
•	Unified Examination Certificate (UEC)
•	Sijil Pelajaran Malaysia (SPM)
•	Sijil Tinggi Persekolahan Malaysia (STPM)
•	Brunei-Cambridge General Certificate of Education Ordinary Level
•	National College Entrance Examination (NCEE) ‘Gaokao’
•	Year 12 Senior Middle School Graduation Examination Results
•	Year 11 Senior Middle 2 Semester 2 Results
•	Hong Kong Diploma of Secondary Education (HKDSE)
•	Year 10 of Central Board of Secondary Education (CBSE) 
•	Indian Certificate of Secondary Education (ICSE)
•	Higher Secondary School Certificate (Year 12)  
- **Important** The minimum entry requirements details are different depending on enquirer's qualification and nationality country. Do not indicate whether the enqurier can meet the minimum entry requirement, simply extract the minimum entry requirement and direct the enquirer to refer to [DAE International Qualification] link for the minimum entry requirement details. 
- For course minimum entry requirement, direct enquirer to [Course Minimum Entry Requirement].
    

    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_by_messages(messages)
    return response_to_customer


def process_user_message_2(user_input):
    delimiter = "```"

    # Process 3: Generate Response based on Course Details
    reply = generate_response_based_on_course_details_2(user_input)

    return reply