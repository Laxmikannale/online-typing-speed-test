# ⌨️ Online Typing Speed Test Platform

## 📌 About the Project

**Online Typing Speed Test Platform** is a web-based application developed using **Python and Django**. 
It allows users to take interactive typing tests and measure their typing speed and accuracy. 
The platform provides user authentication, performance tracking, leaderboard, and notification features through a responsive and user-friendly interface.

## ✨ Key Features

* User registration, login, and logout
* Interactive typing speed tests
* Automatic **WPM and accuracy calculation**
* Performance tracking and leaderboard
* User notifications
* Responsive user interface

## 🧩 Project Modules

### 👤 Accounts Module

The Accounts module manages user-related functionality. It provides **registration, login, logout, and authentication** features.
It ensures that users can securely access the typing test and other personalized features.

### ⌨️ Typing Test Module

The Typing Test module is the main part of the application. Users are provided with text to type and their typing performance is evaluated. 
The system calculates **typing speed (WPM), accuracy, and test results** based on their input.

### 🏆 Leaderboard Module

The Leaderboard module manages and displays users' typing performance. It allows users to view and compare typing scores.
This feature encourages users to improve their typing speed and accuracy.

### 🔔 Notifications Module

The Notifications module manages notifications displayed to users. It provides important system updates and relevant information.
This helps keep users informed while using the application.

## 🛠️ Technologies Used

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
* **Database:** SQLite
  

## ⚙️ How to Run

```bash
git clone https://github.com/Laxmikannale/online-typing-speed-test.git
cd online-typing-speed-test
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver
```

Open in your browser:

```text
http://127.0.0.1:8000/
```

## 🎯 Objective

The main objective of this project is to provide an interactive platform where users can **practice typing, measure their performance, and improve their typing speed and accuracy**.

## 👩‍💻 Developer

**Laxmi Kannale**
