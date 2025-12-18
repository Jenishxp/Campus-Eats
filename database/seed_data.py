from database.connection import get_connection

def seed():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (name,email,password,role)
        VALUES ('Demo Vendor','vendor@demo.com','demo','vendor')
    """)
    user_id = cur.lastrowid

    cur.execute("""
        INSERT INTO vendors (user_id, shop_name)
        VALUES (%s,'Demo Canteen')
    """, (user_id,))

    vendor_id = cur.lastrowid

    dishes = [
        ('Veg Puff', 30),
        ('Samosa', 20),
        ('Tea', 15),
        ('Coffee', 25)
    ]

    for name, price in dishes:
        cur.execute(
            "INSERT INTO menu_items (vendor_id,item_name,price) VALUES (%s,%s,%s)",
            (vendor_id, name, price)
        )

    conn.commit()
    conn.close()
    print("Demo vendors & dishes added!")

if __name__ == "__main__":
    seed()
