import streamlit as st
from database.connection import get_connection

def admin_dashboard(user):
    st.header("🛠️ Admin Dashboard")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS c FROM users")
    st.metric("👥 Total Users", cur.fetchone()["c"])

    cur.execute("SELECT COUNT(*) AS c FROM vendors")
    st.metric("🏪 Active Vendors", cur.fetchone()["c"])

    cur.execute("SELECT COUNT(*) AS c FROM orders")
    total_orders = cur.fetchone()["c"]
    st.metric("📦 Total Orders", total_orders)

    cur.execute("SELECT COUNT(*) AS c FROM orders WHERE status='ready'")
    ready = cur.fetchone()["c"]
    st.metric("✅ Ready for Pickup", ready)

    cur.execute("SELECT COUNT(*) AS c FROM orders WHERE status='collected'")
    collected = cur.fetchone()["c"]
    st.metric("🎯 Orders Collected", collected)

    st.subheader("📉 Queue Reduction Insight")
    st.info(
        f"Out of {total_orders} orders, "
        f"{collected} were collected without queue waiting."
    )

    conn.close()
