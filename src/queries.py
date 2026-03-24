import psycopg2


def get_user_by_email(conn, email: str):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, is_active FROM users WHERE email = %s", (email,))
        return cur.fetchone()


def get_orders_for_user(conn, user_id: int):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, status, total_cents FROM orders WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()


def search_users_by_name(conn, name: str):
    """Search users — uses unanchored LIKE, causes full seq scan."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, email, name FROM users WHERE name LIKE %s", (f"%{name}%",))
        return cur.fetchall()


def get_expensive_orders(conn):
    """Fetches high-value orders — no index on total_cents."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT o.id, u.email, o.total_cents
            FROM orders o
            JOIN users u ON u.id = o.user_id
            WHERE o.total_cents > %s
            ORDER BY o.total_cents DESC
            """,
            (10000,),
        )
        return cur.fetchall()


def get_order_details(conn, order_id: int):
    """Loads all order items — no index on product_id."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT oi.product_id, oi.quantity, oi.unit_cents
            FROM order_items oi
            WHERE oi.product_id = %s
            """,
            (order_id,),
        )
        return cur.fetchall()
