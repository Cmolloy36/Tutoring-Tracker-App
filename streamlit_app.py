import streamlit as st
import pandas as pd
import numpy as np
import requests as r

st.write("Student Data Visualization")

get_students_url = f'http://localhost:8000/students' 
response = r.get(get_students_url)
students_data = response.json()
students_df = pd.DataFrame(students_data)

all_students = students_df['name']
test_types = ['ACT','SAT','PSAT']

with st.container(border=True):
    selected_student_name = st.selectbox("Student:",all_students)
    selected_test_type = st.selectbox("Test Type:",test_types)
    student_average = st.toggle("Average all students")


selected_student_id = students_df.loc[students_df['name'] == selected_student_name, 'id']
get_tests_url = f'http://localhost:8000/students/{selected_student_id}/tests' 
response = r.get(get_tests_url)
test_data = response.json()
test_df = pd.DataFrame(test_data)
print(test_df.head())

test_df = test_df.loc[test_df['test_type'] == selected_test_type]

tab1, tab2 = st.tabs(["Chart", "Dataframe"])
tab1.line_chart(x=test_df['id'], y=test_df['english_score'], height=250)
tab2.dataframe(test_df, height=250, use_container_width=True)
