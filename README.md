🍽️ Campus Eats – Smart Campus Food Ordering System

Campus Eats is a role-based food ordering web application designed for college campuses.
Students can order food from classrooms or anywhere on campus, vendors prepare food in advance, and students collect food from the canteen — reducing queues and enabling digital payments.

🚀 Features
👤 User (Student)

Browse live menu

Add food to cart with quantity (+ / −)

Mock digital payment

Track order status (Paid → Preparing → Ready → Collected)

Confirm food collection

🧑‍🍳 Vendor (Canteen)

Add / remove menu items

Receive orders in real time

Update order status (Preparing → Ready)

🛠️ Admin

View total users, vendors, and orders

Monitor ready & collected orders

Queue reduction insights

🔄 Real-Time Updates

Auto-refresh dashboards every few seconds

No manual refresh

No repeated login

🧰 Tech Stack

Frontend: Streamlit

Backend: Python

Database: MySQL

Auth: Session-based login

Payments: Mock payment (extendable to UPI)

📁 Project Structure
CE/
│
├── app.py
├── requirements.txt
├── README.md
│
├── auth/
├── user/
├── vendor/
├── admin/
├── database/
├── config/
└── utils/

⚙️ Prerequisites (Friend’s PC)

Make sure your friend has:

Python 3.9+

MySQL 8.0+

Internet connection (for pip installs)

🛠️ Step-by-Step Setup (IMPORTANT)
1️⃣ Clone / Copy Project

Copy the entire CE folder to your friend’s PC.

2️⃣ Create MySQL Database

Open MySQL:

CREATE DATABASE campus_eats;

3️⃣ Update Database Credentials

Edit:

config/db_config.py


Example:

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",   # change if needed
    "database": "campus_eats",
    "port": 3306
}

4️⃣ Install Dependencies

Open terminal in project root (CE folder):

pip install -r requirements.txt


If pip doesn’t work:

python -m pip install -r requirements.txt

5️⃣ Initialize Database Tables
python -m database.init_db

6️⃣ (Optional) Add Demo Data
python -m database.seed_data


This adds:

Sample vendors

Sample dishes

7️⃣ Run the Application
streamlit run app.py


Open browser:

http://localhost:8501

🔑 Sample Flow (For Testing)

Signup as Vendor → add dishes

Signup as User → order food

Vendor marks Preparing → Ready

User marks Collected

Admin monitors system

🔄 Live Updates (No Refresh Needed)

Vendor sees new orders automatically

User sees order status updates live

Sessions remain logged in

🎓 Project Use Case

Campus Eats enables students to order food digitally from classrooms or anywhere on campus. Vendors prepare food in advance, and students collect it directly from the canteen — reducing queues, improving efficiency, and enabling a cashless campus ecosystem.

🚧 Future Enhancements

UPI / wallet integration

QR-based pickup verification

Push notifications

Mobile app version

🏆 Author

Campus Eats
Built as a real-world academic project for smart campus digitization.