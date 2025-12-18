from database.connection import get_connection
from utils.security import hash_password, verify_password

def signup_user(name, email, password, role, shop_name=None):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    hashed = hash_password(password)

    cur.execute(
        "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",
        (name, email, hashed, role)
    )
    user_id = cur.lastrowid

    if role == "vendor":
        cur.execute(
            "INSERT INTO vendors (user_id, shop_name) VALUES (%s,%s)",
            (user_id, shop_name)
        )

    conn.commit()
    conn.close()

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    conn.close()

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user
