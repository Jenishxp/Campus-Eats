import streamlit as st
from database.connection import get_connection

def user_dashboard(user):
    st.header(f"Welcome {user['name']} 👋")

    # ---------- CART INIT ----------
    if "cart" not in st.session_state:
        st.session_state.cart = {}

    # ---------- CART UI ----------
    st.subheader("🛒 Your Cart")

    if st.session_state.cart:
        total = 0

        for key, item in st.session_state.cart.items():
            col1, col2, col3, col4 = st.columns([3,1,1,1])

            col1.write(item["item_name"])
            col2.write(f"₹{item['price']}")

            if col3.button("➖", key=f"minus_{key}"):
                item["qty"] -= 1
                if item["qty"] == 0:
                    del st.session_state.cart[key]
                st.rerun()

            col4.write(f"Qty: {item['qty']}")

            if col4.button("➕", key=f"plus_{key}"):
                item["qty"] += 1
                st.rerun()

            total += item["price"] * item["qty"]

        st.markdown(f"### 💰 Total: ₹{total}")

        if st.button("💳 Pay Now"):
            with st.spinner("Processing payment..."):
                place_order(user, st.session_state.cart, total)
            st.balloons()   # 🎉 animation
            st.success("Order placed successfully!")
            st.session_state.cart = {}
            st.rerun()

    else:
        st.info("Cart is empty")

    st.divider()

    # ---------- MENU ----------
    st.subheader("🍽️ Available Food")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            v.id AS vendor_id,
            v.shop_name,
            m.item_name,
            m.price
        FROM menu_items m
        JOIN vendors v ON m.vendor_id = v.id
        WHERE v.is_active = TRUE AND m.is_available = TRUE
        ORDER BY v.shop_name
    """)
    items = cur.fetchall()
    conn.close()

    current_vendor = None
    for item in items:
        if current_vendor != item["shop_name"]:
            st.markdown(f"### 🏪 {item['shop_name']}")
            current_vendor = item["shop_name"]

        col1, col2 = st.columns([3,1])
        col1.write(f"{item['item_name']} — ₹{item['price']}")

        cart_key = f"{item['vendor_id']}_{item['item_name']}"

        if col2.button("Add", key=f"add_{cart_key}"):
            if cart_key in st.session_state.cart:
                st.session_state.cart[cart_key]["qty"] += 1
            else:
                st.session_state.cart[cart_key] = {
                    "item_name": item["item_name"],
                    "vendor_id": item["vendor_id"],
                    "price": item["price"],
                    "qty": 1
                }
            st.success("Added to cart")

# ---------- ORDER + MOCK PAYMENT ----------
def place_order(user, cart, total):
    conn = get_connection()
    cur = conn.cursor()

    # Create order
    cur.execute(
        "INSERT INTO orders (user_id, total) VALUES (%s,%s)",
        (user["id"], total)
    )
    order_id = cur.lastrowid

    # Insert order items
    for item in cart.values():
        cur.execute("""
            INSERT INTO order_items 
            (order_id, vendor_id, item_name, price, quantity)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            order_id,
            item["vendor_id"],
            item["item_name"],
            item["price"],
            item["qty"]
        ))

    conn.commit()
    conn.close()
