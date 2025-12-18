from streamlit_autorefresh import st_autorefresh
import streamlit as st
from database.connection import get_connection

def user_orders(user):
    st_autorefresh(interval=5000, key="user_orders_refresh")
    st.header("📦 My Orders")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT id, total, status, created_at
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user["id"],))

    orders = cur.fetchall()
    conn.close()

    if not orders:
        st.info("No orders placed yet.")
        return

    for o in orders:
        st.markdown(f"""
        ### 🧾 Order #{o['id']}
        - 💰 Total: ₹{o['total']}
        - 📌 Status: **{o['status'].upper()}**
        - 🕒 Time: {o['created_at']}
        """)

        # ✅ COLLECTED BUTTON (ONLY WHEN READY)
        if o["status"] == "ready":
            if st.button(
                "📍 Mark as Collected",
                key=f"collect_{o['id']}"
            ):
                conn2 = get_connection()
                cur2 = conn2.cursor()
                cur2.execute(
                    "UPDATE orders SET status='collected' WHERE id=%s",
                    (o["id"],)
                )
                conn2.commit()
                conn2.close()

                st.success("Enjoy your meal! 🍽️")
                st.balloons()
                st.rerun()
