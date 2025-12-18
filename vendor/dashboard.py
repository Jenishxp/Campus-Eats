import streamlit as st
from database.connection import get_connection
from streamlit_autorefresh import st_autorefresh

def vendor_dashboard(user):
    # 🔄 Auto refresh every 5 seconds
    st_autorefresh(interval=5000, key="vendor_refresh")
    st.caption("🔄 Live incoming orders (auto-updating)")
    
    st.header("🧑‍🍳 Vendor Dashboard")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # ---------------- GET VENDOR ID ----------------
    cur.execute(
        "SELECT id, shop_name FROM vendors WHERE user_id=%s",
        (user["id"],)
    )
    vendor = cur.fetchone()

    if not vendor:
        st.error("Vendor profile not found.")
        conn.close()
        return

    vendor_id = vendor["id"]
    st.subheader(f"🏪 {vendor['shop_name']}")

    # ---------------- ADD MENU ITEM ----------------
    st.subheader("➕ Add New Dish")
    dish = st.text_input("Dish Name")
    price = st.number_input("Price", min_value=1)

    if st.button("Add Dish"):
        cur.execute(
            "INSERT INTO menu_items (vendor_id, item_name, price) VALUES (%s,%s,%s)",
            (vendor_id, dish, price)
        )
        conn.commit()
        st.success("Dish added successfully!")
        st.rerun()

    # ---------------- VIEW / DELETE MENU ----------------
    st.subheader("📋 Your Menu")
    cur.execute(
        "SELECT id, item_name, price FROM menu_items WHERE vendor_id=%s",
        (vendor_id,)
    )
    menu_items = cur.fetchall()

    if not menu_items:
        st.info("No dishes added yet.")
    else:
        for item in menu_items:
            col1, col2 = st.columns([3,1])
            col1.write(f"{item['item_name']} — ₹{item['price']}")
            if col2.button("❌ Remove", key=f"del_{item['id']}"):
                cur.execute(
                    "DELETE FROM menu_items WHERE id=%s",
                    (item["id"],)
                )
                conn.commit()
                st.rerun()

    # ---------------- ORDERS MANAGEMENT ----------------
    st.subheader("📦 Incoming Orders")

    cur.execute("""
        SELECT DISTINCT o.id, o.status, o.total, u.name
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN users u ON o.user_id = u.id
        WHERE oi.vendor_id = %s
        ORDER BY o.created_at DESC
    """, (vendor_id,))

    orders = cur.fetchall()

    if not orders:
        st.info("No orders yet.")
    else:
        for o in orders:
            st.write(
                f"🧾 Order #{o['id']} | {o['name']} | ₹{o['total']} | {o['status']}"
            )

            if o["status"] == "paid":
                if st.button("👨‍🍳 Start Preparing", key=f"prep_{o['id']}"):
                    cur.execute(
                        "UPDATE orders SET status='preparing' WHERE id=%s",
                        (o["id"],)
                    )
                    conn.commit()
                    st.rerun()

            elif o["status"] == "preparing":
                if st.button("✅ Mark Ready", key=f"ready_{o['id']}"):
                    cur.execute(
                        "UPDATE orders SET status='ready' WHERE id=%s",
                        (o["id"],)
                    )
                    conn.commit()
                    st.rerun()

    # ---------------- CLOSE CONNECTION ----------------
    conn.close()
