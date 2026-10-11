# ATBU Intelligent Automated Timetable Generation System

## Project Title

**DESIGN AND IMPLEMENTATION OF AN INTELLIGENT AUTOMATED TIMETABLE GENERATION SYSTEM (A CASE STUDY OF COMPUTER SCIENCE DEPARTMENT, ATBU BAUCHI)**

## Overview

The ATBU Intelligent Automated Timetable Generation System is a web-based application designed to assist in the management and generation of academic timetables for the Computer Science Department of Abubakar Tafawa Balewa University (ATBU), Bauchi.

The application uses a constraint-based heuristic approach to arrange courses, lecturers, venues, and time slots while aiming to reduce scheduling conflicts and improve timetable preparation.

## Key Features

- Administrator authentication.
- Department, programme, and level management.
- Lecturer and course management.
- Semester and course offering management.
- Venue and time-slot management.
- Automated timetable generation.
- Timetable viewing and scheduling management.

## Technologies Used

- **Programming Language:** Python
- **Web Framework:** Flask
- **Database Integration:** Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Database:** MySQL/MariaDB
- **Frontend:** HTML, CSS, Jinja2 templates

## Project Structure

```text
atbu-intelligent-timetable-system/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Running the Project Locally

### Prerequisites

Install Python, Git, and MySQL or MariaDB.

### 1. Clone the repository

```powershell
git clone https://github.com/itzemp41-maker/atbu-intelligent-timetable-system.git
cd atbu-intelligent-timetable-system
```

### 2. Create and activate a virtual environment

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install project dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the database

Create a MySQL/MariaDB database named `timetable_atbu`.

Configure the database connection and application secret key using local environment variables. Do not commit your actual `.env` file or production credentials to GitHub.

### 5. Start the application

```powershell
python run.py
```

Open the local address displayed by Flask in your browser.

## Project Status

This repository contains the source code for an academic project. Database configuration, administrator setup, application testing, and deployment should be completed according to the project's environment and requirements.

## Author

Developed as a final-year Computer Science project at Abubakar Tafawa Balewa University, Bauchi.
