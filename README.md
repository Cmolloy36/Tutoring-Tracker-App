## Tutoring-Tracker-App
Tutoring Tracker App

### Purpose
The purpose of this app is to manage SAT & ACT students by providing interactive visuals of their scores over time. 

### Tech Stack
This app is built on a FastAPI backend and leverages streamlit for a simple frontend. Data is stored in a postgres database. The app is dockerized for simplicity of use (but individual services may also be run locally).

### Installing the App
Run `git clone https://github.com/Cmolloy36/Tutoring-Tracker-App` in your desired repository.

### Running the App
Make sure Docker is installed and running on your system. In the root directory, run `docker compose up`. Access `http://localhost:8000/docs`, and be sure to add at least one student and one test for that student. Next, navigate to `http://localhost:8501` to see the data analysis.