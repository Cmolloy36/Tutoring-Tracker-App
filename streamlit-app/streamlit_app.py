import streamlit as st
import pandas as pd
import numpy as np
import requests as r

st.write("Student Data Visualization")

# get_students_url = f'http://localhost:8000/students' # local 
get_students_url = f'http://fastapi-app:8000/students' # for Docker 

response = r.get(get_students_url)
students_data = response.json()
students_df = pd.DataFrame(students_data)

all_students = students_df['name']
test_types = ['ACT','SAT','PSAT']

with st.container(border=True):
    selected_student_name = st.selectbox("Student:",all_students)
    selected_test_type = st.selectbox("Test Type:",test_types)
    student_average = st.toggle("Average all students")

selected_student = students_df.loc[students_df['name'] == selected_student_name]
student_id = selected_student.iloc[0]['id']

# get_tests_url = f'http://localhost:8000/students/{student_id}/tests' # local
get_tests_url = f'http://fastapi-app:8000/students/{student_id}/tests' # for Docker
response = r.get(get_tests_url)
test_data = response.json()
test_df = pd.DataFrame(test_data)
test_df = test_df.loc[test_df['test_type'] == selected_test_type]

tab1, tab2, tab3 = st.tabs(["Bar Chart", "Line Graph", "Dataframe"])

tab1.bar_chart(data=test_df,x='name', y='total_score', color='is_official', height=250)
tab2.line_chart(data=test_df,x='name', y='total_score', height=250)
tab3.dataframe(data=test_df, height=250, width='stretch')
