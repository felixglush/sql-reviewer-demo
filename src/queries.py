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
